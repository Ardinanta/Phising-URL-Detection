# Public research contribution

Direktori ini berisi **salinan publik** kontribusi audit, reproduksi, analisis dan aset publikasi. Artefak lokal asli dari Tahap 1–7 tetap dipertahankan di mesin penelitian; sumber historis anggota tim pada root repository dan `hasil/` tidak ditimpa.

## Status bukti

- Angka eksperimen, parameter, fitur 38/15/15, seed 42, split, aturan threshold dan hasil evaluasi tidak diubah.
- Path mesin pribadi disamarkan pada salinan laporan/manifest/notebook evidence. Notebook `*.executed.ipynb` adalah bukti tersanitasi, bukan template untuk dijalankan ulang.
- Template `runs/reproduction-001/02_Eksperimen_Utama.ipynb`, preflight dan analisis memiliki perbaikan portabilitas. Seluruh penyesuaian berkaitan dengan path, I/O, integritas dan workflow; tidak ada training tambahan pada tahap publikasi ini.
- Checksum **historis** di dalam manifest penelitian dipertahankan sebagai provenance. Checksum tersebut tidak boleh dipakai untuk memvalidasi byte salinan yang sudah disanitasi atau mengharuskan file privat yang sengaja tidak dibagikan.
- `PUBLIC_COPY_MAP.json` mencatat hash asli dan hash salinan publik; `DISTRIBUTION_MANIFEST.json` adalah inventory otoritatif file distribusi saat ini. Keduanya tidak mengklaim checksum historis cocok dengan file yang telah disanitasi.

## Artefak yang tidak dipublikasikan

Dataset duplikat run, cache fitur, membership SHA-256 URL per record, seluruh prediksi/probabilitas per record, virtual environment, font cache, contact sheets dan ZIP tidak disertakan. Ini keputusan kurasi distribusi, bukan penghapusan lokal. Lisensi/versi salinan Kaggle belum terverifikasi lengkap. Dataset asli yang sudah tracked oleh tim tidak diubah atau diduplikasi dalam kontribusi ini.

Untuk mendapatkan cache, membership dan prediksi lokal yang diperlukan analisis/ROC, jalankan workflow eksplisit di README root pada **run baru**. Source-only checkout tidak dapat menjalankan validasi per-record atau menggambar ROC ulang hanya dari metrik agregat. Script memberi instruksi input yang hilang dan tidak pernah otomatis memulai training.

## Validasi dan keterbatasan

`python scripts/validate_distribution.py` memeriksa inventory publik, syntax, serta pola path/credential. Itu smoke test distribusi, bukan pengulangan training atau pengganti validasi ilmiah Tahap 4–6.

Hasil historis enam konfigurasi telah direproduksi sebelumnya dan melewati 138 pemeriksaan host independen. Publikasi ini tidak mengklaim training diulang setelah perbaikan portabilitas. Kesamaan metrik agregat historis tidak membuktikan prediksi historis per record identik. Baseline masih menunggu persetujuan final tim; otorisasi training pengguna sebelumnya bukan persetujuan seluruh tim.
