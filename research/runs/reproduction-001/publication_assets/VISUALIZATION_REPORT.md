# Laporan Visualisasi dan Tabel Ilmiah

Status akhir: SELESAI. Validasi numerik, format dan pemeriksaan visual lulus.

Jumlah: 14 gambar ilmiah, masing-masing PNG300DPI dan SVG (28 file), serta 10 tabel dalam CSV/Markdown (20 file).

## Validasi sumber dan desain

Checksum analysis/Tahap4/Tahap5 lulus; metrik dibandingkan dengan CSV utama; 6 ROC-AUC diperiksa dari probabilitas aktual dan membership test. Data dibaca round_trip, tanpa mengambil nilai tabel yang sudah dibulatkan. Warna LR biru #0072B2 dan RF jingga #D55E00; bentuk marker membedakan model. Background putih, font DejaVu Sans, tanpa3D/error bar. Skala persentase dan pp dipisahkan; count dan rate terpisah. Caption menyebut sumbu F1/recall/trade-off yang diperbesar.

## Ekspor dan QA

Semua PNG dapat dibuka melalui Pillow dan mencatat DPI mendekati300; dimensi piksel per file ada di asset_manifest.json. Semua SVG lolos XML parsing. Confusion matrix berbagi skala warna, normalized per kelas aktual dan denominator dicantumkan. ROC memakai probabilitas aktual, bukan rekonstruksi AUC. Generator source/generate_assets.py dan contact sheets mendukung inspeksi ulang.

## Reproduksi

Working directory bebas: generator menentukan input/output dari lokasi file. Gunakan interpreter project .venv. Dari root repositori:

```powershell
.\.venv\Scripts\python.exe runs/reproduction-001/publication_assets/source/generate_assets.py --overwrite
```

Tanpa --overwrite generator menolak jika manifest aset sudah ada. Flag hanya mengizinkan regenerasi output publication_assets, tidak sumber eksperimen. Dependency aktual: {"matplotlib": "3.11.1", "numpy": "2.5.2", "pandas": "3.0.5", "scikit-learn": "1.9.1", "pillow": "13.0.0"}. Tidak ada install/training. Semua source/output tercatat di manifest dan ASSET_INDEX.md.

## Integritas dan batas klaim

98 file sebelumnya diperiksa sebelum/sesudah; berubah: []. Bukti SHA256 tersimpan pada asset_manifest.json. Baseline masih menunggu persetujuan tim. Satu dataset/seed, ketimpangan struktur, test B/C berbeda, provenance belum lengkap, dan timing non-end-to-end membatasi klaim. Tidak ada klaim signifikansi statistik, leakage terkonfirmasi atau FPR populasi nol. Template jurnal belum tersedia; diagram/multipanel cocok dua kolom, point plots/timing dapat memakai satu kolom setelah uji keterbacaan. Ukuran fisik aktual dicatat lewat dimensi pixel/DPI dan source.

## Rekomendasi aset utama

Methods: fig01/fig02 dan table02/table03/table05. Results: fig03/fig04/fig05/fig06, table06/table07/table08. Discussion: fig09/fig10/fig11 dan table10. Confusion matrix, ROC dan timing lengkap dapat menjadi materi pendukung sesuai batas ruang template. Ini rekomendasi aset, bukan naskah artikel.

## Inventaris

ASSET_INDEX.md memetakan seluruh nama file dan sumber. FIGURE_CAPTIONS.md dan TABLE_CAPTIONS.md menyimpan judul, penjelasan, satuan, sumber, batas klaim dan bagian artikel yang disarankan. asset_manifest.json menyimpan format, ukuran, checksum, resolusi, environment dan integritas sumber.

## QA visual dan verifikasi akhir

Keempat contact sheets ditelaah untuk seluruh 14 desain. Panel delta yang semula terlalu renggang diperbaiki dan diperiksa ulang pada resolusi lebih tinggi; ROC dengan label Indonesia juga diperiksa ulang. Tidak ditemukan label terpotong, teks saling menutup, atau legenda menutupi data. Gambar ROC pada sumbu penuh memang bertumpuk dekat kiri-atas; caption menjelaskan hal ini tanpa menambahkan sumbu zoom tersembunyi.

Seluruh 10 tabel CSV dibandingkan dengan sumber presisi penuh: ringkasan dataset, konfigurasi, split, irisan domain, parameter estimator, metrik, delta, confusion counts, waktu dan reproduksibilitas. Header tabel delta dan penanda nilai tidak tersedia diperbaiki agar tidak mengandung karakter pengganti. CSV mempertahankan presisi; pembulatan hanya Markdown/anotasi.

PNG diverifikasi terbuka dengan DPI300; SVG dapat dibuka/parsing sebagai XML dan berasal dari Figure yang sama dengan PNG yang diperiksa visual. Rendering SVG pada perangkat lunak jurnal tertentu belum diuji. Ketika template tersedia, keterbacaan pada ukuran kolom final masih perlu diperiksa; khusus multipanel/diagram direkomendasikan dua kolom. Tidak ada klaim signifikansi atau confidence interval fiktif.

Seluruh 98 file sebelumnya tetap identik. Tidak ada training, tuning, perubahan split/fitur, perubahan hasil eksperimen, commit atau push. Semua output tahap ini termasuk cache font Matplotlib, contact sheets dan skrip QA berada dalam publication_assets/. asset_manifest.json tidak mencantumkan checksum dirinya sendiri untuk menghindari checksum melingkar. Menjalankan ulang generator akan mengembalikan status inspeksi visual ke PENDING, sehingga inspeksi ekspor baru harus dilakukan kembali.
