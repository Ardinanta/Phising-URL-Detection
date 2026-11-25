"""Local notebook execution helpers. Dependencies: jupyter-client/ipykernel (lockfile)."""
import hashlib,json,os,queue,sys,time
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

def repository_root(start=None):
    start=Path(start or __file__).resolve()
    for p in [start,*start.parents]:
        if (p/'requirements.txt').is_file() and (p/'01_Audit_dan_Split.ipynb').is_file():return p
    raise SystemExit('Repository root not found; keep scripts inside the repository.')

def run_path(value):
    root=repository_root();p=Path(value)
    p=(root/p).resolve() if not p.is_absolute() else p.resolve()
    if root not in p.parents or p.parent!=root/'runs':raise SystemExit('Use a direct child of repository runs/, e.g. runs/reproduction-002')
    if not p.is_dir():raise SystemExit('Run missing. First: python scripts/reproduce.py prepare --run runs/reproduction-002')
    return p

def digest(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()

def now():return datetime.now(ZoneInfo('Asia/Bangkok')).isoformat()

def require_files(run,names,action):
    missing=[n for n in names if not (run/n).is_file()]
    if missing:raise SystemExit('Missing local inputs: '+', '.join(missing)+'. '+action+' No training is started automatically.')

def protected_snapshot(root,exclude=None):
    return {p.relative_to(root).as_posix():digest(p) for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['.git','.venv','__pycache__','.runtime']) and (not exclude or exclude not in p.parents)}

def execute_notebook(path,run,*,authorize=False):
    """Execute only the requested notebook in a new kernel; stop on first error."""
    from jupyter_client import KernelManager
    path=Path(path);run=Path(run);n=json.loads(path.read_text(encoding='utf-8'))
    dest=path.with_name(path.stem+'.executed.ipynb')
    if dest.exists():raise SystemExit('Executed notebook exists; choose a new run rather than overwriting evidence.')
    for c in n['cells']:
        if c['cell_type']=='code':c.update(outputs=[],execution_count=None)
    env=dict(os.environ,MPLCONFIGDIR=str(run/'.runtime/mpl'),IPYTHONDIR=str(run/'.runtime/ipython'),JUPYTER_RUNTIME_DIR=str(run/'.runtime/jupyter'))
    env.pop('TTKI_P1_TRAINING_AUTHORIZED',None)
    if authorize:env['TTKI_P1_TRAINING_AUTHORIZED']=run.name+'-six-main'
    runtime=run/'.runtime';runtime.mkdir(exist_ok=True);(runtime/'jupyter').mkdir(exist_ok=True)
    km=KernelManager();km.kernel_spec.argv=[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'];km.connection_file=str(runtime/'jupyter/kernel.json')
    status={'started_at':now(),'status':'running','cells':[],'interpreter':str(Path(sys.executable).relative_to(repository_root())) if repository_root() in Path(sys.executable).parents else Path(sys.executable).name,'cwd':run.relative_to(repository_root()).as_posix()};kc=None
    try:
        km.start_kernel(cwd=str(run),env=env);kc=km.client();kc.start_channels();kc.wait_for_ready(timeout=60)
        for i,c in enumerate(n['cells'],1):
            r={'cell':i,'type':c['cell_type'],'started_at':now()};status['cells'].append(r)
            if c['cell_type']!='code':r['status']='Markdown preserved';continue
            start=time.monotonic();mid=kc.execute(''.join(c['source']),stop_on_error=True)
            print('CELL',i,'START',flush=True)
            while True:
                try:msg=kc.get_iopub_msg(timeout=1)
                except queue.Empty:continue
                if msg.get('parent_header',{}).get('msg_id')!=mid:continue
                kind=msg['msg_type'];body=msg['content']
                if kind=='execute_input':c['execution_count']=body['execution_count']
                elif kind=='stream':c['outputs'].append(dict(output_type='stream',name=body['name'],text=body['text']))
                elif kind in ['display_data','execute_result']:
                    o=dict(output_type=kind,data=body['data'],metadata=body.get('metadata',{}))
                    if kind=='execute_result':o['execution_count']=body['execution_count']
                    c['outputs'].append(o)
                elif kind=='error':c['outputs'].append(dict(output_type='error',**{k:body[k] for k in ['ename','evalue','traceback']}))
                elif kind=='status' and body['execution_state']=='idle':break
            reply=kc.get_shell_msg(timeout=30)
            while reply.get('parent_header',{}).get('msg_id')!=mid:reply=kc.get_shell_msg(timeout=30)
            r.update(status=reply['content']['status'],seconds=time.monotonic()-start,execution_count=c['execution_count']);dest.write_text(json.dumps(n,indent=1,ensure_ascii=False),encoding='utf-8')
            if r['status']!='ok':raise RuntimeError('Cell failed; outputs/partial artifacts preserved in '+dest.name)
            print('CELL',i,'PASS',flush=True)
        status['status']='completed'
    except Exception as exc:status.update(status='failed',error=str(exc));raise
    finally:
        if kc:kc.stop_channels()
        km.shutdown_kernel(now=True);status['finished_at']=now()
        dest.write_text(json.dumps(n,indent=1,ensure_ascii=False),encoding='utf-8')
        (runtime/(path.stem+'_execution.json')).write_text(json.dumps(status,indent=2),encoding='utf-8')
    return status
