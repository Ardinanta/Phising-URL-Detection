# Evaluasi Fitur Leksikal URL dan Pemisahan Domain pada PhiUSIIL

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
