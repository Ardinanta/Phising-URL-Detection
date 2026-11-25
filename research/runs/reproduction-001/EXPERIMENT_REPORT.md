# Hasil Reproduksi Enam Eksperimen Utama - Tahap 5

Status: **SELESAI**. Enam konfigurasi LR/RF x A/B/C berhasil dijalankan. Tidak ada subgroup analysis, reweighting atau tuning tambahan.

## Otorisasi, run dan environment

Pengguna secara eksplisit mengotorisasi enam training historis serta guard reproduction-001-six-main. Otorisasi ini bukan persetujuan final baseline seluruh tim; status baseline tetap menunggu tim. Bukti: stage5_execution/authorization.json. Run reproduction-001, branch develop, commit d80117b50f179cfefe91f1c138706264a2934cc7.

Kernel bersih menggunakan .venv Python 3.13.0 dengan cwd [REPOSITORY_ROOT]\runs\reproduction-001. Guard diaktifkan hanya pada environment kernel. Preflight diulang sebelum training dan lagi pada cell 2. Hasil: PASS. Paket: {"numpy": "2.5.2", "pandas": "3.0.5", "scikit-learn": "1.9.1", "matplotlib": "3.11.1", "tldextract": "5.3.1", "threadpoolctl": "3.8.0", "ipykernel": "7.4.0"}. OS Windows-11-10.0.26200-SP0; CPU AMD64 Family 23 Model 160 Stepping 0, AuthenticAMD; RAM 7817785344 byte. Lima versi paket yang tercatat historis sama; Python historis 3.14.4 berbeda dari 3.13.0 saat ini. Dependency transitif/perangkat historis tidak sepenuhnya sama atau tercatat.

## Integritas dan perubahan runner

Cache SHA-256 e7678de14cae2ed296d22d2b2644196af551ae12550dab5170413ce000ea3d8a sesuai Tahap 4; 235370 x 42, phishing 100520, legitimate 134850. Membership/label/cache, checksum input, freeze lock, kedua kelas dan nol irisan domain C diperiksa sebelum fit. A/B memakai membership acak sama; B/C fitur identik. Daftar prediktor tidak mengandung label/identifier.

Runner yang disetujui 02_Eksperimen_Utama.ipynb dipertahankan byte-identik selama eksekusi; hasil disimpan terpisah di 02_Eksperimen_Utama.executed.ipynb. RUNNER_CHANGES.md merinci isolasi dari historis: hilangkan weighted/subgroup execution, tambah guard, training timer, classes assertion, logging dan penyimpanan prediksi. Threshold dan metrics mempertahankan AST historis. Tidak ada perubahan source/fungsi setelah melihat test.

## Konfigurasi dan evaluasi

LR max_iter=1000, random_state=42; pipeline median imputation -> StandardScaler -> LR. RF n_estimators=60, max_depth=16, min_samples_leaf=3, random_state=42, n_jobs=1; median imputation -> RF. Parameter lain mengikuti library historis; actual_parameters.json menyimpan parameter aktual enam pipeline. A=38 selected features, B=C=15; seed42 dan split Tahap4 dipertahankan.

Fit preprocessing/model hanya train. Ambang memaksimalkan F1 validation; tie-break FPR terendah kemudian threshold tertinggi. Phishing positif1; semua classes_ [0,1]; skor positif predict_proba[:,1]. Test hanya evaluasi/timing. Training tidak diulang untuk mengejar skor.

## Hasil utama aktual

| model | skenario | ambang | val_samples | uji_samples | val_f1 | uji_f1 | uji_precision | uji_recall | uji_fpr | uji_roc_auc | uji_accuracy |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LR | A | 0.415656534502 | 35305 | 35306 | 0.999336826049 | 0.999270411886 | 0.999336694083 | 0.99920413848 | 0.000494364247578 | 0.999974540799 | 0.999376876452 |
| LR | B | 0.506425641354 | 35305 | 35306 | 0.991576977071 | 0.99295704129 | 0.999529601505 | 0.986470354158 | 0.000346054973304 | 0.996919494012 | 0.994023678695 |
| LR | C | 0.574050296508 | 34356 | 36229 | 0.991759226084 | 0.991356680965 | 0.999354588873 | 0.983485772358 | 0.000488162069807 | 0.996278165748 | 0.992547406774 |
| RF | A | 0.510749513057 | 35305 | 35306 | 0.999966838004 | 0.999800995025 | 1 | 0.99960206924 | 0 | 0.999998436054 | 0.999830057214 |
| RF | B | 0.559311367725 | 35305 | 35306 | 0.994500916514 | 0.995273598722 | 0.998997728184 | 0.991577132246 | 0.000741546371366 | 0.998092558272 | 0.995978020733 |
| RF | C | 0.555678190464 | 34356 | 36229 | 0.994428173441 | 0.99428644387 | 0.999358357395 | 0.989265752033 | 0.000488162069807 | 0.997540283603 | 0.995059206713 |

Metrik precision/recall/FPR/ROC-AUC/accuracy validation lengkap terdapat pada eksperimen_utama/metrik_utama.csv; angka tabel dibulatkan untuk keterbacaan, CSV menyimpan presisi aktual.

## Confusion matrix aktual

Urutan [TN, FP, FN, TP]; label0 legitimate dan label1 phishing.

| model | skenario | val_tn | val_fp | val_fn | val_tp | uji_tn | uji_fp | uji_fn | uji_tp |
|---|---|---|---|---|---|---|---|---|---|
| LR | A | 20216 | 11 | 9 | 15069 | 20218 | 10 | 12 | 15066 |
| LR | B | 20220 | 7 | 245 | 14833 | 20221 | 7 | 204 | 14874 |
| LR | C | 20286 | 3 | 227 | 13840 | 20475 | 10 | 260 | 15484 |
| RF | A | 20227 | 0 | 1 | 15077 | 20228 | 0 | 6 | 15072 |
| RF | B | 20220 | 7 | 158 | 14920 | 20213 | 15 | 127 | 14951 |
| RF | C | 20279 | 10 | 146 | 13921 | 20475 | 10 | 169 | 15575 |

## Perbandingan presisi penuh dengan historis

| model | scenario | metric | historical | reproduction | difference | absolute_difference |
|---|---|---|---|---|---|---|
| LR | A | ambang | 0.415656534502 | 0.415656534502 | 0 | 0 |
| LR | A | uji_recall | 0.99920413848 | 0.99920413848 | 0 | 0 |
| LR | A | uji_f1 | 0.999270411886 | 0.999270411886 | 0 | 0 |
| LR | A | uji_fpr | 0.000494364247578 | 0.000494364247578 | 0 | 0 |
| LR | A | uji_roc_auc | 0.999974540799 | 0.999974540799 | 0 | 0 |
| LR | B | ambang | 0.506425641354 | 0.506425641354 | 0 | 0 |
| LR | B | uji_recall | 0.986470354158 | 0.986470354158 | 0 | 0 |
| LR | B | uji_f1 | 0.99295704129 | 0.99295704129 | 0 | 0 |
| LR | B | uji_fpr | 0.000346054973304 | 0.000346054973304 | 0 | 0 |
| LR | B | uji_roc_auc | 0.996919494012 | 0.996919494012 | 0 | 0 |
| LR | C | ambang | 0.574050296508 | 0.574050296508 | 0 | 0 |
| LR | C | uji_recall | 0.983485772358 | 0.983485772358 | 0 | 0 |
| LR | C | uji_f1 | 0.991356680965 | 0.991356680965 | 0 | 0 |
| LR | C | uji_fpr | 0.000488162069807 | 0.000488162069807 | 0 | 0 |
| LR | C | uji_roc_auc | 0.996278165748 | 0.996278165748 | 0 | 0 |
| RF | A | ambang | 0.510749513057 | 0.510749513057 | 0 | 0 |
| RF | A | uji_recall | 0.99960206924 | 0.99960206924 | 0 | 0 |
| RF | A | uji_f1 | 0.999800995025 | 0.999800995025 | 0 | 0 |
| RF | A | uji_fpr | 0 | 0 | 0 | 0 |
| RF | A | uji_roc_auc | 0.999998436054 | 0.999998436054 | 0 | 0 |
| RF | B | ambang | 0.559311367725 | 0.559311367725 | 0 | 0 |
| RF | B | uji_recall | 0.991577132246 | 0.991577132246 | 0 | 0 |
| RF | B | uji_f1 | 0.995273598722 | 0.995273598722 | 0 | 0 |
| RF | B | uji_fpr | 0.000741546371366 | 0.000741546371366 | 0 | 0 |
| RF | B | uji_roc_auc | 0.998092558272 | 0.998092558272 | 0 | 0 |
| RF | C | ambang | 0.555678190464 | 0.555678190464 | 0 | 0 |
| RF | C | uji_recall | 0.989265752033 | 0.989265752033 | 0 | 0 |
| RF | C | uji_f1 | 0.99428644387 | 0.99428644387 | 0 | 0 |
| RF | C | uji_fpr | 0.000488162069807 | 0.000488162069807 | 0 | 0 |
| RF | C | uji_roc_auc | 0.997540283603 | 0.997540283603 | 0 | 0 |

Perbandingan lengkap validation/test, precision, seluruh confusion counts, threshold, F1, recall, FPR, AUC dan timing tersedia di historical_comparison_full.csv. Nilai historis dibaca dari CSV menggunakan float_precision=round_trip. Kesamaan agregat tidak membuktikan prediksi atau membership historis per record identik; artefak historis per record tidak tersedia.

## Validasi independen

138 pemeriksaan host lulus. Proses host terpisah membaca kembali 12 CSV prediksi dengan parser round_trip, memverifikasi ID/urutan/label terhadap membership, count dan threshold. Confusion counts, precision, recall, F1, FPR dan accuracy dihitung secara aritmetika; ROC-AUC dihitung independen melalui rank-sum dengan average ranks untuk ties. Semua sesuai CSV dalam toleransi absolut 1e-12. Sweep terpisah atas probability groups validation memverifikasi maksimum F1 serta tie-break threshold. Tidak memakai fungsi metrics/choose_threshold runner untuk validasi host.

Cell 6 juga menghasilkan independent_metric_validation.csv. Bukti validasi host yang lebih lengkap: independent_host_validation.csv.

## Training dan inference time

| model | skenario | training_seconds | uji_batch_ms | historical_batch_ms |
|---|---|---|---|---|
| LR | A | 2.39619300001 | 4.1046999977 | 2.21570000008 |
| LR | B | 0.850476899999 | 2.74640000134 | 1.72010000006 |
| LR | C | 1.1082669 | 2.53349999548 | 1.98969999997 |
| RF | A | 17.285501 | 10.8439000032 | 11.7166999999 |
| RF | B | 6.0004973 | 9.97600000119 | 10.1066 |
| RF | C | 5.8624905 | 9.42959998793 | 10.1084 |

Training time mengukur pipeline.fit. Inference time median5 pengukuran setelah satu warm-up, batch1024, threadlimit1, sampling seed42. Waktu mencakup preprocessing pipeline dan predict_proba; tidak mencakup ekstraksi URL atau pengambilan halaman. Ini pengukuran batch test, bukan timing terpisah validation/test atau end-to-end. Perbedaan perangkat/load membuat timing bukan kriteria kesamaan metrik. Training time historis tidak tersedia untuk pembandingan.

## Selisih antarskenario

| model | perbandingan | uji_f1 | uji_recall | uji_fpr |
|---|---|---|---|---|
| LR | B - A | -0.00631337059589 | -0.0127337843215 | -0.000148309274273 |
| LR | C - B | -0.00160036032427 | -0.00298458180065 | 0.000142107096503 |
| RF | B - A | -0.004527396303 | -0.0080249369943 | 0.000741546371366 |
| RF | C - B | -0.000987154851978 | -0.00231138021314 | -0.000253384301559 |

A/B mengukur tambahan 23 atribut halaman terpilih pada split sama. C/B juga mengubah sampel test dan komposisi kelas. Bias struktur legitimate yang seluruhnya akar pada korpus tetap membatasi interpretasi FPR. Hasil satu seed bukan interval ketidakpastian dan tidak membuktikan generalisasi lintas korpus/periode.

## Error dan warning

Semua enam event training PASS. Warning training: []. Status cell dan output disimpan di notebook executed serta stage5_execution/execution_status.json. Launcher kernel memberi warning lokal TCP tanpa enkripsi; kernel telah dimatikan. Git tetap memperingatkan global ignore tidak dapat dibaca. Tidak ada URL dataset dikunjungi/dicetak.

## Perlindungan file lama

52 file yang dilindungi tetap identik dengan checksum sebelum eksekusi, termasuk dataset/notebook asli, hasil historis, seluruh dokumen Tahap2/3 dan artefak preprocessing Tahap4. Perubahan yang diizinkan: laporan Tahap5, stage5_preflight.json (dijalankan ulang), dan tambahan field stage5 pada run_manifest.json. Semua field run_manifest sebelumnya dipertahankan. Bukti before/after di stage5_execution/. Tidak ada reset/commit/push.

## Inventaris artefak

- Notebook executed: 02_Eksperimen_Utama.executed.ipynb.
- metrik_utama.csv, selisih_utama.csv, actual_parameters.json, training_log.jsonl, manifest_eksperimen.json.
- Dua belas predictions/<model>_<scenario>_<val|uji>.csv.gz dengan clean_row_id, hash URL, label, probabilitas phishing, threshold dan prediksi.
- independent_metric_validation.csv dan independent_host_validation.csv.
- historical_comparison.csv dan historical_comparison_full.csv.
- artifact_checksums.json serta stage5_execution/artifact_inventory.csv dengan SHA-256, ukuran dan path.
- stage5_execution/authorization.json, execution_status.json, preflight_stdout.txt, snapshot before laporan/run manifest/preflight dan checksum before/after.

Semua output ML berada di eksperimen_utama/ run ini. Model tidak disimpan (opsional); parameter aktual dan seluruh probabilitas/prediksi tersimpan sehingga hasil evaluasi dapat ditelusuri. Manifest mencatat hash urutan membership tiap bagian A/B/C, input, runner dan notebook executed.

## Satu pekerjaan berikutnya

Review hasil aktual bersama tim untuk menetapkan baseline selected features serta menyepakati interpretasi perbedaan A/B/C dengan batas bias dataset dan perbedaan environment. Tidak perlu menjalankan training ulang hanya untuk mengejar kesamaan angka. Artikel ilmiah belum ditulis.

## Catatan verifikasi akhir

Perbandingan historical_comparison_full.csv dengan parser round_trip menunjukkan selisih tepat nol untuk seluruh threshold, confusion counts, precision, recall, F1, FPR dan ROC-AUC validation/test. Kolom timing berbeda (maksimum selisih absolut 1,889 ms/batch). Berkas historical_comparison.csv dari parser default runner dapat memperlihatkan selisih representasi desimal sekitar 1e-16; gunakan historical_comparison_full.csv untuk pembandingan presisi penuh.

Output stderr cell 3 mencatat pesan Matplotlib membangun font cache. Tidak ada warning training pada enam event log. Preflight statis masih memuat teks persiapan user training authorization required dan training_started=false; itu snapshot sebelum fit, bukan status akhir otorisasi. Bukti otorisasi aktual terdapat pada stage5_execution/authorization.json dan manifest eksperimen baru.

Status Git akhir: develop, commit d80117b; docs/, requirements-lock.txt dan runs/ untracked; tidak ada diff file tracked. Tidak commit/push. Inventaris aktual output ML berisi 22 file termasuk 12 prediksi gzip, serta notebook executed dan evidence eksekusi di luar direktori output ML.
