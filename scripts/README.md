# Portable reproduction scripts

Semua perintah menggunakan Python >=3.11 dalam virtual environment project. Dependency langsung mengikuti `requirements.txt`; lockfile merekam environment aktual Python3.13/Windows dari reproduksi. `jupyter-client`, `scipy`, dan `psutil` merupakan dependency transitif yang dicatat lockfile. Tidak ada package global dipasang oleh script.

| Script | Fungsi | Menjalankan training? |
|---|---|---|
| reproduce.py prepare | Copy input ke direktori run baru, tidak menimpa run lama | Tidak |
| reproduce.py preprocess | Eksekusi notebook audit asli pada kernel bersih/cwd run | Tidak |
| validate_cache.py | Validator Tahap4 yang dipromosikan; ekstraksi ulang lokal dan membership | Tidak |
| preflight.py | Verifikasi cache/membership dan fitur aktual sebelum fit | Tidak |
| reproduce.py train --authorize-training | Enam konfigurasi utama saja pada kernel bersih | Ya, hanya dengan flag eksplisit |
| validate_metrics.py | Validator host Tahap5 yang dipromosikan; count, rate, rank-based AUC, threshold | Tidak |
| reproduce.py analysis | Notebook analisis dari metrik dan prediksi aktual lokal | Tidak |
| reproduce.py figures | Generator Matplotlib dari hasil aktual/prediksi | Tidak |
| validate_distribution.py | Checksum/syntax/path/secret-pattern pada file publik | Tidak |

Jalankan dari root repository. `--run` menunjuk direct child `runs/`, misalnya `runs/reproduction-002`. Script menolak output yang sudah ada dan berhenti pada error; log serta notebook parsial dipertahankan. Jangan memakai snapshot publik `research/runs/reproduction-001` sebagai direktori output.

Pemindahan kode: validate_cache.py berasal dari validator independen Tahap4; validate_metrics.py berasal dari finalizer/validator independen Tahap5. Perubahan input root/run menjadi CLI, penghilangan path mesin lama dan pengecualian file runtime dari snapshot integritas tidak mengubah perhitungan metrik/fitur atau metode penelitian. Notebook utama mempertahankan helper model, threshold dan metrics yang sama; penambahan guard/timing/penyimpanan tetap sebagaimana audit Tahap5.

Hash gzip cache berbeda antar-generasi dapat disebabkan timestamp container. Preflight sekarang memvalidasi hash **run aktual**, checksum CSV, schema/label/fitur, membership dan hasil validator; tidak memaksakan hash container run lama pada file baru. Checksum historis asli tetap dicatat dalam provenance publik.

Pengujian publikasi tidak menjalankan preprocessing atau training ulang. Lihat `research/PUBLICATION_QA.md` untuk pemeriksaan yang benar-benar dijalankan dan keterbatasannya.
