"""Portable orchestration. No command invokes training except train --authorize-training.
Dependencies: project requirements/lockfile; validation also uses transitive scipy.
"""
import argparse,hashlib,json,platform,shutil,subprocess,sys
from pathlib import Path
from importlib.metadata import version
from workflow_common import repository_root,run_path,digest,now,require_files,protected_snapshot,execute_notebook
ROOT=repository_root();REFERENCE=ROOT/'research/runs/reproduction-001'

def prepare(value):
    p=(ROOT/value).resolve()
    if p.parent!=ROOT/'runs' or p.exists():raise SystemExit('Choose a new runs/<run-id>; existing directories are never overwritten.')
    source=ROOT/'Dataset/PhiUSIIL_Phishing_URL_Dataset.csv'
    if not source.is_file():raise SystemExit('Place the locally obtained PhiUSIIL CSV in Dataset/ (see README). No download is performed.')
    ref=json.loads((ROOT/'hasil/manifest_data.json').read_text());assert digest(source)==ref['sha256'],'Dataset differs from historical checksum; stop for review.'
    p.mkdir(parents=True);(p/'Dataset').mkdir();(p/'hasil').mkdir()
    for name in ['01_Audit_dan_Split.ipynb','02_Eksperimen_dan_Evaluasi.ipynb','requirements-lock.txt']:shutil.copyfile(ROOT/name,p/name)
    shutil.copyfile(source,p/'Dataset'/source.name)
    shutil.copyfile(REFERENCE/'02_Eksperimen_Utama.ipynb',p/'02_Eksperimen_Utama.ipynb')
    shutil.copyfile(REFERENCE/'stage5_preflight.py',p/'stage5_preflight.py')
    manifest=dict(run_id=p.name,created_at=now(),purpose='Historical configuration reproduction only',baseline_approval='pending team',branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip(),commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),python=platform.python_version(),packages={pkg:version(pkg) for pkg in ['numpy','pandas','scikit-learn','matplotlib','tldextract','threadpoolctl','ipykernel']},os=platform.platform(),cpu=platform.processor(),working_directory=p.relative_to(ROOT).as_posix(),output_directory=(p/'hasil').relative_to(ROOT).as_posix(),seed=42,input_checksums={name:digest(p/name) for name in ['01_Audit_dan_Split.ipynb','02_Eksperimen_dan_Evaluasi.ipynb','Dataset/PhiUSIIL_Phishing_URL_Dataset.csv','requirements-lock.txt']},status='prepared',cells=[],kernel_preflight={'cwd':p.relative_to(ROOT).as_posix()},ram_bytes=0)
    try:
        import psutil
        manifest['ram_bytes']=psutil.virtual_memory().total
    except ImportError:pass
    (p/'run_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8');print('Prepared',p.relative_to(ROOT))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('command',choices=['prepare','preprocess','validate-cache','preflight','train','validate-metrics','analysis','figures']);parser.add_argument('--run',required=True);parser.add_argument('--authorize-training',action='store_true');args=parser.parse_args()
    if args.command=='train' and not args.authorize_training:raise SystemExit('Training is blocked. Use train --authorize-training only after explicit authorization for the historical six configurations.')
    if args.command=='prepare':prepare(args.run);return
    run=run_path(args.run)
    if args.command=='preprocess':
        require_files(run,['01_Audit_dan_Split.ipynb','Dataset/PhiUSIIL_Phishing_URL_Dataset.csv'],'Use prepare first.')
        if any((run/'hasil').iterdir()):raise SystemExit('hasil/ is not empty; choose a fresh run.')
        before=protected_snapshot(ROOT,exclude=run);(run/'historical_integrity_before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
        status=execute_notebook(run/'01_Audit_dan_Split.ipynb',run)
        p=run/'run_manifest.json';m=json.loads(p.read_text());m.update(status='execution_success',cells=status['cells']);p.write_text(json.dumps(m,indent=2),encoding='utf-8')
    elif args.command in ['validate-cache','validate-metrics']:
        filename='validate_cache.py' if args.command=='validate-cache' else 'validate_metrics.py'
        subprocess.run([sys.executable,str(ROOT/'scripts'/filename),'--run',str(run)],cwd=ROOT,check=True)
    elif args.command=='preflight':
        from preflight import verify
        print(json.dumps(verify(run),indent=2))
    elif args.command=='train':
        from preflight import verify
        result=verify(run)
        if (run/'eksperimen_utama').exists() or (run/'stage5_execution').exists():raise SystemExit('Experiment outputs already exist; preserve them and choose a new run.')
        (run/'stage5_preflight.json').write_text(json.dumps(result,indent=2),encoding='utf-8');ev=run/'stage5_execution';ev.mkdir()
        for name in ['run_manifest.json','stage5_preflight.json']:(ev/('before_'+name)).write_bytes((run/name).read_bytes())
        before=protected_snapshot(ROOT);(ev/'integrity_before.json').write_text(json.dumps(before,indent=2),encoding='utf-8')
        auth=dict(authorized=True,basis='User supplied explicit --authorize-training CLI flag',scope=['LR/A','LR/B','LR/C','RF/A','RF/B','RF/C'],baseline_team_approval='pending',recorded_at=now(),guard=run.name+'-six-main');(ev/'authorization.json').write_text(json.dumps(auth,indent=2),encoding='utf-8')
        try:status=execute_notebook(run/'02_Eksperimen_Utama.ipynb',run,authorize=True)
        except Exception:
            runtime=run/'.runtime/02_Eksperimen_Utama_execution.json'
            if runtime.exists():shutil.copyfile(runtime,ev/'execution_status.json')
            raise
        (ev/'execution_status.json').write_text(json.dumps(status,indent=2),encoding='utf-8')
        print('Six main experiments complete. Run validate-metrics next; no automatic retraining.')
    elif args.command=='analysis':
        require_files(run,['eksperimen_utama/independent_host_validation.csv','eksperimen_utama/predictions/LR_A_uji.csv.gz'],'Generate local predictions with authorized train, then validate-metrics.')
        dest=run/'analysis'
        if dest.exists():raise SystemExit('analysis/ already exists; do not overwrite evidence.')
        dest.mkdir();shutil.copyfile(REFERENCE/'analysis/analysis_results.ipynb',dest/'analysis_results.ipynb');execute_notebook(dest/'analysis_results.ipynb',dest)
    elif args.command=='figures':
        require_files(run,['analysis/validation_manifest.json','eksperimen_utama/predictions/RF_C_uji.csv.gz'],'Run analysis after producing local predictions. Published static figures are already in research/.')
        dest=run/'publication_assets'
        if dest.exists():raise SystemExit('publication_assets/ exists; use a new run or explicitly regenerate with its generator.')
        (dest/'source').mkdir(parents=True)
        shutil.copyfile(REFERENCE/'publication_assets/source/generate_assets.py',dest/'source/generate_assets.py')
        subprocess.run([sys.executable,str(dest/'source/generate_assets.py')],cwd=ROOT,check=True)

if __name__=='__main__':main()
