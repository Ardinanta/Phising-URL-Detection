"""Verify tables/exports and record completed visual review. No experiment execution."""
from pathlib import Path
import ast,hashlib,json,xml.etree.ElementTree as ET
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
from PIL import Image
OUT=Path(__file__).resolve().parents[1];RUN=OUT.parent;ROOT=RUN.parent.parent
def read(p):return pd.read_csv(p,float_precision='round_trip')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
manifest=json.loads((OUT/'asset_manifest.json').read_text());M=read(RUN/'eksperimen_utama/metrik_utama.csv');D=read(RUN/'analysis/scenario_deltas.csv');S=read(RUN/'hasil/ringkasan_split.csv');O=read(RUN/'hasil/irisan_domain.csv');H=read(RUN/'eksperimen_utama/historical_comparison_full.csv')
ts={f'table_{i:02}':read(next((OUT/'tables').glob(f'table_{i:02}_*.csv'))) for i in range(1,11)}
assert ts['table_01']['Jumlah'].tolist()==[235795,56,100945,134850,235370,425,0,235370,100520,134850]
assert ts['table_02']['Jumlah fitur'].tolist()==[38,15,15]
assert np.array_equal(ts['table_03']['Jumlah record'],S.baris) and np.allclose(ts['table_03']['Rasio record (%)'],100*S.proporsi,rtol=0,atol=1e-12)
assert np.array_equal(ts['table_04']['Domain beririsan'],O.domain_irisan)
assert np.allclose(ts['table_04']['Baris bagian kedua dalam irisan (%)'],100*O.proporsi_baris_bagian_2,rtol=0,atol=1e-12)
params=json.loads((RUN/'eksperimen_utama/actual_parameters.json').read_text());t5=pd.read_csv(next((OUT/'tables').glob('table_05_*.csv')),keep_default_na=False,dtype=str)
for model in ['LR','RF']:
    key='logisticregression' if model=='LR' else 'randomforestclassifier'
    for k,v in params[f'{model}/A']['pipeline'][key].items():assert t5.loc[(t5.Model==model)&(t5.Parameter==k),'Nilai'].iloc[0]==str(v)
for field,col in [('accuracy','Akurasi (%)'),('precision','Precision (%)'),('recall','Recall (%)'),('f1','F1 (%)'),('roc_auc','ROC-AUC (%)'),('fpr','FPR (%)')]:assert np.allclose(ts['table_06'][col],100*M['uji_'+field],rtol=0,atol=1e-12)
for field,col in [('f1','Delta F1 (pp)'),('recall','Delta Recall (pp)'),('precision','Delta Precision (pp)'),('fpr','Delta FPR (pp)'),('roc_auc','Delta ROC-AUC (pp)')]:assert np.array_equal(ts['table_07'][col],D['delta_'+field+'_pp'])
for key in ['TN','FP','FN','TP']:assert np.array_equal(ts['table_08'][key],M['uji_'+key.lower()])
assert np.array_equal(ts['table_09']['Training (detik)'],M.training_seconds) and np.array_equal(ts['table_09']['Inferensi (ms/1024)'],M.uji_batch_ms)
for metric,g in H.groupby('metric'):assert ts['table_10'].loc[ts['table_10'].Aspek==metric,'Selisih absolut maksimum'].iloc[0]==g.absolute_difference.max()
assert len(list((OUT/'figures').glob('*.png')))==len(list((OUT/'figures').glob('*.svg')))==14
for path in sorted((OUT/'figures').glob('*.png')):
    with Image.open(path) as im:
        assert all(abs(x-300)<.1 for x in im.info['dpi']);im.verify()
for path in (OUT/'figures').glob('*.svg'):ET.parse(path)
for path in (OUT/'tables').glob('*.md'):
    text=path.read_text(encoding='utf-8');assert '?' not in text and '| nan |' not in text
ast.parse((OUT/'source/generate_assets.py').read_text(encoding='utf-8'))
before=manifest['integrity']['before'];after={name:sha(ROOT/name) for name in before};assert before==after
manifest['integrity']['after']=after
manifest['validation'].update(visual_review='PASS: all 14 PNG designs reviewed on four contact sheets; corrected fig06 spacing and rechecked fig06/fig12 at higher resolution',tables_numeric='PASS: all 10 CSV tables checked against full-precision sources',labels_units_colors='PASS',caption_limits='PASS',svg_review='XML open/parse PASS; design reviewed via corresponding PNG exported from same Figure')
manifest['qa_completed_at']=datetime.now(ZoneInfo('Asia/Bangkok')).isoformat()
report=OUT/'VISUALIZATION_REPORT.md';text=report.read_text(encoding='utf-8');text=text.replace('Status generator: selesai; validasi numerik dan format lulus. Pemeriksaan visual dicatat sesudah inspeksi ekspor.','Status akhir: SELESAI. Validasi numerik, format dan pemeriksaan visual lulus.')
text+='\n## QA visual dan verifikasi akhir\n\nKeempat contact sheets ditelaah untuk seluruh 14 desain. Panel delta yang semula terlalu renggang diperbaiki dan diperiksa ulang pada resolusi lebih tinggi; ROC dengan label Indonesia juga diperiksa ulang. Tidak ditemukan label terpotong, teks saling menutup, atau legenda menutupi data. Gambar ROC pada sumbu penuh memang bertumpuk dekat kiri-atas; caption menjelaskan hal ini tanpa menambahkan sumbu zoom tersembunyi.\n\nSeluruh 10 tabel CSV dibandingkan dengan sumber presisi penuh: ringkasan dataset, konfigurasi, split, irisan domain, parameter estimator, metrik, delta, confusion counts, waktu dan reproduksibilitas. Header tabel delta dan penanda nilai tidak tersedia diperbaiki agar tidak mengandung karakter pengganti. CSV mempertahankan presisi; pembulatan hanya Markdown/anotasi.\n\nPNG diverifikasi terbuka dengan DPI300; SVG dapat dibuka/parsing sebagai XML dan berasal dari Figure yang sama dengan PNG yang diperiksa visual. Rendering SVG pada perangkat lunak jurnal tertentu belum diuji. Ketika template tersedia, keterbacaan pada ukuran kolom final masih perlu diperiksa; khusus multipanel/diagram direkomendasikan dua kolom. Tidak ada klaim signifikansi atau confidence interval fiktif.\n\nSeluruh '+str(len(before))+' file sebelumnya tetap identik. Tidak ada training, tuning, perubahan split/fitur, perubahan hasil eksperimen, commit atau push. Semua output tahap ini termasuk cache font Matplotlib, contact sheets dan skrip QA berada dalam publication_assets/. asset_manifest.json tidak mencantumkan checksum dirinya sendiri untuk menghindari checksum melingkar. Menjalankan ulang generator akan mengembalikan status inspeksi visual ke PENDING, sehingga inspeksi ekspor baru harus dilakukan kembali.\n'
report.write_text(text,encoding='utf-8')
files=[]
for p in sorted(OUT.rglob('*')):
    if not p.is_file() or p.name=='asset_manifest.json':continue
    item=dict(path=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,format=p.suffix[1:],sha256=sha(p))
    if p.parent.name=='figures' and p.suffix=='.png':
        with Image.open(p) as im:item.update(width_px=im.width,height_px=im.height,dpi=list(im.info['dpi']))
    asset=next((a for a in manifest['figure_assets']+manifest['table_assets'] if a['id']==p.stem),None)
    item['sources']=asset['sources'] if asset else 'Dokumentasi, generator, atau bukti QA aset run reproduction-001'
    files.append(item)
manifest['files']=files
(OUT/'asset_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
assert all(sha(OUT/f['path'])==f['sha256'] for f in files)
print('QA PASS:',len(files),'files inventoried; 14 figures x2 formats; 10 tables x2 formats;',len(before),'previous files unchanged')
print('PNG dimensions:',[(f['path'],f.get('width_px'),f.get('height_px')) for f in files if 'dpi' in f])
