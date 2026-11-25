"""Generate publication assets from frozen results. No training or URL access.
Run with project .venv Python; cwd is arbitrary. Use --overwrite only for this asset directory.
"""
import argparse,hashlib,json,platform,sys,os,xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
OUT=Path(__file__).resolve().parents[1];RUN=OUT.parent;ROOT=RUN.parent.parent
os.environ['MPLCONFIGDIR']=str(OUT/'source'/'mpl_cache')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
from PIL import Image,ImageDraw
from sklearn.metrics import roc_curve,roc_auc_score
from importlib.metadata import version
parser=argparse.ArgumentParser();parser.add_argument('--overwrite',action='store_true');args=parser.parse_args()
if (OUT/'asset_manifest.json').exists() and not args.overwrite:raise SystemExit('Assets exist; use --overwrite explicitly to regenerate only publication_assets')
if not (RUN/'eksperimen_utama/predictions/LR_A_uji.csv.gz').is_file():raise SystemExit('Publication snapshot omits record predictions. Generate a local run explicitly, then use scripts/reproduce.py figures --run runs/<run-id>. No training is automatic.')
for name in ['figures','tables','source']: (OUT/name).mkdir(parents=True,exist_ok=True)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return pd.read_csv(p,float_precision='round_trip')
def md(name,lines):(OUT/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
protected={str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file() and not any(x in p.relative_to(ROOT).parts for x in ('.git','.venv','publication_assets'))}
checks=[]
for name,h in json.loads((RUN/'analysis/validation_manifest.json').read_text())['output_checksums'].items():assert sha(RUN/'analysis'/name)==h,name
for name,h in json.loads((RUN/'eksperimen_utama/artifact_checksums.json').read_text()).items():assert sha(RUN/name)==h,name
for name,h in json.loads((RUN/'artifact_checksums.json').read_text()).items():assert sha(RUN/name)==h,name
M=read(RUN/'eksperimen_utama/metrik_utama.csv');P=read(RUN/'analysis/performance_comparison.csv');D=read(RUN/'analysis/scenario_deltas.csv');E=read(RUN/'analysis/error_analysis.csv');TIME=read(RUN/'analysis/efficiency_analysis.csv')
S=read(RUN/'hasil/ringkasan_split.csv');O=read(RUN/'hasil/irisan_domain.csv');U=read(RUN/'hasil/audit_struktur_mentah.csv');H=read(RUN/'eksperimen_utama/historical_comparison_full.csv');MEM=read(RUN/'split_membership.csv.gz')
manifest=json.loads((RUN/'eksperimen_utama/manifest_eksperimen.json').read_text());data_manifest=json.loads((RUN/'hasil/manifest_data.json').read_text());params=json.loads((RUN/'eksperimen_utama/actual_parameters.json').read_text())
for c in M.columns:assert M[c].equals(P[c]),c
assert len(M)==6 and all(read(RUN/'eksperimen_utama'/f).status.eq('PASS').all() for f in ['independent_metric_validation.csv','independent_host_validation.csv'])
assert np.array_equal(E.loc[E.partition=='uji','total_errors'],M.uji_fp+M.uji_fn)
for row in D.to_dict('records'):
    g=M.loc[M.model==row['model']].set_index('skenario')
    for metric in ['f1','recall','precision','fpr','roc_auc']:
        assert abs(100*(g.loc[row['later'],'uji_'+metric]-g.loc[row['earlier'],'uji_'+metric])-row['delta_'+metric+'_pp'])<1e-12
predictions={}
for r in M.to_dict('records'):
    key=(r['model'],r['skenario']);p=read(RUN/'eksperimen_utama/predictions'/f'{key[0]}_{key[1]}_uji.csv.gz');predictions[key]=p
    assert abs(roc_auc_score(p.phishing,p.probability_phishing)-r['uji_roc_auc'])<1e-12
    assert np.array_equal(p.prediction,p.probability_phishing>=r['ambang'])
    part=MEM.loc[MEM['domain' if key[1]=='C' else 'acak']=='uji'];assert p.url_sha256.equals(part.url_sha256.reset_index(drop=True))
assert H.loc[H.metric!='uji_batch_ms','absolute_difference'].max()==0
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.labelsize':10,'axes.titlesize':11,'legend.fontsize':9,'xtick.labelsize':9,'ytick.labelsize':9,'figure.facecolor':'white','axes.facecolor':'white','savefig.facecolor':'white','svg.fonttype':'none','axes.spines.top':False,'axes.spines.right':False,'axes.unicode_minus':True})
COL={'LR':'#0072B2','RF':'#D55E00'};SCENARIOS=['A','B','C'];figures=[];tables=[]
SOURCE_METRICS='eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv'
def save(fig,name,caption,unit,sources,section='Results',limitation='Satu dataset dan seed; tanpa interval ketidakpastian.'):
    for fmt in ['png','svg']:fig.savefig(OUT/'figures'/f'{name}.{fmt}',dpi=300,bbox_inches='tight',pad_inches=.15)
    plt.close(fig);figures.append(dict(id=name,caption=caption,unit=unit,sources=sources,section=section,limitation=limitation))
def axis_style(ax):ax.grid(axis='y',color='#dddddd',linewidth=.6);ax.set_axisbelow(True)
def box(ax,x,y,w,h,text,fc='#F2F4F6',ec='#52616B',fs=10):
    ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle='round,pad=0.012',facecolor=fc,edgecolor=ec,linewidth=1));ax.text(x,y,text,ha='center',va='center',fontsize=fs)
def arrow(ax,a,b):ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'->','color':'#53616B','lw':1.1,'shrinkA':2,'shrinkB':2})
# Methodology: deterministic extraction before split; learned preprocessing fits only train.
fig,ax=plt.subplots(figsize=(12,9));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
box(ax,.16,.92,.27,.09,'PhiUSIIL\n235.795 baris; 56 kolom');box(ax,.50,.92,.23,.09,'Audit data\nlabel, duplikat, konflik');box(ax,.83,.92,.25,.09,'Deduplikasi URL\n235.370 baris')
arrow(ax,(.30,.92),(.37,.92));arrow(ax,(.63,.92),(.69,.92))
box(ax,.28,.73,.32,.10,'Ekstraksi 15 fitur leksikal\ndari teks URL');box(ax,.72,.73,.32,.10,'Seleksi 23 atribut halaman\ndari CSV')
arrow(ax,(.83,.86),(.28,.80));arrow(ax,(.83,.86),(.72,.80))
box(ax,.30,.55,.38,.10,'Split acak terstratifikasi\ntrain / validation / test');box(ax,.76,.55,.34,.10,'Split domain terdaftar\ntrain / validation / test')
arrow(ax,(.28,.67),(.25,.61));arrow(ax,(.72,.67),(.35,.61));arrow(ax,(.37,.68),(.76,.61))
box(ax,.18,.38,.23,.09,'A: 38 fitur terpilih');box(ax,.44,.38,.23,.09,'B: 15 leksikal');box(ax,.76,.38,.25,.09,'C: 15 leksikal')
arrow(ax,(.25,.49),(.18,.44));arrow(ax,(.34,.49),(.44,.44));arrow(ax,(.76,.49),(.76,.44))
box(ax,.5,.23,.77,.10,'LR dan RF untuk A/B/C (seed 42)\nFit imputasi, standardisasi LR, dan model HANYA pada train')
for x in [.18,.44,.76]:arrow(ax,(x,.32),(x,.29))
box(ax,.17,.075,.28,.10,'Threshold: F1 validation\nmaksimum + tie-break');box(ax,.5,.075,.27,.10,'Evaluasi test\nthreshold dibekukan');box(ax,.83,.075,.27,.10,'Analisis hasil\ndan reproduksibilitas')
arrow(ax,(.27,.17),(.17,.14));arrow(ax,(.32,.075),(.35,.075));arrow(ax,(.65,.075),(.68,.075))
save(fig,'fig_01_methodology_flow','Alur metodologi konfigurasi historis P1. Ekstraksi leksikal deterministik mendahului split; seluruh praproses yang memerlukan fit hanya menggunakan train. Validation memilih ambang dan test mengevaluasi ambang beku.','Baris, kolom, jumlah fitur','hasil/manifest_data.json; 01_Audit_dan_Split.ipynb cell 2/4/6; 02_Eksperimen_Utama.ipynb cell 3–6','Methods','Diagram mendeskripsikan konfigurasi yang direproduksi; persetujuan baseline tim masih menunggu.')
fig,ax=plt.subplots(figsize=(11,5));ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
for x,title,text in [(.17,'A','38 fitur terpilih\n15 leksikal + 23 halaman\nSplit acak terstratifikasi'),(.5,'B','15 fitur leksikal\nSplit acak identik dengan A'),(.83,'C','15 fitur leksikal identik B\nSplit domain terdaftar')]:
    box(ax,x,.7,.27,.35,title+'\n\n'+text,fs=10)
arrow(ax,(.2,.43),(.47,.43));ax.text(.335,.36,'B − A: cakupan fitur',ha='center',fontsize=10)
arrow(ax,(.53,.43),(.80,.43));ax.text(.665,.36,'C − B: protokol split',ha='center',fontsize=10)
ax.text(.5,.20,'A/B: membership train, validation, test sama',ha='center');ax.text(.5,.10,'B/C: fitur sama; membership dan komposisi test berbeda',ha='center')
save(fig,'fig_02_experimental_scenarios','Tiga skenario eksperimen dengan selected features. B − A mengubah cakupan fitur; C − B mengubah protokol serta keanggotaan data, dengan fitur leksikal tetap.','Jumlah fitur','analysis/performance_comparison.csv; eksperimen_utama/actual_parameters.json','Methods','A bukan seluruh fitur PhiUSIIL; C − B bukan efek kausal domain yang terisolasi.')
def metric_plot(field,label,name,ylim,zoom):
    fig,ax=plt.subplots(figsize=(6.5,4.2));x=np.arange(3)
    for model,offset in [('LR',-.07),('RF',.07)]:
        vals=M.loc[M.model==model].set_index('skenario').loc[SCENARIOS,'uji_'+field].to_numpy()*100
        ax.scatter(x+offset,vals,c=COL[model],label=model,s=48,marker='o' if model=='LR' else 's',zorder=3)
        for xx,v in zip(x+offset,vals):ax.annotate(f'{v:.4f}',(xx,v),xytext=(-8,-17) if model=='LR' else (9,9),textcoords='offset points',ha='center',fontsize=8)
    ax.set(xticks=x,xticklabels=SCENARIOS,xlabel='Skenario',ylabel=label+' test (%)',ylim=ylim,xlim=(-.35,2.35));axis_style(ax)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,1.16),ncol=2,frameon=False);fig.tight_layout()
    save(fig,name,f'Perbandingan {label} test LR dan RF pada A/B/C. '+zoom,'Persen (%)',SOURCE_METRICS,limitation='Point plot tanpa error bar. B/C memakai test berbeda; satu seed.')
metric_plot('f1','F1','fig_03_f1_comparison',(99.0,100.08),'Sumbu Y diperbesar ke 99,0–100,08%; tidak dimulai dari nol.')
metric_plot('recall','Recall phishing','fig_04_recall_comparison',(98.0,100.08),'Sumbu Y diperbesar ke 98,0–100,08%; tidak dimulai dari nol.')
metric_plot('fpr','FPR','fig_05_fpr_comparison',(0,.085),'FPR ditampilkan pada panel terpisah dengan sumbu Y mulai nol.')
fig,axs=plt.subplots(1,3,figsize=(12,4.1))
for ax,field,title in zip(axs,['f1','recall','fpr'],['ΔF1','ΔRecall','ΔFPR']):
    for model,offset in [('LR',-.07),('RF',.07)]:
        vals=D.loc[D.model==model,'delta_'+field+'_pp'].to_numpy();xx=np.arange(2)+offset
        ax.scatter(xx,vals,color=COL[model],label=model,s=45,marker='o' if model=='LR' else 's',zorder=3)
        for x,y in zip(xx,vals):ax.annotate(f'{y:+.4f}',(x,y),textcoords='offset points',xytext=(-5,-17) if model=='LR' else (6,9),ha='center',fontsize=8)
    ax.axhline(0,color='black',lw=.8);ax.set(xticks=[0,1],xticklabels=['B − A','C − B'],xlim=(-.35,1.35),ylabel=title+' (poin persentase)');ax.margins(y=.28);axis_style(ax)
fig.legend(*axs[0].get_legend_handles_labels(),loc='upper center',bbox_to_anchor=(.5,1.0),ncol=2,frameon=False);fig.subplots_adjust(left=.08,right=.98,bottom=.17,top=.85,wspace=.38)
save(fig,'fig_06_scenario_deltas','Perubahan F1, recall dan FPR: B dikurangi A serta C dikurangi B. Tanda menunjukkan arah perubahan terhadap skenario awal; garis horizontal menandai nol.','Poin persentase (pp)','analysis/scenario_deltas.csv',limitation='pp bukan perubahan relatif persen. B/C berbeda dalam komposisi dan membership test; tidak ada klaim kausal atau signifikansi.')
def matrices(normalized):
    fig,axs=plt.subplots(2,3,figsize=(11.5,7.1),layout='constrained');images=[]
    for i,model in enumerate(['LR','RF']):
        for j,scenario in enumerate(SCENARIOS):
            r=M.loc[(M.model==model)&(M.skenario==scenario)].iloc[0];cm=np.array([[r.uji_tn,r.uji_fp],[r.uji_fn,r.uji_tp]],dtype=float);values=100*cm/cm.sum(axis=1,keepdims=True) if normalized else cm
            ax=axs[i,j];im=ax.imshow(values,cmap='Blues',vmin=0,vmax=100 if normalized else 20500);images.append(im)
            for row in range(2):
                for col in range(2):ax.text(col,row,f'{values[row,col]:.4f}%' if normalized else f'{int(values[row,col]):,}'.replace(',','.'),ha='center',va='center',fontsize=11,color='white' if values[row,col]>(50 if normalized else 10250) else 'black')
            ax.set(xticks=[0,1],xticklabels=['Legitimate (0)','Phishing (1)'],yticks=[0,1],yticklabels=['Legitimate (0)','Phishing (1)'],xlabel='Kelas prediksi',ylabel='Kelas aktual')
            ax.set_title(f'{model}/{scenario}\nN₀={int(r.uji_sah):,}; N₁={int(r.uji_phishing):,}'.replace(',','.'),color=COL[model],fontsize=10)
    fig.colorbar(images[0],ax=axs.ravel().tolist(),shrink=.85,label='Persentase dalam kelas aktual (%)' if normalized else 'Jumlah record')
    save(fig,'fig_07b_confusion_matrix_normalized' if normalized else 'fig_07a_confusion_matrix_counts','Confusion matrix enam konfigurasi test; baris adalah kelas aktual, kolom kelas prediksi. '+('Normalisasi per baris menggunakan denominator kelas aktual; rentang warna bersama 0–100%.' if normalized else 'Count aktual ditulis pada setiap sel; rentang warna bersama 0–20.500 record.'),'Persen kelas aktual (%)' if normalized else 'Jumlah record',SOURCE_METRICS+'; analysis/error_analysis.csv',limitation='N₀ legitimate dan N₁ phishing tercantum per panel. Nol FP tidak membuktikan FPR populasi nol; test C berbeda dari A/B.')
matrices(False);matrices(True)
def time_plot(field,ylabel,name):
    fig,ax=plt.subplots(figsize=(6.7,4.2));x=np.arange(3)
    for model,offset in [('LR',-.18),('RF',.18)]:
        vals=M.loc[M.model==model].set_index('skenario').loc[SCENARIOS,field].to_numpy();bars=ax.bar(x+offset,vals,width=.34,color=COL[model],label=model);ax.bar_label(bars,fmt='%.3f',padding=4,fontsize=8)
    ax.set(xticks=x,xticklabels=SCENARIOS,xlabel='Skenario',ylabel=ylabel,ylim=(0,M[field].max()*1.22));axis_style(ax);ax.legend(loc='upper right',frameon=False);fig.tight_layout()
    save(fig,name,'Waktu '+('training pipeline.fit' if field=='training_seconds' else 'inferensi pipeline')+' per konfigurasi pada perangkat reproduksi yang sama.','Detik' if field=='training_seconds' else 'ms per 1.024 sampel','analysis/efficiency_analysis.csv; '+SOURCE_METRICS,limitation='Satu run/perangkat. Inferensi median5 setelah warm-up1, thread1; ekstraksi URL dan pengambilan halaman tidak tercakup. Bukan end-to-end.')
time_plot('training_seconds','Waktu training (detik)','fig_08a_training_time');time_plot('uji_batch_ms','Waktu inferensi (ms / 1.024 sampel)','fig_08b_inference_time')
fig,ax=plt.subplots(figsize=(7.2,4.7))
for model in ['LR','RF']:
    group=M.loc[M.model==model];ax.scatter(group.uji_batch_ms,100*group.uji_f1,c=COL[model],s=55,label=model,marker='o' if model=='LR' else 's')
    for r in group.itertuples():ax.annotate(f'{model}/{r.skenario}',(r.uji_batch_ms,100*r.uji_f1),xytext=(7,8),textcoords='offset points',fontsize=9)
ax.set(xlabel='Waktu inferensi (ms / 1.024 sampel)',ylabel='F1 test (%)',ylim=(99.0,100.12),xlim=(1.8,12));axis_style(ax);ax.legend(loc='lower right',frameon=False);fig.tight_layout()
save(fig,'fig_09_f1_efficiency_tradeoff','Hubungan deskriptif antara F1 test dan waktu inferensi enam konfigurasi. Sumbu Y diperbesar ke 99,0–100,12%.','F1 persen (%); inferensi ms / 1.024 sampel',SOURCE_METRICS+'; analysis/efficiency_analysis.csv',limitation='Satu perangkat/run; bukan end-to-end. Tidak ada garis frontier atau klaim model terbaik universal; test C berbeda.')
fig,ax=plt.subplots(figsize=(7.2,4.7));x=np.arange(3)
for field,offset,color,label in [('sah',-.18,'#009E73','Legitimate (0)'),('phishing',.18,'#CC79A7','Phishing (1)')]:
    bars=ax.bar(x+offset,U[field],width=.34,color=color,label=label)
    ax.bar_label(bars,labels=[f'{int(v):,}'.replace(',','.') for v in U[field]],padding=4,fontsize=9)
ax.set(xticks=x,xticklabels=['Akar','Path','Query'],xlabel='Struktur URL mentah',ylabel='Jumlah record',ylim=(0,160000));axis_style(ax);ax.legend(frameon=False,loc='upper right');fig.tight_layout()
save(fig,'fig_10_url_structure_distribution','Distribusi struktur URL sebelum deduplikasi. Seluruh 134.850 legitimate berada pada akar; kelompok path/query hanya berisi phishing pada salinan ini.','Jumlah record mentah','hasil/audit_struktur_mentah.csv','Discussion','Ketimpangan struktur menunjukkan potensi shortcut dataset, bukan leakage terkonfirmasi.')
fig,ax=plt.subplots(figsize=(7.2,4.5));x=np.arange(3)
for split,offset,color,label in [('acak',-.18,'#6F6F6F','Acak'),('domain',.18,'#CC79A7','Domain terdaftar')]:
    vals=O.loc[O.split==split,'domain_irisan'].to_numpy();bars=ax.bar(x+offset,vals,width=.34,color=color,label=label);ax.bar_label(bars,padding=4,fontsize=9)
ax.set(xticks=x,xticklabels=['Train–validation','Train–test','Validation–test'],ylabel='Jumlah domain beririsan',ylim=(0,3100));axis_style(ax);ax.legend(frameon=False,loc='upper right');fig.tight_layout()
save(fig,'fig_11_domain_overlap','Jumlah irisan domain terdaftar pada tiga pasangan bagian. Split C memiliki nol irisan pada seluruh pasangan; split acak memiliki irisan nonnol.','Jumlah domain','hasil/irisan_domain.csv','Results','Domain mengikuti tldextract5.3.1, private suffix aktif, fallback host untuk IP/suffix tak dikenal. Nol irisan tidak membuktikan generalisasi lintas korpus.')
fig,axs=plt.subplots(1,3,figsize=(12,4.1),layout='constrained')
roc_validation=[]
for ax,scenario in zip(axs,SCENARIOS):
    for model in ['LR','RF']:
        p=predictions[(model,scenario)];fpr,tpr,_=roc_curve(p.phishing,p.probability_phishing);auc=roc_auc_score(p.phishing,p.probability_phishing)
        ax.plot(100*fpr,100*tpr,color=COL[model],lw=1.4,linestyle='-' if model=='LR' else '--',label=f'{model}; AUC={auc:.6f}');roc_validation.append(dict(model=model,scenario=scenario,auc=auc))
    ax.plot([0,100],[0,100],color='#aaaaaa',lw=.7,linestyle=':');ax.set(xlim=(0,100),ylim=(0,101),xlabel='FPR (%)',ylabel='Recall phishing / TPR (%)',title=f'Skenario {scenario}');ax.legend(loc='lower right',fontsize=8,frameon=False);ax.grid(color='#eeeeee',lw=.5)
save(fig,'fig_12_roc_curves','Kurva ROC test dari probabilitas aktual per record, dipisah menurut A/B/C. Garis LR/RF dapat bertumpuk karena AUC mendekati satu; sumbu penuh 0–100% dipertahankan.','FPR dan TPR persen (%); AUC proporsi 0–1','eksperimen_utama/predictions/*_uji.csv.gz; '+SOURCE_METRICS,limitation='C memiliki membership test berbeda. Kurva bukan rekonstruksi dari satu nilai AUC; tidak ada interval ketidakpastian.')
# CSV retains full numerical precision; Markdown rounds only for display.
def table_asset(frame,name,caption,unit,sources,section='Results',limitation='Satu dataset/seed; interpretasi deskriptif.'):
    frame.to_csv(OUT/'tables'/f'{name}.csv',index=False)
    lines=['| '+' | '.join(frame.columns)+' |','|'+'|'.join(['---']*len(frame.columns))+'|']
    for row in frame.itertuples(index=False,name=None):lines.append('| '+' | '.join(('Tidak tersedia' if pd.isna(v) else f'{v:.6f}') if isinstance(v,float) else str(v) for v in row)+' |')
    (OUT/'tables'/f'{name}.md').write_text('\n'.join(lines)+'\n',encoding='utf-8');tables.append(dict(id=name,caption=caption,unit=unit,sources=sources,section=section,limitation=limitation))
audit=data_manifest['audit'];dataset=pd.DataFrame([('Baris mentah',audit['baris_mentah']),('Kolom asli',56),('Phishing mentah',int(U.phishing.sum())),('Legitimate mentah',int(U.sah.sum())),('URL unik',audit['url_unik']),('Pengulangan URL',audit['duplikat_tambahan']),('URL konflik label',audit['url_konflik_label']),('Baris bersih',audit['baris_bersih']),('Phishing bersih',100520),('Legitimate bersih',134850)],columns=['Aspek','Jumlah'])
table_asset(dataset,'table_01_dataset_summary','Ringkasan audit dataset mentah dan setelah deduplikasi.','Jumlah record/kolom/URL','hasil/manifest_data.json; hasil/audit_struktur_mentah.csv','Methods','Label asli0 phishing,1 legitimate; target model membalik phishing menjadi1. Provenance versi Kaggle belum lengkap.')
sc=pd.DataFrame([('A',38,'15 leksikal + 23 halaman terpilih','Acak terstratifikasi','Sama dengan B'),('B',15,'Leksikal URL','Acak terstratifikasi','Sama dengan A'),('C',15,'Leksikal identik B','Domain terdaftar','Berbeda dari A/B')],columns=['Skenario','Jumlah fitur','Cakupan','Protokol split','Membership'])
table_asset(sc,'table_02_experimental_scenarios','Definisi skenario historis yang direproduksi.','Jumlah fitur','eksperimen_utama/actual_parameters.json; analysis/performance_comparison.csv','Methods','A adalah selected features; persetujuan final baseline tim masih menunggu.')
split_table=S.rename(columns={'split':'Protokol','bagian':'Bagian','baris':'Jumlah record','sah':'Legitimate','phishing':'Phishing','domain_unik':'Domain unik'}).copy();split_table['Rasio record (%)']=100*split_table.pop('proporsi')
table_asset(split_table,'table_03_split_distribution','Ukuran, distribusi kelas dan domain unik setiap bagian.','Record, domain, persen (%)','hasil/ringkasan_split.csv','Methods','Target70/15/15; rasio domain-grouped diarahkan pada kelompok domain sehingga rasio baris berbeda.')
ov=O.copy();ov['Baris bagian kedua dalam irisan (%)']=100*ov.pop('proporsi_baris_bagian_2');ov=ov.rename(columns={'split':'Protokol','bagian_1':'Bagian pertama','bagian_2':'Bagian kedua','domain_irisan':'Domain beririsan'})
table_asset(ov,'table_04_domain_overlap','Irisan domain antarbagiannya dan proporsi record bagian kedua yang domainnya termasuk irisan.','Jumlah domain; persen (%)','hasil/irisan_domain.csv','Results','Proporsi bukan persentase domain. Private suffix dan fallback mengikuti implementasi historis.')
param_rows=[]
for model in ['LR','RF']:
    p=params[f'{model}/A']['pipeline'];last=p['logisticregression' if model=='LR' else 'randomforestclassifier']
    for key,val in last.items():param_rows.append(dict(Model=model,Komponen='Estimator (A/B/C)',Parameter=key,Nilai=str(val)))
    param_rows.append(dict(Model=model,Komponen='Pipeline',Parameter='Praproses',Nilai='Imputasi median; StandardScaler' if model=='LR' else 'Imputasi median'))
param_rows.extend([dict(Model='LR/RF',Komponen='Evaluasi',Parameter='Threshold',Nilai='F1 validation maksimum; tie FPR rendah lalu threshold tinggi'),dict(Model='LR/RF',Komponen='Inferensi',Parameter='Pengukuran',Nilai='Batch1024; warm-up1; median5; thread1')])
table_asset(pd.DataFrame(param_rows),'table_05_model_parameters','Parameter estimator aktual dan aturan pipeline/evaluasi.','Nilai parameter; batch dan pengulangan','eksperimen_utama/actual_parameters.json; eksperimen_utama/manifest_eksperimen.json','Methods','Semua parameter default estimator aktual dicatat; fit hanya train, threshold hanya validation.')
perf=M[['model','skenario','uji_samples','ambang','uji_accuracy','uji_precision','uji_recall','uji_f1','uji_roc_auc','uji_fpr']].copy()
for field in ['accuracy','precision','recall','f1','roc_auc','fpr']:perf[field+' (%)']=100*perf.pop('uji_'+field)
perf=perf.rename(columns={'model':'Model','skenario':'Skenario','uji_samples':'N test','ambang':'Ambang'})
perf=perf.rename(columns={'accuracy (%)':'Akurasi (%)','precision (%)':'Precision (%)','recall (%)':'Recall (%)','f1 (%)':'F1 (%)','roc_auc (%)':'ROC-AUC (%)','fpr (%)':'FPR (%)'})
table_asset(perf,'table_06_test_performance','Performa test enam konfigurasi. CSV memakai presisi penuh; Markdown enam angka desimal pada persen.','Metrik persen (%); threshold proporsi',SOURCE_METRICS,'Results','Nol FP/FPR sampel tidak membuktikan FPR populasi nol; test C berbeda.')
delta_table=D[['model','direction','delta_f1_pp','delta_recall_pp','delta_precision_pp','delta_fpr_pp','delta_roc_auc_pp','delta_fp_count','delta_fn_count','delta_training_seconds','delta_inference_ms_per_1024']].copy()
delta_table=delta_table.rename(columns={'model':'Model','direction':'Arah selisih','delta_f1_pp':'Delta F1 (pp)','delta_recall_pp':'Delta Recall (pp)','delta_precision_pp':'Delta Precision (pp)','delta_fpr_pp':'Delta FPR (pp)','delta_roc_auc_pp':'Delta ROC-AUC (pp)','delta_fp_count':'Delta FP (record)','delta_fn_count':'Delta FN (record)','delta_training_seconds':'Delta Training (detik)','delta_inference_ms_per_1024':'Delta Inferensi (ms/1024)'})
table_asset(delta_table,'table_07_scenario_deltas','Selisih B minus A dan C minus B dengan arah dan satuan eksplisit pada nama kolom.','pp untuk metrik; record untuk FP/FN; detik training; ms/1024 inferensi','analysis/scenario_deltas.csv','Results','pp bukan persen relatif. C/B berbeda dalam membership dan komposisi test; tidak ada klaim kausal.')
cm_table=M[['model','skenario','uji_samples','uji_sah','uji_phishing','uji_tn','uji_fp','uji_fn','uji_tp']].rename(columns={'model':'Model','skenario':'Skenario','uji_samples':'N test','uji_sah':'N legitimate','uji_phishing':'N phishing','uji_tn':'TN','uji_fp':'FP','uji_fn':'FN','uji_tp':'TP'})
table_asset(cm_table,'table_08_confusion_matrix','Confusion counts test dan denominator setiap kelas.','Jumlah record',SOURCE_METRICS+'; analysis/error_analysis.csv','Results','Counts B/C tidak dibandingkan tanpa denominator. Nol FP bukan jaminan populasi.')
eff=TIME[['model','skenario','training_seconds','uji_batch_ms','RF_over_LR_training_ratio','RF_over_LR_inference_ratio']].rename(columns={'model':'Model','skenario':'Skenario','training_seconds':'Training (detik)','uji_batch_ms':'Inferensi (ms/1024)','RF_over_LR_training_ratio':'Rasio training RF/LR','RF_over_LR_inference_ratio':'Rasio inferensi RF/LR'})
table_asset(eff,'table_09_computational_efficiency','Waktu training dan inferensi aktual serta rasio RF terhadap LR pada skenario sama.','Detik; ms/1024; rasio','analysis/efficiency_analysis.csv','Results','Satu perangkat/run, bukan end-to-end; rasio sama diulang pada kedua model untuk konteks.')
repro=[]
for metric,g in H.groupby('metric',sort=False):repro.append({'Aspek':metric,'Selisih absolut maksimum':g.absolute_difference.max(),'Status':'Sama agregat' if g.absolute_difference.max()==0 else 'Berbeda (timing)','Batas':'Per-record historis belum tersedia' if metric!='uji_batch_ms' else 'Perangkat/load berbeda; ms/1024'})
repro.extend([{'Aspek':'Prediksi historis per record','Selisih absolut maksimum':np.nan,'Status':'Belum dapat diverifikasi','Batas':'Artefak historis tidak tersedia'},{'Aspek':'Python','Selisih absolut maksimum':np.nan,'Status':'Historis3.14.4; reproduksi3.13.0','Batas':'Lima versi paket utama sama; environment tidak identik'}])
table_asset(pd.DataFrame(repro),'table_10_reproducibility','Ringkasan pembandingan presisi penuh dengan hasil historis dan batas bukti per record.','Selisih proporsi/count; timing ms/1024; versi environment','eksperimen_utama/historical_comparison_full.csv; eksperimen_utama/manifest_eksperimen.json','Discussion','Tidak mengklaim reproducibility sempurna; tidak ada training time historis untuk dibandingkan.')
def captions(items,title):
    lines=['# '+title,'']
    for x in items:lines.extend(['## '+x['id'],'',x['caption'],'','Satuan: '+x['unit']+'.','Sumber (relatif run): '+x['sources']+'.','Batas interpretasi: '+x['limitation'],'Rekomendasi bagian: '+x['section']+'.',''])
    return lines
md('FIGURE_CAPTIONS.md',captions(figures,'Caption Gambar Ilmiah'));md('TABLE_CAPTIONS.md',captions(tables,'Caption Tabel Ilmiah'))
# Programmatic export QA; visual review is recorded separately after contact sheets are inspected.
files=[]
for p in sorted((OUT/'figures').glob('*')):
    info={'path':p.relative_to(OUT).as_posix(),'bytes':p.stat().st_size,'format':p.suffix[1:],'sha256':sha(p)}
    if p.suffix=='.png':
        with Image.open(p) as im:im.verify()
        with Image.open(p) as im:info.update(width_px=im.width,height_px=im.height,dpi=list(im.info.get('dpi',[])))
        assert all(abs(d-300)<.1 for d in info['dpi'])
    else:ET.parse(p)
    files.append(info)
# Contact sheets are local QA aids, not publication figures.
pngs=sorted((OUT/'figures').glob('*.png'))
for start in range(0,len(pngs),4):
    sheet=Image.new('RGB',(1700,1300),'white');draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(pngs[start:start+4]):
        im=Image.open(p).convert('RGB');im.thumbnail((825,595));x=(j%2)*850+(850-im.width)//2;y=(j//2)*650+35
        sheet.paste(im,(x,y));draw.text(((j%2)*850+12,(j//2)*650+8),p.stem,fill='black')
    sheet.save(OUT/'source'/f'qa_contact_{start//4+1:02}.png')
after={name:sha(ROOT/name) for name in protected};changed=[name for name in protected if protected[name]!=after[name]];assert not changed,changed
index=['# Indeks Aset Publikasi','','Seluruh aset dihasilkan dari run reproduction-001 tanpa training. Path sumber relatif terhadap run; output relatif terhadap publication_assets.','', '| ID | File | Sumber | Bagian |','|---|---|---|---|']
for item in figures:index.append('| '+item['id']+' | [PNG](figures/'+item['id']+'.png), [SVG](figures/'+item['id']+'.svg) | '+item['sources']+' | '+item['section']+' |')
for item in tables:index.append('| '+item['id']+' | [CSV](tables/'+item['id']+'.csv), [Markdown](tables/'+item['id']+'.md) | '+item['sources']+' | '+item['section']+' |')
md('ASSET_INDEX.md',index)
report=['# Laporan Visualisasi dan Tabel Ilmiah','','Status generator: selesai; validasi numerik dan format lulus. Pemeriksaan visual dicatat sesudah inspeksi ekspor.','',f'Jumlah: {len(figures)} gambar ilmiah, masing-masing PNG300DPI dan SVG ({len(figures)*2} file), serta {len(tables)} tabel dalam CSV/Markdown ({len(tables)*2} file).','', '## Validasi sumber dan desain','','Checksum analysis/Tahap4/Tahap5 lulus; metrik dibandingkan dengan CSV utama; 6 ROC-AUC diperiksa dari probabilitas aktual dan membership test. Data dibaca round_trip, tanpa mengambil nilai tabel yang sudah dibulatkan. Warna LR biru #0072B2 dan RF jingga #D55E00; bentuk marker membedakan model. Background putih, font DejaVu Sans, tanpa3D/error bar. Skala persentase dan pp dipisahkan; count dan rate terpisah. Caption menyebut sumbu F1/recall/trade-off yang diperbesar.','', '## Ekspor dan QA','','Semua PNG dapat dibuka melalui Pillow dan mencatat DPI mendekati300; dimensi piksel per file ada di asset_manifest.json. Semua SVG lolos XML parsing. Confusion matrix berbagi skala warna, normalized per kelas aktual dan denominator dicantumkan. ROC memakai probabilitas aktual, bukan rekonstruksi AUC. Generator source/generate_assets.py dan contact sheets mendukung inspeksi ulang.','', '## Reproduksi','','Working directory bebas: generator menentukan input/output dari lokasi file. Gunakan interpreter project .venv. Dari root repositori:','', '```powershell','.\\.venv\\Scripts\\python.exe runs/reproduction-001/publication_assets/source/generate_assets.py --overwrite','```','','Tanpa --overwrite generator menolak jika manifest aset sudah ada. Flag hanya mengizinkan regenerasi output publication_assets, tidak sumber eksperimen. Dependency aktual: '+json.dumps({p:version(p) for p in ['matplotlib','numpy','pandas','scikit-learn','pillow']})+'. Tidak ada install/training. Semua source/output tercatat di manifest dan ASSET_INDEX.md.','', '## Integritas dan batas klaim','',f'{len(protected)} file sebelumnya diperiksa sebelum/sesudah; berubah: {changed}. Bukti SHA256 tersimpan pada asset_manifest.json. Baseline masih menunggu persetujuan tim. Satu dataset/seed, ketimpangan struktur, test B/C berbeda, provenance belum lengkap, dan timing non-end-to-end membatasi klaim. Tidak ada klaim signifikansi statistik, leakage terkonfirmasi atau FPR populasi nol. Template jurnal belum tersedia; diagram/multipanel cocok dua kolom, point plots/timing dapat memakai satu kolom setelah uji keterbacaan. Ukuran fisik aktual dicatat lewat dimensi pixel/DPI dan source.','', '## Rekomendasi aset utama','','Methods: fig01/fig02 dan table02/table03/table05. Results: fig03/fig04/fig05/fig06, table06/table07/table08. Discussion: fig09/fig10/fig11 dan table10. Confusion matrix, ROC dan timing lengkap dapat menjadi materi pendukung sesuai batas ruang template. Ini rekomendasi aset, bukan naskah artikel.','', '## Inventaris','','ASSET_INDEX.md memetakan seluruh nama file dan sumber. FIGURE_CAPTIONS.md dan TABLE_CAPTIONS.md menyimpan judul, penjelasan, satuan, sumber, batas klaim dan bagian artikel yang disarankan. asset_manifest.json menyimpan format, ukuran, checksum, resolusi, environment dan integritas sumber.']
md('VISUALIZATION_REPORT.md',report)
allfiles=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='asset_manifest.json':
        item=next((i.copy() for i in files if i['path']==p.relative_to(OUT).as_posix()),dict(path=p.relative_to(OUT).as_posix(),bytes=p.stat().st_size,format=p.suffix[1:],sha256=sha(p)))
        stem=p.stem;asset=next((a for a in figures+tables if a['id']==stem),None);item['sources']=asset['sources'] if asset else 'Dokumentasi/generator/QA aset run reproduction-001';allfiles.append(item)
record={'created_at':datetime.now(ZoneInfo('Asia/Bangkok')).isoformat(),'figure_count':len(figures),'table_count':len(tables),'figure_assets':figures,'table_assets':tables,'files':allfiles,'integrity':{'files_checked':len(protected),'changed':changed,'before':protected,'after':after},'validation':{'checksums':'PASS','metrics_and_deltas':'PASS','test_probability_auc':'PASS','png_open_and_300dpi':'PASS','svg_xml':'PASS','visual_review':'PENDING'},'environment':{p:version(p) for p in ['matplotlib','numpy','pandas','scikit-learn','pillow']},'python':platform.python_version(),'baseline_team_approval':'pending'}
(OUT/'asset_manifest.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('GENERATED',len(figures),'FIGURES',len(tables),'TABLES','PROTECTED',len(protected),'FILES');print('VISUAL REVIEW PENDING')
