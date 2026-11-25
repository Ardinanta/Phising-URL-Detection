# Isolasi enam eksperimen utama - Tahap 5

Status: disiapkan, belum dieksekusi untuk training. Baseline masih menunggu persetujuan tim. Otorisasi training pengguna belum tersedia; instruksi Tahap 5 bagian 1 mewajibkan menunggu otorisasi tersebut.

Sumber: notebook asli `../../02_Eksperimen_dan_Evaluasi.ipynb`, khususnya cell 2, 4, 6 dan 8. Nomor cell mulai 1 termasuk Markdown. Notebook asli dan salinan historis Tahap 4 tidak diubah. Notebook baru: `02_Eksperimen_Utama.ipynb`.

## Pemetaan cell notebook baru

| Cell | Isi | Hubungan dengan historis |
|---|---|---|
| 1 | Penjelasan status dan cakupan | Dokumentasi baru |
| 2 | Guard otorisasi, cwd, preflight input | Pemeriksaan integritas baru; gagal sebelum fit jika otorisasi belum diberikan |
| 3 | Import, input, parameter, output terpisah | Berasal dari cell 2 historis; input tetap `hasil/` dalam run, output baru `eksperimen_utama/`; menolak output yang sudah ada |
| 4 | choose_threshold, metrics, fit_and_score | Berasal dari cell 4 historis; lihat rincian di bawah |
| 5 | Loop LR/A, LR/B, LR/C, RF/A, RF/B, RF/C | Hanya loop utama cell 6 historis; simpan prediksi dan hasil parsial |
| 6 | Validasi prediksi, perbandingan, manifest, checksum | Pelaporan tambahan; tidak mengubah model atau memilih konfigurasi dari test |

`choose_threshold` dan `metrics` dipertahankan identik secara AST. F1 validation dimaksimalkan dengan tie-break FPR terendah lalu ambang tertinggi. Pemanggilan utama selalu `fpr_limit=None`; cabang batas FPR historis tetap di fungsi tetapi tidak dipakai.

`fit_and_score` mempertahankan pemilihan train/validation/test, pipeline, parameter, model.fit pada train, pemanasan, sampling batch 1024 seed 42, lima pengulangan median dan thread limit satu. Perubahan hanya: assert strategi tanpa bobot, hapus cabang pembentukan bobot yang tidak dipakai, timer di sekitar pipeline.fit, assert classes_ tepat [0,1], dan pengembalian model serta durasi untuk penyimpanan parameter. Kolom probabilitas tetap [:,1]. Tidak ada perubahan skor, threshold atau parameter berdasarkan hasil test.

Helper `evaluate` historis tidak disalin karena memproduksi subgroup. Agregasi utamanya memakai fungsi metrics yang sama dan threshold validation yang sama. sample_weights, loop weighted, by_group, recall minimum subgroup dan grafik pembobotan tidak disalin. Konfigurasi A/B/C dan urutan fit tetap sama. Accuracy dan jumlah sampel ditambahkan hanya sebagai metrik pelaporan. Inference time mencakup preprocessing pipeline dan predict_proba; tidak mencakup ekstraksi URL atau pengambilan halaman.

Output yang direncanakan: metrik_utama.csv, selisih_utama.csv, actual_parameters.json, training_log.jsonl, dua belas file prediksi gzip dengan ID/hash URL, independent_metric_validation.csv, historical_comparison.csv, manifest_eksperimen.json, dan artifact_checksums.json di `eksperimen_utama/`. Validasi metrik membaca ulang prediksi tersimpan dan menghitung confusion matrix, accuracy, precision, recall, F1, FPR dan ROC-AUC. Model tidak disimpan karena opsional; parameter aktual dan probabilitas per record dipertahankan. Notebook hasil eksekusi harus disimpan terpisah setelah otorisasi; belum ada pada tahap persiapan ini.

Input dan hash membership dicatat di stage5_preflight.json. Saat eksekusi kelak, manifest output juga akan memuat hash urutan SHA-256 URL tiap bagian dan skenario. Perbandingan historis menggunakan presisi penuh CSV; waktu diberi catatan perangkat berbeda. Prediksi historis tidak tersedia sehingga kesamaan historis per record tidak boleh diklaim.

Metadata kernel notebook baru menunjuk ttki-p1/.venv dan Python aktual 3.13.0. Notebook memiliki ID cell stabil; seluruh execution_count masih null dan outputs kosong. Kernel baru hanya dipakai untuk menguji interpreter, cwd dan guard yang menolak training; tidak ada cell fit dikirim ke kernel.

## Otorisasi

Guard menggunakan variabel `TTKI_P1_TRAINING_AUTHORIZED` bernilai `reproduction-001-six-main`. Variabel belum diatur. Pengaturan hanya dilakukan setelah pengguna memberikan otorisasi eksplisit; pengaturan variabel itu sendiri bukan bukti persetujuan tim. Persetujuan baseline tim dan otorisasi menjalankan reproduksi historis adalah dua catatan berbeda.

Setelah otorisasi: verifikasi ulang checksum/preflight, gunakan kernel bersih dengan interpreter .venv dan cwd direktori run, jalankan keenam cell kode/Markdown sesuai urutan, simpan notebook hasil eksekusi dan catatan otorisasi, periksa file lama sebelum/sesudah, lalu lengkapi EXPERIMENT_REPORT.md dengan angka aktual. Jangan mengubah file input atau menimpa output bila eksekusi parsial telah ada.
