"""Verify public inventory, syntax and notebook parsing without executing research cells."""
import argparse,ast,hashlib,json,re
from pathlib import Path
from workflow_common import repository_root

def validate(root):
    manifest=json.loads((root/'research/DISTRIBUTION_MANIFEST.json').read_text(encoding='utf-8'))
    problems=[];count=0
    for item in manifest['files']:
        p=root/item['path']
        if not p.is_file():problems.append('Missing '+item['path']);continue
        if hashlib.sha256(p.read_bytes()).hexdigest()!=item['sha256']:problems.append('Checksum '+item['path'])
        if any(x in Path(item['path']).parts for x in ['.venv','predictions','Dataset','mpl_cache']):problems.append('Excluded path '+item['path'])
        if p.suffix in ['.py','.json','.ipynb','.md','.csv','.jsonl','.txt']:
            text=p.read_text(encoding='utf-8')
            if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----',text):problems.append('Secret-like pattern '+item['path'])
            if re.search(r'(?i)C:(?:\\+|/)(?:Users|semester|laragon|Program Files|bot absen)',text):problems.append('Machine path '+item['path'])
            if p.suffix=='.py':ast.parse(text,filename=str(p))
            elif p.suffix in ['.json','.ipynb']:
                obj=json.loads(text)
                if p.suffix=='.ipynb':
                    for c in obj['cells']:
                        if c['cell_type']=='code':ast.parse(''.join(c['source']))
        count+=1
    if problems:raise SystemExit('\n'.join(problems))
    print(f'PASS: {count} public files; checksums, Python AST, JSON/notebook syntax, path/secret-pattern review. No training executed.')
    return count

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path);a=p.parse_args();validate(a.root.resolve() if a.root else repository_root())
