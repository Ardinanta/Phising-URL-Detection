# Evaluasi Fitur Leksikal URL dan Pemisahan Domain pada PhiUSIIL

> **Panduan reproduksi enam eksperimen utama:** lihat bagian "Workflow portable" di bawah. Instruksi historis yang menjalankan seluruh notebook kedua juga menjalankan analisis pembobotan tambahan; workflow utama baru tidak menjalankannya. Baseline selected features masih menunggu persetujuan final tim.

Proyek ini menguji Logistic Regression dan Random Forest pada tiga skenario. Metrik utama adalah F1 untuk kelas phishing. Analisis tambahan mengevaluasi pembobotan kelompok struktur URL.

## Menjalankan proyek

Dari direktori proyek, gunakan Python 3.11 atau lebih baru dan pasang dependensi.

```powershell
python -m pip install -r requirements.txt
```

1. Pastikan `Dataset/PhiUSIIL_Phishing_URL_Dataset.csv` tersedia.
2. Buka [01_Audit_dan_Split.ipynb](01_Audit_dan_Split.ipynb) di VS Code atau Jupyter, pilih kernel Python tempat dependensi dipasang, lalu jalankan semua sel.
3. Jalankan semua sel di [02_Eksperimen_dan_Evaluasi.ipynb](02_Eksperimen_dan_Evaluasi.ipynb) dengan direktori kerja yang sama.

## Rancangan eksperimen

| Skenario | Fitur | Split |
| --- | --- | --- |
| A | 15 fitur leksikal dan 23 atribut halaman dari CSV | Acak terstratifikasi |
| B | 15 fitur leksikal dari teks URL | Acak terstratifikasi dengan baris yang sama seperti A |
| C | Fitur leksikal yang sama seperti B | Domain terdaftar terpisah |

Audit mendeteksi konflik label dan menghapus duplikasi sebelum split. Seed 42 digunakan untuk target 70/15/15. Split C mengalokasikan domain menurut rasio tersebut, lalu melaporkan rasio baris aktual dan memeriksa irisan domain nol. URL diperlakukan sebagai teks lokal. Domain dihitung dari snapshot Public Suffix List bawaan tldextract. Imputasi dan standardisasi dipelajari dari data latih. Ambang hasil utama memaksimalkan F1 validasi dan dibekukan untuk data uji.

Analisis tambahan membandingkan tanpa bobot, bobot kelas, dan bobot kelompok phishing berdasarkan struktur akar, path atau query. Ambang validasi memaksimalkan recall dengan FPR maksimal 1%. Recall minimum menggunakan kelompok dengan setidaknya 30 sampel phishing.

## Keluaran

- `hasil/ringkasan_split.csv`, `hasil/irisan_domain.csv` dan `hasil/distribusi_struktur_split.csv` mendokumentasikan pembagian data.
- `hasil/metrik_utama.csv` memuat enam konfigurasi dengan F1, precision, recall, ROC-AUC, FPR, TP/FP/FN/TN dan waktu inferensi. Waktu adalah median per 1.024 baris dan mencakup praproses pipeline serta prediksi probabilitas. Ekstraksi fitur dilakukan lebih dahulu.
- `hasil/selisih_utama.csv` memuat B − A dan C − B. B dan C memakai sampel uji berbeda.
- `hasil/metrik_pembobotan.csv`, `hasil/metrik_struktur_pembobotan.csv` dan `hasil/selisih_pembobotan.csv` memuat hasil pembobotan.
- `hasil/manifest_data.json` dan `hasil/manifest_eksperimen.json` menyimpan checksum CSV, seed, versi pustaka, fitur, dan parameter run. `hasil/fitur_internal.csv.gz` dibuat ulang oleh notebook audit.

## Sumber

PhiUSIIL menggunakan label asli 0 untuk phishing dan 1 untuk sah. Notebook memetakan phishing menjadi kelas positif 1. UCI mendokumentasikan lisensi CC BY 4.0. Identitas file lokal dicatat dengan SHA-256. Versi, tanggal unduh dan lisensi yang tercantum pada salinan Kaggle belum terverifikasi. [Kaggle](https://www.kaggle.com/datasets/kaggleprollc/phishing-url-websites-dataset-phiusiil) · [UCI](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset) · [Artikel PhiUSIIL](https://doi.org/10.1016/j.cose.2023.103545)

## Workflow portable: enam eksperimen utama

Kontribusi reproduksi mempertahankan pertanyaan penelitian, LR/RF, seed42, target70/15/15, phishing positif1, serta aturan threshold F1 validation maksimum (tie-break FPR terendah, lalu threshold tertinggi). A menggunakan **38 selected features** (15 leksikal + 23 atribut halaman terpilih); B menggunakan 15 leksikal pada membership acak yang sama; C menggunakan fitur identik B dengan domain terdaftar terpisah. A bukan seluruh fitur PhiUSIIL. Imputasi median/model hanya fit train; StandardScaler hanya LR. Test tidak dipakai tuning.

LR memakai max_iter=1000 dan random_state=42. RF memakai n_estimators=60, max_depth=16, min_samples_leaf=3, random_state=42, n_jobs=1. Parameter aktual lengkap tersimpan pada artefak publik. Tidak ada subgroup/reweighting dalam workflow enam utama.

```text
scripts/                         CLI reproduksi dan validator portable
research/docs/audit/             salinan publik audit fitur dan environment
research/runs/reproduction-001/  bukti hasil aktual, analisis, dan aset ilmiah
research/DISTRIBUTION_MANIFEST.json  checksum distribusi publik
runs/<run-id>/                   output lokal baru; cache/prediksi tidak diunggah
hasil/                          hasil historis anggota tim, tetap dipertahankan
```

### Environment dan input

Gunakan Python >=3.11 dan virtual environment project; reproduksi aktual sebelumnya memakai Python3.13.0. Lockfile merekam versi aktual, bukan jaminan kompatibilitas lintas semua platform/versi Python. Pada platform yang tidak menyediakan wheel versi lockfile, jangan mengubah versi diam-diam; dokumentasikan perbedaan dan tinjau bersama tim.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts/validate_distribution.py
```

Dataset harus tersedia lokal pada `Dataset/PhiUSIIL_Phishing_URL_Dataset.csv`. Script tidak mengunduh data atau membuka URL dataset. Sumber dan ketidakpastian lisensi/versi salinan Kaggle tetap sebagaimana bagian Sumber. Checksum CSV historis:

```text
a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6
```

### Preprocessing, split, dan validasi

Pilih run ID baru; semua langkah menolak penimpaan bukti run yang sudah ada. Jalankan dari root repository:

```powershell
.\.venv\Scripts\python.exe scripts/reproduce.py prepare --run runs/reproduction-002
.\.venv\Scripts\python.exe scripts/reproduce.py preprocess --run runs/reproduction-002
.\.venv\Scripts\python.exe scripts/reproduce.py validate-cache --run runs/reproduction-002
.\.venv\Scripts\python.exe scripts/reproduce.py preflight --run runs/reproduction-002
```

Preprocessing menyalin notebook audit asli dan mengeksekusinya pada kernel baru dengan cwd run. Validator menghasilkan membership ID/hash URL, memeriksa fitur/cache/label, cakupan baris dan irisan domain. Private suffix aktif, PSL bawaan tldextract, IP/suffix tak dikenal fallback host. Rasio baris aktual domain-grouped dilaporkan, bukan dipaksa70/15/15.

### Training eksplisit dan evaluasi

Perintah berikut **menjalankan training**. Hanya jalankan setelah otorisasi untuk reproduksi enam konfigurasi historis. Otorisasi tersebut tidak menggantikan persetujuan baseline seluruh tim.

```powershell
.\.venv\Scripts\python.exe scripts/reproduce.py train --run runs/reproduction-002 --authorize-training
.\.venv\Scripts\python.exe scripts/reproduce.py validate-metrics --run runs/reproduction-002
```

Tanpa flag otorisasi, training ditolak. Output adalah notebook executed, CSV metrik, durasi, parameter, log, probabilitas/prediksi validation/test dan hash membership. Validator terpisah menghitung ulang confusion counts, precision, recall, F1, FPR, accuracy, rank-based ROC-AUC serta threshold validation. Error menghentikan proses dan mempertahankan hasil parsial; tidak ada tuning/retry training otomatis.

### Analisis dan visualisasi tanpa training ulang

```powershell
.\.venv\Scripts\python.exe scripts/reproduce.py analysis --run runs/reproduction-002
.\.venv\Scripts\python.exe scripts/reproduce.py figures --run runs/reproduction-002
```

Perintah tersebut hanya membaca artefak lokal yang telah dihasilkan. Jika cache/prediksi belum ada, script memberikan instruksi dan berhenti, bukan memulai training. Snapshot publik sudah menyediakan hasil agregat, analisis serta 14 gambar PNG300DPI/SVG dan 10 tabel CSV/Markdown, sehingga dapat dibaca tanpa menghasilkan ulang prediksi. ROC tidak dapat digambar ulang dari satu nilai AUC; perlu probabilitas test aktual.

## Ringkasan hasil reproduksi aktual

| Konfigurasi | F1 test | Recall test | FPR test |
|---|---:|---:|---:|
| LR/A | 0.999270 | 0.999204 | 0.000494 |
| LR/B | 0.992957 | 0.986470 | 0.000346 |
| LR/C | 0.991357 | 0.983486 | 0.000488 |
| RF/A | 0.999801 | 0.999602 | 0.000000 |
| RF/B | 0.995274 | 0.991577 | 0.000742 |
| RF/C | 0.994286 | 0.989266 | 0.000488 |

Sumber: [metrik presisi penuh](research/runs/reproduction-001/eksperimen_utama/metrik_utama.csv), [laporan eksperimen](research/runs/reproduction-001/EXPERIMENT_REPORT.md), [analisis](research/runs/reproduction-001/analysis/ANALYSIS_REPORT.md), dan [indeks aset](research/runs/reproduction-001/publication_assets/ASSET_INDEX.md). Reproduksi historis melewati 138 pemeriksaan host independen. Threshold, confusion matrix dan metrik agregat sama dengan CSV historis; timing berbeda. Prediksi historis per record tidak tersedia untuk membuktikan kesamaan per record.

## Bukti publik, keterbatasan, dan kontribusi tim

[Panduan salinan publik](research/README.md) menjelaskan sanitasi dan manifest. Checksum historis tetap provenance; checksum file yang didistribusikan terdapat pada manifest distribusi terpisah. Artefak lokal asli tidak diubah. Dataset duplikat run, cache fitur, membership per-record, prediksi, .venv, ZIP dan cache font tidak diunggah; workflow menghasilkan ulang input lokal tersebut secara eksplisit.

Keterbatasan: satu dataset/seed; seluruh legitimate mentah berstruktur akar; potensi shortcut bukan leakage terkonfirmasi; A adalah selected features; membership/komposisi B dan C berbeda; provenance belum lengkap; timing bukan end-to-end. Tidak ada klaim signifikansi statistik, FPR populasi nol, atau reproducibility sempurna. Persetujuan final baseline tim masih menunggu.

Kontribusi lanjutan memakai feature branch dan PR ke develop, bukan push langsung ke develop/main. Jangan menimpa hasil historis, mengunggah credential/prediksi belum ditinjau, atau mengubah parameter berdasarkan skor test. Gunakan staging eksplisit, tinjau ukuran/path sensitif, dan jalankan QA distribusi. Detail script dan batas pengujian: [scripts/README.md](scripts/README.md) dan [PUBLICATION_QA.md](research/PUBLICATION_QA.md).
