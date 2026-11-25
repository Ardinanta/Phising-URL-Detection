import hashlib,json,platform,sys,subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from workflow_common import repository_root,run_path
import argparse
_parser=argparse.ArgumentParser();_parser.add_argument('--run',required=True);_args=_parser.parse_args()
root=repository_root();run=run_path(_args.run)
from workflow_common import require_files
require_files(run,['eksperimen_utama/metrik_utama.csv', 'eksperimen_utama/predictions/LR_A_uji.csv.gz', 'stage5_execution/execution_status.json'],"Use scripts/reproduce.py to generate local inputs first.")
out=run/'eksperimen_utama';ev=run/'stage5_execution'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
status=json.loads((ev/'execution_status.json').read_text());assert status['status']=='completed',status
metrics=pd.read_csv(out/'metrik_utama.csv',float_precision='round_trip');hist=pd.read_csv(root/'hasil/metrik_utama.csv',float_precision='round_trip')
members=pd.read_csv(run/'split_membership.csv.gz');cache=pd.read_csv(run/'hasil/fitur_internal.csv.gz')
checks=[];comparisons=[]
for row in metrics.to_dict('records'):
    name,scenario=row['model'],row['skenario'];split='domain' if scenario=='C' else 'acak'
    for prefix,part in [('val','validasi'),('uji','uji')]:
        p=pd.read_csv(out/'predictions'/f'{name}_{scenario}_{prefix}.csv.gz',float_precision='round_trip')
        expected=members.loc[members[split]==part]
        assert np.array_equal(p.clean_row_id,expected.clean_row_id) and np.array_equal(p.url_sha256,expected.url_sha256)
        assert np.array_equal(p.phishing,expected.phishing) and len(p)==row[prefix+'_samples']
        y=p.phishing.to_numpy();score=p.probability_phishing.to_numpy();pred=p.prediction.to_numpy()
        assert np.isfinite(score).all() and ((score>=0)&(score<=1)).all()
        assert (p.threshold==row['ambang']).all() and np.array_equal(score>=row['ambang'],pred)
        tn=int(((y==0)&(pred==0)).sum());fp=int(((y==0)&(pred==1)).sum());fn=int(((y==1)&(pred==0)).sum());tp=int(((y==1)&(pred==1)).sum())
        ranks=rankdata(score,method='average');pos=int(y.sum());neg=len(y)-pos
        auc=(ranks[y==1].sum()-pos*(pos+1)/2)/(pos*neg)
        independent=dict(tn=tn,fp=fp,fn=fn,tp=tp,precision=tp/(tp+fp),recall=tp/(tp+fn),f1=2*tp/(2*tp+fp+fn),fpr=fp/(fp+tn),accuracy=(tp+tn)/len(y),roc_auc=auc)
        for key,val in independent.items():
            delta=abs(float(val)-row[prefix+'_'+key]);assert delta<=1e-12,(name,scenario,prefix,key,delta)
            checks.append(dict(model=name,scenario=scenario,part=prefix,metric=key,recomputed=val,saved=row[prefix+'_'+key],absolute_difference=delta,status='PASS'))
        checks.append(dict(model=name,scenario=scenario,part=prefix,metric='membership_count_label_probability_threshold',recomputed=len(p),saved=row[prefix+'_samples'],absolute_difference=0,status='PASS'))
        if prefix=='val':
            # Independent sweep over descending probability groups, preserving tied scores.
            groups=pd.DataFrame({'score':score,'positive':y}).groupby('score',sort=True).agg(positive=('positive','sum'),count=('positive','size')).iloc[::-1]
            cps=groups.positive.cumsum().to_numpy();fps=groups['count'].cumsum().to_numpy()-cps
            thresholds=np.r_[np.nextafter(score.max(),np.inf),groups.index.to_numpy()]
            cps=np.r_[0,cps];fps=np.r_[0,fps];f1s=2*cps/(pos+cps+fps);fprs=fps/neg
            best=sorted(range(len(thresholds)),key=lambda i:(-f1s[i],fprs[i],-thresholds[i]))[0]
            assert thresholds[best]==row['ambang'],(name,scenario,'threshold mismatch')
            checks.append(dict(model=name,scenario=scenario,part=prefix,metric='validation_threshold_F1_tiebreak',recomputed=thresholds[best],saved=row['ambang'],absolute_difference=0,status='PASS'))
    old=hist.loc[(hist.model==name)&(hist.skenario==scenario)].iloc[0]
    common=['ambang']+[p+'_'+k for p in ['val','uji'] for k in ['tn','fp','fn','tp','precision','recall','f1','fpr','roc_auc']]+['uji_batch_ms']
    for key in common:
        delta=float(row[key]-old[key]);comparisons.append(dict(model=name,scenario=scenario,metric=key,historical=old[key],reproduction=row[key],difference=delta,absolute_difference=abs(delta),note='Timing differs with hardware/load' if key=='uji_batch_ms' else 'Historical per-record predictions unavailable'))
pd.DataFrame(checks).to_csv(out/'independent_host_validation.csv',index=False)
pd.DataFrame(comparisons).to_csv(out/'historical_comparison_full.csv',index=False)
params=json.loads((out/'actual_parameters.json').read_text());authorization=json.loads((ev/'authorization.json').read_text())
assert len(params)==6
for key,value in params.items():assert value['classes']==[0,1]
manifest=json.loads((out/'manifest_eksperimen.json').read_text());manifest['authorization']=authorization;manifest['ram_bytes']=json.loads((run/'run_manifest.json').read_text())['ram_bytes'];manifest['runner_sha256']=sha(run/'02_Eksperimen_Utama.ipynb');manifest['executed_notebook_sha256']=sha(run/'02_Eksperimen_Utama.executed.ipynb');manifest['host_validation_checks']=len(checks)
(out/'manifest_eksperimen.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
oldrun=json.loads((ev/'before_run_manifest.json').read_text());newrun=dict(oldrun)
newrun['stage5']={'status':'completed','completed_at':datetime.now(ZoneInfo('Asia/Bangkok')).isoformat(),'authorization':authorization,'output_directory':str(out),'executed_notebook':'02_Eksperimen_Utama.executed.ipynb','host_validation_checks':len(checks),'baseline_team_approval':'pending'}
(run/'run_manifest.json').write_text(json.dumps(newrun,indent=2),encoding='utf-8');assert all(newrun[k]==v for k,v in oldrun.items())
before=json.loads((ev/'integrity_before.json').read_text());after={k:sha(root/k) for k in before};changed=[k for k in before if before[k]!=after[k]]
allowed={(run/x).relative_to(root).as_posix() for x in ['stage5_preflight.json','run_manifest.json','EXPERIMENT_REPORT.md']}
assert not(set(changed)-allowed),changed
(ev/'integrity_after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
protected=[k for k in before if k not in allowed];assert all(before[k]==after[k] for k in protected)
events=[json.loads(line) for line in (out/'training_log.jsonl').read_text().splitlines()];assert len(events)==6 and all(e['status']=='PASS' for e in events)
warnings=[(e['model'],e['scenario'],w) for e in events for w in e['warnings']]
def table(frame):
    rows=['| '+' | '.join(map(str,frame.columns))+' |','|'+'|'.join(['---']*len(frame.columns))+'|']
    for record in frame.itertuples(index=False,name=None):rows.append('| '+' | '.join(format(v,'.12g') if isinstance(v,float) else str(v) for v in record)+' |')
    return '\n'.join(rows)
summary=metrics[['model','skenario','ambang','val_samples','uji_samples','val_f1','uji_f1','uji_precision','uji_recall','uji_fpr','uji_roc_auc','uji_accuracy']]
cms=metrics[['model','skenario','val_tn','val_fp','val_fn','val_tp','uji_tn','uji_fp','uji_fn','uji_tp']]
timing=metrics[['model','skenario','training_seconds','uji_batch_ms']].copy();timing['historical_batch_ms']=[float(hist.loc[(hist.model==r.model)&(hist.skenario==r.skenario),'uji_batch_ms'].iloc[0]) for r in metrics.itertuples()]
delta=pd.DataFrame(comparisons);performance=delta.loc[delta.metric.isin(['ambang','uji_f1','uji_recall','uji_fpr','uji_roc_auc'])]
lines=['# Hasil Reproduksi Enam Eksperimen Utama - Tahap 5','', 'Status: **SELESAI**. Enam konfigurasi LR/RF x A/B/C berhasil dijalankan. Tidak ada subgroup analysis, reweighting atau tuning tambahan.','', '## Otorisasi, run dan environment','', 'Pengguna secara eksplisit mengotorisasi enam training historis serta guard reproduction-001-six-main. Otorisasi ini bukan persetujuan final baseline seluruh tim; status baseline tetap menunggu tim. Bukti: stage5_execution/authorization.json. Run reproduction-001, branch develop, commit d80117b50f179cfefe91f1c138706264a2934cc7.','', 'Kernel bersih menggunakan .venv Python '+platform.python_version()+' dengan cwd '+str(run)+'. Guard diaktifkan hanya pada environment kernel. Preflight diulang sebelum training dan lagi pada cell 2. Hasil: PASS. Paket: '+json.dumps(manifest['inputs']['packages'])+'. OS '+manifest['os']+'; CPU '+manifest['cpu']+'; RAM '+str(manifest['ram_bytes'])+' byte. Lima versi paket yang tercatat historis sama; Python historis 3.14.4 berbeda dari 3.13.0 saat ini. Dependency transitif/perangkat historis tidak sepenuhnya sama atau tercatat.','', '## Integritas dan perubahan runner','', 'Cache SHA-256 e7678de14cae2ed296d22d2b2644196af551ae12550dab5170413ce000ea3d8a sesuai Tahap 4; 235370 x 42, phishing 100520, legitimate 134850. Membership/label/cache, checksum input, freeze lock, kedua kelas dan nol irisan domain C diperiksa sebelum fit. A/B memakai membership acak sama; B/C fitur identik. Daftar prediktor tidak mengandung label/identifier.','', 'Runner yang disetujui 02_Eksperimen_Utama.ipynb dipertahankan byte-identik selama eksekusi; hasil disimpan terpisah di 02_Eksperimen_Utama.executed.ipynb. RUNNER_CHANGES.md merinci isolasi dari historis: hilangkan weighted/subgroup execution, tambah guard, training timer, classes assertion, logging dan penyimpanan prediksi. Threshold dan metrics mempertahankan AST historis. Tidak ada perubahan source/fungsi setelah melihat test.','', '## Konfigurasi dan evaluasi','', 'LR max_iter=1000, random_state=42; pipeline median imputation -> StandardScaler -> LR. RF n_estimators=60, max_depth=16, min_samples_leaf=3, random_state=42, n_jobs=1; median imputation -> RF. Parameter lain mengikuti library historis; actual_parameters.json menyimpan parameter aktual enam pipeline. A=38 selected features, B=C=15; seed42 dan split Tahap4 dipertahankan.','', 'Fit preprocessing/model hanya train. Ambang memaksimalkan F1 validation; tie-break FPR terendah kemudian threshold tertinggi. Phishing positif1; semua classes_ [0,1]; skor positif predict_proba[:,1]. Test hanya evaluasi/timing. Training tidak diulang untuk mengejar skor.','', '## Hasil utama aktual','', table(summary),'', 'Metrik precision/recall/FPR/ROC-AUC/accuracy validation lengkap terdapat pada eksperimen_utama/metrik_utama.csv; angka tabel dibulatkan untuk keterbacaan, CSV menyimpan presisi aktual.','', '## Confusion matrix aktual','', 'Urutan [TN, FP, FN, TP]; label0 legitimate dan label1 phishing.','',table(cms),'', '## Perbandingan presisi penuh dengan historis','',table(performance[['model','scenario','metric','historical','reproduction','difference','absolute_difference']]),'', 'Perbandingan lengkap validation/test, precision, seluruh confusion counts, threshold, F1, recall, FPR, AUC dan timing tersedia di historical_comparison_full.csv. Nilai historis dibaca dari CSV menggunakan float_precision=round_trip. Kesamaan agregat tidak membuktikan prediksi atau membership historis per record identik; artefak historis per record tidak tersedia.','', '## Validasi independen','',str(len(checks))+' pemeriksaan host lulus. Proses host terpisah membaca kembali 12 CSV prediksi dengan parser round_trip, memverifikasi ID/urutan/label terhadap membership, count dan threshold. Confusion counts, precision, recall, F1, FPR dan accuracy dihitung secara aritmetika; ROC-AUC dihitung independen melalui rank-sum dengan average ranks untuk ties. Semua sesuai CSV dalam toleransi absolut 1e-12. Sweep terpisah atas probability groups validation memverifikasi maksimum F1 serta tie-break threshold. Tidak memakai fungsi metrics/choose_threshold runner untuk validasi host.','', 'Cell 6 juga menghasilkan independent_metric_validation.csv. Bukti validasi host yang lebih lengkap: independent_host_validation.csv.','', '## Training dan inference time','',table(timing),'', 'Training time mengukur pipeline.fit. Inference time median5 pengukuran setelah satu warm-up, batch1024, threadlimit1, sampling seed42. Waktu mencakup preprocessing pipeline dan predict_proba; tidak mencakup ekstraksi URL atau pengambilan halaman. Ini pengukuran batch test, bukan timing terpisah validation/test atau end-to-end. Perbedaan perangkat/load membuat timing bukan kriteria kesamaan metrik. Training time historis tidak tersedia untuk pembandingan.','', '## Selisih antarskenario','',table(pd.read_csv(out/'selisih_utama.csv')),'', 'A/B mengukur tambahan 23 atribut halaman terpilih pada split sama. C/B juga mengubah sampel test dan komposisi kelas. Bias struktur legitimate yang seluruhnya akar pada korpus tetap membatasi interpretasi FPR. Hasil satu seed bukan interval ketidakpastian dan tidak membuktikan generalisasi lintas korpus/periode.','', '## Error dan warning','', 'Semua enam event training PASS. Warning training: '+json.dumps(warnings)+'. Status cell dan output disimpan di notebook executed serta stage5_execution/execution_status.json. Launcher kernel memberi warning lokal TCP tanpa enkripsi; kernel telah dimatikan. Git tetap memperingatkan global ignore tidak dapat dibaca. Tidak ada URL dataset dikunjungi/dicetak.','', '## Perlindungan file lama','', str(len(protected))+' file yang dilindungi tetap identik dengan checksum sebelum eksekusi, termasuk dataset/notebook asli, hasil historis, seluruh dokumen Tahap2/3 dan artefak preprocessing Tahap4. Perubahan yang diizinkan: laporan Tahap5, stage5_preflight.json (dijalankan ulang), dan tambahan field stage5 pada run_manifest.json. Semua field run_manifest sebelumnya dipertahankan. Bukti before/after di stage5_execution/. Tidak ada reset/commit/push.','', '## Inventaris artefak','', '- Notebook executed: 02_Eksperimen_Utama.executed.ipynb.','- metrik_utama.csv, selisih_utama.csv, actual_parameters.json, training_log.jsonl, manifest_eksperimen.json.','- Dua belas predictions/<model>_<scenario>_<val|uji>.csv.gz dengan clean_row_id, hash URL, label, probabilitas phishing, threshold dan prediksi.','- independent_metric_validation.csv dan independent_host_validation.csv.','- historical_comparison.csv dan historical_comparison_full.csv.','- artifact_checksums.json serta stage5_execution/artifact_inventory.csv dengan SHA-256, ukuran dan path.','- stage5_execution/authorization.json, execution_status.json, preflight_stdout.txt, snapshot before laporan/run manifest/preflight dan checksum before/after.','', 'Semua output ML berada di eksperimen_utama/ run ini. Model tidak disimpan (opsional); parameter aktual dan seluruh probabilitas/prediksi tersimpan sehingga hasil evaluasi dapat ditelusuri. Manifest mencatat hash urutan membership tiap bagian A/B/C, input, runner dan notebook executed.','', '## Satu pekerjaan berikutnya','', 'Review hasil aktual bersama tim untuk menetapkan baseline selected features serta menyepakati interpretasi perbedaan A/B/C dengan batas bias dataset dan perbedaan environment. Tidak perlu menjalankan training ulang hanya untuk mengejar kesamaan angka. Artikel ilmiah belum ditulis.']
(run/'EXPERIMENT_REPORT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
# Final hashes cover output files and executed notebook; checksum files exclude themselves.
inventory=[]
for p in sorted(out.rglob('*')):
    if p.is_file() and p.name!='artifact_checksums.json':inventory.append(dict(path=p.relative_to(run).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
for p in [run/'02_Eksperimen_Utama.executed.ipynb',run/'EXPERIMENT_REPORT.md',run/'02_Eksperimen_Utama.ipynb',run/'stage5_preflight.json',run/'run_manifest.json']:
    inventory.append(dict(path=p.relative_to(run).as_posix(),bytes=p.stat().st_size,sha256=sha(p)))
pd.DataFrame(inventory).to_csv(ev/'artifact_inventory.csv',index=False)
(out/'artifact_checksums.json').write_text(json.dumps({r['path']:r['sha256'] for r in inventory},indent=2),encoding='utf-8')
after={k:sha(root/k) for k in before};assert all(before[k]==after[k] for k in protected)
(ev/'integrity_after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
print(table(summary));print(table(timing));print('INDEPENDENT_CHECKS',len(checks),'PROTECTED_UNCHANGED',len(protected),'WARNINGS',warnings)
