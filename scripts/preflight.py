"""Read-only cache/membership validation; never trains. Requires NumPy/pandas."""
import argparse,json,platform,sys
from pathlib import Path
import numpy as np
import pandas as pd
from importlib.metadata import version
from workflow_common import repository_root,run_path,digest,require_files

def verify(run):
    root=repository_root()
    require_files(run,['hasil/fitur_internal.csv.gz','hasil/manifest_data.json','split_membership.csv.gz','validation_results.json'],'Run preprocessing and validate-cache first.')
    mf=json.loads((run/'hasil/manifest_data.json').read_text());original=json.loads((root/'hasil/manifest_data.json').read_text());v=json.loads((run/'validation_results.json').read_text())
    if not all(x['status']=='PASS' for x in v['checks']):raise SystemExit('Cache validation has failures; training blocked.')
    frame=pd.read_csv(run/'hasil/fitur_internal.csv.gz');members=pd.read_csv(run/'split_membership.csv.gz')
    assert frame.shape==(235370,42) and frame.phishing.value_counts().to_dict()=={0:134850,1:100520}
    assert mf['seed']==42 and mf['fitur_leksikal']==original['fitur_leksikal'] and mf['fitur_halaman']==original['fitur_halaman']
    assert mf['sha256']==digest(run/'Dataset/PhiUSIIL_Phishing_URL_Dataset.csv')==original['sha256']
    assert members.clean_row_id.tolist()==list(range(len(frame))) and members.url_sha256.is_unique
    for field in ['phishing','acak','domain']:assert np.array_equal(frame[field],members[field])
    for split in ['acak','domain']:
        assert set(frame[split])=={'latih','validasi','uji'}
        for part in ['latih','validasi','uji']:assert set(frame.loc[frame[split]==part,'phishing'])=={0,1}
    ds=[set(members.loc[members.domain==p,'domain_sha256']) for p in ['latih','validasi','uji']]
    assert not(ds[0]&ds[1] or ds[0]&ds[2] or ds[1]&ds[2])
    features=mf['fitur_leksikal']+mf['fitur_halaman'];assert len(set(features))==38 and not set(features)&{'phishing','label','URL','domain_terdaftar','struktur','acak','domain','FILENAME'}
    for filename,h in json.loads((run/'artifact_checksums.json').read_text()).items():assert digest(run/filename)==h
    # gzip container hashes may differ between newly generated runs (timestamp); validate the actual run, not a fixed old gzip hash.
    return dict(status='PASS',training_started=False,approval='Training requires explicit CLI flag; baseline team approval pending',shape=list(frame.shape),cache_sha256=digest(run/'hasil/fitur_internal.csv.gz'),membership_sha256=digest(run/'split_membership.csv.gz'),lock_sha256=digest(run/'requirements-lock.txt'),python=platform.python_version(),packages={p:version(p) for p in ['numpy','pandas','scikit-learn','matplotlib','tldextract','threadpoolctl','ipykernel']},feature_counts=[38,15,15],C_domain_overlap=0)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();print(json.dumps(verify(run_path(a.run)),indent=2))
