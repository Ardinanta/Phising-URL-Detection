# QA distribusi publik

Tanggal pemeriksaan: 25 November 2026. Branch kontribusi: feature/reproducibility. Identitas Git diatur hanya pada repository lokal; tidak ada perubahan konfigurasi global. Baseline masih menunggu keputusan final tim.

## Pemeriksaan yang benar-benar dijalankan

- Python AST untuk seluruh script dan cell kode notebook publik; parsing JSON/manifest.
- Validasi inventory SHA-256 publik dan pemeriksaan pola credential/path mesin pribadi. Pemindaian pola bukan jaminan deteksi semua jenis rahasia.
- Preflight **read-only** pada cache Tahap4 asli: 235370 x 42, label 100520 phishing/134850 legitimate, fitur38/15/15, checksum dataset/cache/membership dan nol irisan domain C lulus. Tidak ada fit model.
- Lima belas smoke check pada ekspor bersih tanpa dataset/cache/prediksi dan tanpa folder .git: validator distribusi, lima CLI --help, penolakan train tanpa flag, pesan dataset hilang saat prepare, enam penolakan input hilang, dan satu kernel sintetis. Semua lulus.
- Kernel sintetis hanya mencetak pesan; tidak mengeksekusi notebook penelitian. Interpreter/cwd portable dipakai dan hasil executed disimpan di direktori smoke lokal yang diabaikan Git.
- Smoke test pertama menemukan validator membaca komponen path absolut tempat ekspor berada sebagai path distribusi. Pemeriksaan diperbaiki menjadi relatif terhadap root ekspor; smoke test pada direktori baru kemudian lulus. Tidak ada metodologi/model yang diubah untuk memperbaiki masalah ini.
- pip check pada environment penelitian tidak menemukan dependency rusak. Lockfile aktual dipertahankan.
- Link file lokal dalam README diperiksa keberadaannya. Aturan ignore diuji memakai git check-ignore; .venv, dataset duplikat, cache fitur, prediksi dan ZIP diabaikan, sedangkan dokumen/hasil ilmiah publik tidak diabaikan.
- Matriks metrik numerik publik dan parameter aktual dibandingkan dengan bukti lokal. Helper fit/threshold/metrics pada template utama tetap identik secara AST dengan runner enam-utama yang telah direproduksi, kecuali lokasi input/output/guard portabel di cell terpisah.
- Ukuran dan daftar staging ditinjau eksplisit; tidak memakai git add seluruh workspace. Semua sumber asli dan hasil historis dicek checksum sebelum commit.
- Aturan .gitattributes mempertahankan byte distribusi agar autocrlf lintas perangkat tidak membatalkan SHA-256. Whitespace path SVG keluaran Matplotlib dipertahankan sebagai generated data; check whitespace source menggunakan cr-at-eol untuk membedakan terminator CRLF dari spasi kode.

## Batas pengujian

Tidak ada preprocessing atau training ulang pada tahap finalisasi publikasi ini. Workflow portable baru telah diuji syntax, path, dependency dan guard/absence handling, bukan eksekusi penuh enam model. Bukti 138 pemeriksaan host independen mengacu pada reproduksi aktual sebelumnya, bukan smoke test publikasi.

Analisis dan ROC memerlukan prediksi lokal yang sengaja tidak diunggah. Keberhasilan mengulang seluruh workflow pada mesin lain belum dibuktikan; perbedaan Python/platform dan wheel dependency harus dicatat, bukan disembunyikan. Nilai agregat tetap berasal dari eksperimen aktual dan tidak dihitung ulang untuk mengejar kesamaan.

Checksum asli tetap provenance. PUBLIC_COPY_MAP.json membedakan hash asli dari salinan tersanitasi; DISTRIBUTION_MANIFEST.json memvalidasi distribusi publik saat ini. Notebook executed tersanitasi adalah bukti keluaran, bukan template eksekusi. Artefak asli tetap berada di penyimpanan lokal.

Sumber historis pada root, kedua notebook asli, dataset asli, seluruh hasil/ historis, dokumen Tahap2–7 dan semua artefak run asli tidak diubah. Perubahan tracked yang disengaja hanya penambahan panduan README dan aturan ignore. Keduanya disetujui untuk finalisasi repository.
