import ast,csv,gzip,hashlib,json,platform,sys
from pathlib import Path
from itertools import combinations
from ipaddress import ip_address
from urllib.parse import urlsplit
from datetime import datetime
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import tldextract
from workflow_common import repository_root,run_path
import argparse
_parser=argparse.ArgumentParser();_parser.add_argument('--run',required=True);_args=_parser.parse_args()
root=repository_root();run=run_path(_args.run)
from workflow_common import require_files
require_files(run,['run_manifest.json', 'hasil/fitur_internal.csv.gz', 'Dataset/PhiUSIIL_Phishing_URL_Dataset.csv'],"Use scripts/reproduce.py to generate local inputs first.")
m=json.loads((run/'run_manifest.json').read_text()); assert m['status']=='execution_success'
def sha(p):
 with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
manifest=json.loads((run/'hasil/manifest_data.json').read_text()); old=json.loads((root/'hasil/manifest_data.json').read_text())
lex=manifest['fitur_leksikal']; page=manifest['fitur_halaman']; findings=[]; comparisons=[]
def check(name,ok,details): findings.append({'check':name,'status':'PASS' if bool(ok) else 'FAIL','details':details}); print(name,findings[-1]['status'],flush=True)
def compare(name,historical,actual,note=''):
 if isinstance(historical,(int,float)) and isinstance(actual,(int,float)):
  delta=actual-historical; same=abs(delta)<=1e-12
 else: delta='-' ; same=historical==actual
 comparisons.append({'aspect':name,'historical':historical,'reproduction':actual,'difference':delta,'status':'cocok' if same else 'tidak cocok','notes':note})
raw=pd.read_csv(run/'Dataset/PhiUSIIL_Phishing_URL_Dataset.csv',dtype={'URL':'string'})
missing_default={k:int(v) for k,v in raw.isna().sum().items() if v}
literal=pd.read_csv(run/'Dataset/PhiUSIIL_Phishing_URL_Dataset.csv',usecols=['TLD','Title'],keep_default_na=False)
missing_literal={k:int(v) for k,v in literal.eq('').sum().items() if v}
y=(raw['label']==0).astype('int8'); conflicts=raw.groupby('URL')['label'].nunique(); bad=set(conflicts[conflicts>1].index)
clean=raw.loc[~raw['URL'].isin(bad)].drop_duplicates('URL').copy(); original_ids=clean.index.to_numpy(); clean=clean.reset_index(drop=True)
internal=pd.read_csv(run/'hasil/fitur_internal.csv.gz')
check('schema_internal',list(internal.columns)==['phishing',*page,'struktur',*lex,'acak','domain'],{'rows':len(internal),'columns':len(internal.columns),'lexical':len(lex),'page':len(page)})
check('internal_rows_labels',len(internal)==len(clean) and np.array_equal(internal['phishing'].to_numpy(),(clean['label']==0).astype(int).to_numpy()),'Label positif 1 tepat untuk label asli 0; baris mengikuti urutan deduplikasi keep-first')
check('page_features_integrity',internal[page].equals(clean[page]),'Seluruh 23 kolom dibandingkan dengan CSV deduplikasi')
check('missing_model_inputs',not internal[['phishing',*page,*lex,'struktur','acak','domain']].isna().any().any(),'Tidak ada missing pada fitur/target/penanda split aktual')
ext=tldextract.TLDExtract(cache_dir=None,suffix_list_urls=(),include_psl_private_domains=True)
# Independent host-side implementation; no notebook function or kernel variables reused.
domains=[]; structures=[]; values=[]; ip_fallback=0; unknown_fallback=0; private_count=0
for url in clean['URL']:
 parsed=urlsplit(url); host=parsed.hostname.rstrip('.').encode('idna').decode('ascii')
 try: ip_address(host); ipflag=1; domain=host; ip_fallback+=1
 except ValueError:
  ipflag=0; extracted=ext(host); domain=extracted.top_domain_under_public_suffix or host
  private_count+=int(extracted.is_private); unknown_fallback+=int(not extracted.top_domain_under_public_suffix)
 segments=sum(bool(x) for x in parsed.path.split('/'))
 structure='query' if parsed.query else ('path' if segments else 'akar')
 counts={'alpha':0,'digit':0,'other':0}
 for character in url: counts['alpha' if character.isalpha() else 'digit' if character.isdigit() else 'other']+=1
 values.append([len(url),len(host),len(parsed.path),len(parsed.query),host.count('.'),counts['alpha'],counts['digit'],counts['other'],host.count('-'),segments,url.count('%'),parsed.query.count('='),parsed.query.count('&'),int(parsed.scheme=='https'),ipflag])
 domains.append(domain); structures.append(structure)
expected=pd.DataFrame(values,columns=lex)
check('lexical_all_rows',np.array_equal(expected.to_numpy(),internal[lex].to_numpy()),'15 fitur dihitung ulang pada seluruh URL unik secara terpisah dari kernel')
check('structure_all_rows',np.array_equal(np.array(structures),internal['struktur'].to_numpy()),'Query nonkosong diprioritaskan, lalu segmen path, lalu akar')
url_hashes=clean['URL'].map(lambda x:hashlib.sha256(x.encode('utf-8')).hexdigest())
domain_hashes=pd.Series(domains).map(lambda x:hashlib.sha256(x.encode('utf-8')).hexdigest())
check('unique_stable_ids',url_hashes.is_unique,'SHA-256 UTF-8 teks URL asli unik; tidak mencetak URL mentah')
membership=pd.DataFrame({'clean_row_id':np.arange(len(clean)),'source_record_id_zero_based':original_ids,'url_sha256':url_hashes,'domain_sha256':domain_hashes,'phishing':internal['phishing'],'acak':internal['acak'],'domain':internal['domain']})
membership.to_csv(run/'split_membership.csv.gz',index=False)
overlap=[]; summary=[]
for protocol in ['acak','domain']:
 parts={name:np.flatnonzero(internal[protocol].to_numpy()==name) for name in ['latih','validasi','uji']}
 allocated=np.concatenate(list(parts.values()))
 check(protocol+'_exactly_once',len(allocated)==len(clean) and np.array_equal(np.sort(allocated),np.arange(len(clean))),'Setiap ID baris teralokasi tepat sekali; tidak ada bagian tidak dikenal/missing')
 for name,ids in parts.items():
  classes=set(internal.iloc[ids]['phishing']); check(protocol+'_'+name+'_both_classes',classes=={0,1},'Kedua kelas ada')
  summary.append({'split':protocol,'bagian':name,'baris':len(ids),'proporsi':len(ids)/len(clean),'sah':int((internal.iloc[ids]['phishing']==0).sum()),'phishing':int(internal.iloc[ids]['phishing'].sum()),'domain_unik':len(set(np.array(domains)[ids]))})
 for a,b in combinations(parts,2):
  ia,ib=parts[a],parts[b]; url_overlap=len(set(url_hashes.iloc[ia])&set(url_hashes.iloc[ib])); row_overlap=len(set(ia)&set(ib)); shared=set(np.array(domains)[ia])&set(np.array(domains)[ib])
  overlap.append({'split':protocol,'bagian_1':a,'bagian_2':b,'url_irisan':url_overlap,'baris_irisan':row_overlap,'domain_irisan':len(shared),'proporsi_baris_bagian_2':float(np.isin(np.array(domains)[ib],list(shared)).mean())})
  check(protocol+'_'+a+'_'+b+'_disjoint_urls_rows',url_overlap==row_overlap==0,{'url_overlap':url_overlap,'row_overlap':row_overlap})
  if protocol=='domain': check('domain_'+a+'_'+b+'_zero_domains',not shared,{'domain_overlap':len(shared)})
pd.DataFrame(summary).to_csv(run/'independent_split_summary.csv',index=False); pd.DataFrame(overlap).to_csv(run/'independent_overlap.csv',index=False)
saved_summary=pd.read_csv(run/'hasil/ringkasan_split.csv'); saved_overlap=pd.read_csv(run/'hasil/irisan_domain.csv')
check('independent_summary_matches',all(np.allclose(saved_summary[c],pd.DataFrame(summary)[c],rtol=0,atol=1e-12) for c in ['baris','proporsi','sah','phishing','domain_unik']),'Agregat dihitung dari membership dan domain ekstraksi independen')
check('independent_overlap_matches',all(np.allclose(saved_overlap[c],pd.DataFrame(overlap)[c],rtol=0,atol=1e-12) for c in ['domain_irisan','proporsi_baris_bagian_2']),'Irisan dan proporsi dibandingkan artefak notebook')
# Read config statically: never execute notebook 2.
n2=json.loads((run/'02_Eksperimen_dan_Evaluasi.ipynb').read_text(encoding='utf-8')); config_node=None
for c in n2['cells']:
 if c['cell_type']=='code':
  tree=ast.parse(''.join(c['source']))
  for node in tree.body:
   if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='config' for t in node.targets): config_node=node.value
cfg=dict(zip([ast.literal_eval(k) for k in config_node.keys],config_node.values))
a_split=ast.literal_eval(cfg['A'].elts[0]); b_split=ast.literal_eval(cfg['B'].elts[0])
check('A_B_membership_design',a_split==b_split=='acak','Config N2 cell 6 dan filter N2 cell 4 menggunakan kolom split acak yang sama; notebook 2 tidak dijalankan')
check('B_C_identical_features',ast.dump(cfg['B'].elts[1])==ast.dump(cfg['C'].elts[1]) and isinstance(cfg['B'].elts[1],ast.Name) and cfg['B'].elts[1].id=='LEXICAL','Pemeriksaan AST N2 cell 6; 15 fitur identik')
for name,h,a in [('baris mentah',235795,len(raw)),('kolom asli',56,len(raw.columns)),('phishing mentah',100945,int((raw.label==0).sum())),('legitimate mentah',134850,int((raw.label==1).sum())),('URL unik',235370,int(raw.URL.nunique())),('pengulangan teks URL',425,len(raw)-raw.URL.nunique()),('konflik label URL',0,len(bad)),('baris bersih',235370,len(clean)),('phishing bersih',100520,int((clean.label==0).sum())),('legitimate bersih',134850,int((clean.label==1).sum())),('fitur leksikal',15,len(lex)),('atribut halaman',23,len(page))]: compare(name,h,int(a))
for name in ['ringkasan_split.csv','irisan_domain.csv','audit_struktur_mentah.csv','distribusi_struktur_split.csv']:
 historical=pd.read_csv(root/'hasil'/name); fresh=pd.read_csv(run/'hasil'/name)
 equal=list(historical.columns)==list(fresh.columns) and historical.shape==fresh.shape
 for col in historical.columns:
  if pd.api.types.is_numeric_dtype(historical[col]): equal=equal and np.allclose(historical[col],fresh[col],rtol=0,atol=1e-12)
  else: equal=equal and historical[col].equals(fresh[col])
 compare('tabel '+name,'seluruh nilai historis','seluruh nilai historis' if equal else 'berbeda','Toleransi numerik absolut 1e-12; urutan baris diperiksa')
for idx,row in saved_summary.iterrows():
 h=pd.read_csv(root/'hasil/ringkasan_split.csv').iloc[idx]
 for field in ['baris','proporsi','sah','phishing','domain_unik']: compare(row['split']+'/'+row['bagian']+'/'+field,float(h[field]),float(row[field]))
for idx,row in saved_overlap.iterrows():
 h=pd.read_csv(root/'hasil/irisan_domain.csv').iloc[idx]; compare('irisan '+row['split']+'/'+row['bagian_1']+'/'+row['bagian_2'],int(h['domain_irisan']),int(row['domain_irisan']))
compare('checksum CSV',old['sha256'],manifest['sha256'])
compare('Python',old['python'],manifest['python'],'Perbedaan environment yang diketahui; tidak mengubah definisi atau seed')
for pkg,v in manifest['paket'].items(): compare('versi '+pkg,old['paket'][pkg],v)
comparisons.append({'aspect':'Keanggotaan historis per baris','historical':'Artefak per baris tidak tersedia','reproduction':'Membership baru disimpan','difference':'-','status':'belum dapat diverifikasi','notes':'Kesamaan statistik agregat tidak membuktikan membership historis identik'})
# Verify lexical manifests against actual static lists in copied N1.
n1=json.loads((run/'01_Audit_dan_Split.ipynb').read_text(encoding='utf-8')); lists={}
for c in n1['cells']:
 if c['cell_type']=='code':
  for node in ast.parse(''.join(c['source'])).body:
   if isinstance(node,ast.Assign):
    for t in node.targets:
     if isinstance(t,ast.Name) and t.id in ['LEXICAL','PAGE']: lists[t.id]=ast.literal_eval(node.value)
check('manifest_feature_lists',lex==lists['LEXICAL'] and page==lists['PAGE'],'Daftar dan urutan sesuai kode salinan identik')
check('manifest_audit',manifest['audit']=={'baris_mentah':len(raw),'url_unik':raw.URL.nunique(),'duplikat_tambahan':len(raw)-raw.URL.nunique(),'url_konflik_label':len(bad),'baris_bersih':len(clean)},'Dihitung ulang dari CSV lokal')
# Raw structure aggregates from independent URL->structure mapping.
lookup=dict(zip(clean.URL,structures)); raw_struct=raw.URL.map(lookup)
ind_counts=pd.crosstab(raw_struct,y).reindex(index=['akar','path','query'],columns=[0,1],fill_value=0)
saved_counts=pd.read_csv(run/'hasil/audit_struktur_mentah.csv',index_col=0)
check('raw_structure_counts',np.array_equal(ind_counts.to_numpy(),saved_counts.to_numpy()),'Seluruh baris mentah, termasuk URL berulang, dihitung ulang')
# Preserve missing audit without URL values.
pd.DataFrame({'column':raw.columns,'missing_pandas_default':raw.isna().sum().values}).to_csv(run/'missing_values.csv',index=False)
before=json.loads((run/'historical_integrity_before.json').read_text()); after={name:sha(root/name) for name in before}; changed=[name for name in before if before[name]!=after[name]]
check('historical_files_unchanged',not changed,{'files':len(before),'changed':changed})
(run/'historical_integrity_after.json').write_text(json.dumps(after,indent=2),encoding='utf-8')
artifact_paths=sorted((run/'hasil').iterdir())+[run/'split_membership.csv.gz',run/'independent_split_summary.csv',run/'independent_overlap.csv',run/'missing_values.csv',run/'01_Audit_dan_Split.executed.ipynb']
checksums={p.relative_to(run).as_posix():sha(p) for p in artifact_paths}
(run/'artifact_checksums.json').write_text(json.dumps(checksums,indent=2),encoding='utf-8')
pd.DataFrame(comparisons).to_csv(run/'comparison.csv',index=False)
executed=json.loads((run/'01_Audit_dan_Split.executed.ipynb').read_text(encoding='utf-8')); messages=[]
for i,c in enumerate(executed['cells'],1):
 for o in c.get('outputs',[]):
  if o['output_type']=='stream': messages.append({'cell':i,'name':o['name'],'text':o['text']})
  elif o['output_type']=='error': messages.append({'cell':i,'error':o['ename'],'text':o['evalue']})
report={'checks':findings,'missing_default_na':missing_default,'literal_empty_values_title_tld':missing_literal,'domain_definition':{'tldextract':manifest['paket']['tldextract'],'private_suffix':True,'network_suffix_urls':[],'cache_dir':None,'ip_fallback_rows':ip_fallback,'unknown_suffix_fallback_rows':unknown_fallback,'private_suffix_rows':private_count,'normalization':'hostname rstrip dot then IDNA ASCII; top_domain_under_public_suffix or full host'},'warnings_and_errors_in_notebook':messages,'historical_membership':'unavailable; no claim of row-wise historical identity','internal_shape':list(internal.shape),'artifact_checksums':checksums}
(run/'validation_results.json').write_text(json.dumps(report,indent=2,default=int),encoding='utf-8')
m['validation_status']='PASS' if all(x['status']=='PASS' for x in findings) else 'FAIL'; m['validation_completed_at']=datetime.now(ZoneInfo('Asia/Bangkok')).isoformat(); m['historical_integrity']={'files_checked':len(before),'changed':changed}; m['internal_feature_sha256']=checksums['hasil/fitur_internal.csv.gz']; m['validation_files']=['validation_results.json','comparison.csv','split_membership.csv.gz','artifact_checksums.json']; (run/'run_manifest.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
lines=['# Reproduction Report - '+run.name,'','Tanggal: '+m['validation_completed_at']+'. Reproduksi konfigurasi historis saja; persetujuan final baseline tetap menunggu tim. Notebook kedua dan training tidak dijalankan.','','## Isolasi dan input','','Working directory kernel diverifikasi melalui preflight: `'+m['kernel_preflight']['cwd']+'`. Output `'+m['output_directory']+'` awalnya kosong. Input notebook dan dataset disalin byte-identik; checksum sebelum eksekusi tersimpan pada run_manifest.json. Salinan notebook asli dipertahankan; hasil eksekusi disimpan terpisah sebagai 01_Audit_dan_Split.executed.ipynb. Tidak ada hasil historis dipakai sebagai input eksekusi. Hasil historis hanya dibaca sesudahnya untuk pembandingan.','','Branch '+m['branch']+', commit '+m['commit']+'. Interpreter `'+m['executable']+'`, Python '+m['python']+'. Paket: '+json.dumps(m['packages'])+'. OS '+m['os']+'; CPU '+m['cpu']+'; RAM '+str(m['ram_bytes'])+' byte. Seed 42.','','## Hasil setiap cell','','| Cell | Jenis | Status | Detik | Execution count |','|---|---|---|---|---|']
for c in m['cells']: lines.append('| '+str(c['cell'])+' | '+c['type']+' | '+c['status']+' | '+str(c.get('seconds','-'))+' | '+str(c.get('execution_count','-'))+' |')
lines+=['','Kernel bersih menjalankan preflight sebelum cell penelitian. Karena preflight memakai satu execution count, cell kode pertama dapat bernomor 2. Isi source cell tidak diubah; Markdown dipertahankan.','','## Perbandingan hasil historis dan reproduksi','','| Aspek diuji | Historis | Reproduksi | Selisih | Status | Keterangan |','|---|---|---|---|---|---|']
for c in comparisons: lines.append('| '+' | '.join(str(c[k]) for k in ['aspect','historical','reproduction','difference','status','notes'])+' |')
lines+=['','## Validasi independen','','Pemeriksaan berjalan dalam proses host terpisah dari kernel, membaca kembali CSV dan fitur internal; tidak memakai variabel atau fungsi notebook yang sedang dieksekusi. Rumus leksikal dan aturan domain diterapkan ulang sesuai definisi historis; ini validasi implementasi, bukan metode penelitian baru. Membership disimpan per URL unik menggunakan ID record sumber dan SHA-256 URL. Tidak ada URL mentah dalam laporan atau membership.','','| Pemeriksaan | Status | Bukti/rincian |','|---|---|---|']
for c in findings: lines.append('| '+c['check']+' | '+c['status']+' | '+str(c['details'])+' |')
lines+=['','Definisi domain: tldextract '+manifest['paket']['tldextract']+', snapshot PSL bawaan, private suffix aktif, tanpa pembaruan jaringan, cache_dir=None; hostname dibuang titik akhirnya lalu IDNA ASCII. IP memakai host utuh; suffix tak dikenal juga fallback host. Hitungan fallback/private: '+json.dumps(report['domain_definition'])+'.','','A/B memakai satu kolom acak pada artefak baru dan konfigurasi N2 cell 6; membership identik secara desain untuk run baru. N2 tidak dieksekusi. Tidak ada artefak keanggotaan historis per baris, sehingga kesamaan historis per baris tetap belum dapat diverifikasi meskipun seluruh statistik agregat cocok.','','## Missing values, fitur, dan label','','Pandas default NA pada seluruh 56 kolom: '+json.dumps(missing_default)+'. Pembacaan literal keep_default_na=False pada Title/TLD menemukan string kosong: '+json.dumps(missing_literal)+'. Perbedaan parser missing bukan bukti hilangnya data baru; makna semantik token belum terverifikasi. Model input terpilih, target dan penanda split diperiksa tidak missing. Label positif diturunkan dari label asli 0. Fitur internal berukuran '+str(internal.shape[0])+' baris x '+str(internal.shape[1])+' kolom: target, 23 halaman, struktur, 15 leksikal, dan dua penanda split. Domain tidak disimpan dalam cache historis; untuk validasi domain direkonstruksi dan hanya hash-nya disimpan.','','SHA-256 fitur internal: `'+checksums['hasil/fitur_internal.csv.gz']+'`. Seluruh 15 fitur dibandingkan pada semua URL unik; seluruh 23 atribut halaman dibandingkan dengan record deduplikasi. Cache gzip berhasil dibaca. Tidak ada cache fitur historis untuk perbandingan byte; gzip dapat mengandung timestamp sehingga checksum gzip bukan bukti kesetaraan konten lintas run.','','## Error, warning, dan perbedaan','','Error cell: '+str(sum(o['output_type']=='error' for c in executed['cells'] for o in c.get('outputs',[])))+'. Stream notebook tersimpan: '+json.dumps(messages)+'. Kernel launcher memberi warning TCP tanpa enkripsi pada proses lokal; kernel dimatikan setelah eksekusi. Tidak ada URL dataset dikunjungi. Git tetap memberi warning global ignore tidak dapat diakses. Python berubah dari 3.14.4 historis ke '+m['python']+'; paket audit tercatat sama. Perbedaan metadata environment tidak dipaksa hilang.','','## Perlindungan historis','','Checksum sebelum/sesudah pada '+str(len(before))+' file lama: '+('semua sama' if not changed else 'BERUBAH: '+str(changed))+'. Cakupan termasuk dataset asli, kedua notebook asli, seluruh hasil/ historis, requirements dan dokumentasi audit yang sudah ada. Bukti: historical_integrity_before.json dan historical_integrity_after.json. Tidak ada commit/push/reset atau perubahan source.','','## Artefak baru','','Daftar file run pada saat laporan disusun:']
for p in sorted(run.rglob('*')):
 if p.is_file(): lines.append('- `'+str(p.relative_to(run))+'`')
lines+=['- `REPRODUCTION_REPORT.md` (laporan ini).','','Output notebook: hasil/manifest_data.json, hasil/audit_struktur_mentah.csv, hasil/ringkasan_split.csv, hasil/irisan_domain.csv, hasil/distribusi_struktur_split.csv dan hasil/fitur_internal.csv.gz. Checksum artefak tercatat di artifact_checksums.json. comparison.csv menyimpan tabel pembandingan terstruktur; validation_results.json menyimpan seluruh pemeriksaan. Orkestrator lokal scripts/reproduce.py dan scripts/validate_cache.py diabaikan Git.','','## Kesiapan notebook kedua dan satu pekerjaan berikutnya','','Prasyarat data N2 siap jika seluruh validasi PASS: cache, manifest dan fitur baru berada dalam direktori run yang sama, dan interpreter .venv sudah teruji. Belum ada training atau metrik reproduksi baru. Baseline tetap menunggu persetujuan tim. N2 historis cell 6 masih menjalankan pembobotan tambahan dan evaluate pada cell 4 menghitung subgroup; menjalankan seluruh notebook akan melampaui enam eksperimen utama. Jangan menjalankan N2 sebelum cakupan berikutnya disetujui.','','Satu pekerjaan berikutnya: review hasil reproduksi bersama tim dan sepakati cakupan eksekusi enam eksperimen utama serta baseline selected features, termasuk perlakuan terhadap alur pembobotan tambahan pada salinan notebook. Selanjutnya baru otorisasi eksekusi eksperimen pada output run terisolasi.']
(run/'REPRODUCTION_REPORT.md').write_text(chr(10).join(lines)+chr(10),encoding='utf-8')
print('RUN',run.name,'VALIDATION',m['validation_status'],'CACHE_SHA',m['internal_feature_sha256'],flush=True)
print('MISSING',missing_default,'DOMAIN',report['domain_definition'],flush=True)
