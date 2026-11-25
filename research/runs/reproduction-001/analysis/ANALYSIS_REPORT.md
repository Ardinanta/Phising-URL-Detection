# Analisis Ilmiah Hasil Eksperimen TTKI P1

Run reproduction-001; commit d80117b50f179cfefe91f1c138706264a2934cc7. Analisis artefak tersimpan, tanpa training/tuning, perubahan fitur/split, subgroup baru atau reweighting. Bukan draf artikel jurnal. Persetujuan final baseline tim masih menunggu; pengguna telah mengotorisasi reproduksi historis.

## Validasi input dan satuan

Checksum Tahap4 dan seluruh input/output pada inventory Tahap5 diverifikasi. Dua belas file prediksi diperiksa terhadap membership, label, threshold, confusion counts dan seluruh metrik, termasuk ROC-AUC. Validasi Tahap5 120 pemeriksaan notebook dan 138 pemeriksaan host seluruhnya PASS; Tahap6 membaca dan memeriksanya kembali. Bukti rinci disimpan di validation_manifest.json. Seluruh perhitungan memakai float64 dari CSV dengan parser round_trip; pembulatan hanya tabel. pp = poin persentase = 100 x (proporsi kemudian - proporsi awal), bukan perubahan relatif persen. CSV count dan satuan timing eksplisit.

## Performa enam konfigurasi

| model | skenario | uji_accuracy | uji_precision | uji_recall | uji_f1 | uji_roc_auc | uji_fpr |
|---|---|---|---|---|---|---|---|
| LR | A | 0.999376876 | 0.999336694 | 0.999204138 | 0.999270412 | 0.999974541 | 0.000494364248 |
| LR | B | 0.994023679 | 0.999529602 | 0.986470354 | 0.992957041 | 0.996919494 | 0.000346054973 |
| LR | C | 0.992547407 | 0.999354589 | 0.983485772 | 0.991356681 | 0.996278166 | 0.00048816207 |
| RF | A | 0.999830057 | 1 | 0.999602069 | 0.999800995 | 0.999998436 | 0 |
| RF | B | 0.995978021 | 0.998997728 | 0.991577132 | 0.995273599 | 0.998092558 | 0.000741546371 |
| RF | C | 0.995059207 | 0.999358357 | 0.989265752 | 0.994286444 | 0.997540284 | 0.00048816207 |

Accuracy, precision, recall, F1, ROC-AUC dan FPR memakai skala proporsi 0-1. performance_comparison.csv menyimpan seluruh metrik validation/test, confusion counts, threshold, ukuran sampel dan feature count. Phishing=1. FPR=FP/(FP+TN).

Perbandingan RF minus LR pada skenario yang sama (pp):

| skenario | RF_minus_LR_test_accuracy_pp | RF_minus_LR_test_precision_pp | RF_minus_LR_test_recall_pp | RF_minus_LR_test_f1_pp | RF_minus_LR_test_roc_auc_pp | RF_minus_LR_test_fpr_pp |
|---|---|---|---|---|---|---|
| A | 0.0453180762 | 0.0663305917 | 0.039793076 | 0.0530583139 | 0.00238952556 | -0.0494364248 |
| B | 0.195434204 | -0.0531873321 | 0.510677809 | 0.231655743 | 0.117306426 | 0.0395491398 |
| C | 0.251179994 | 0.000376852182 | 0.577997967 | 0.29297629 | 0.126211785 | 0 |

RF memberi F1/recall/ROC-AUC lebih tinggi pada ketiga skenario dan accuracy lebih tinggi. RF A precision lebih tinggi dan FPR lebih rendah; RF B precision lebih rendah dan FPR lebih tinggi daripada LR B; RF C FPR sama. Pemilihan model melibatkan trade-off recall/FP/biaya, bukan satu pemenang universal. Tidak ada pengujian signifikansi.

## B dikurangi A: pembatasan fitur

| model | direction | later | earlier | metric_partition | same_test_membership | same_feature_set | delta_accuracy_pp | delta_precision_pp | delta_recall_pp | delta_f1_pp | delta_roc_auc_pp | delta_fpr_pp | delta_fp_count | delta_fn_count | delta_samples_count | delta_training_seconds | delta_inference_ms_per_1024 | training_relative_change_percent | inference_relative_change_percent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LR | B minus A | B | A | test | True | False | -0.535319776 | 0.0192907422 | -1.27337843 | -0.63133706 | -0.305504679 | -0.0148309274 | -3 | 192 | 0 | -1.5457161 | -1.3583 | -64.507162 | -33.0913343 |
| RF | B minus A | B | A | test | True | False | -0.385203648 | -0.100227182 | -0.802493699 | -0.45273963 | -0.190587778 | 0.0741546371 | 15 | 121 | 0 | -11.2850037 | -0.867900002 | -65.2859509 | -8.00357806 |

A/B menggunakan train, validation dan test identik, diverifikasi dari ID/hash prediksi dan membership. B mengeluarkan 23 atribut halaman terpilih dari A sambil mempertahankan 15 fitur leksikal. F1 dan recall turun pada LR maupun RF. LR mengalami FN bertambah192 dan FP berkurang3; RF mengalami FN bertambah121 dan FP bertambah15. Precision LR sedikit naik tetapi recall turun; precision RF turun. FPR tidak bergerak seragam. Ini bukti kontribusi 23 atribut terpilih dalam konfigurasi ini, bukan klaim tentang semua fitur sumber.

## C dikurangi B: perubahan protokol split

| model | direction | later | earlier | metric_partition | same_test_membership | same_feature_set | delta_accuracy_pp | delta_precision_pp | delta_recall_pp | delta_f1_pp | delta_roc_auc_pp | delta_fpr_pp | delta_fp_count | delta_fn_count | delta_samples_count | delta_training_seconds | delta_inference_ms_per_1024 | training_relative_change_percent | inference_relative_change_percent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LR | C minus B | C | B | test | False | True | -0.147627192 | -0.0175012632 | -0.29845818 | -0.160036032 | -0.0641328263 | 0.0142107097 | 3 | 56 | 923 | 0.25779 | -0.212900006 | 30.3112289 | -7.75196642 |
| RF | C minus B | C | B | test | False | True | -0.091881402 | 0.0360629211 | -0.231138021 | -0.0987154852 | -0.055227467 | -0.0253384302 | -5 | 42 | 923 | -0.1380068 | -0.546400013 | -2.29992271 | -5.47714528 |

B/C memakai 15 fitur identik. Namun train/validation/test dan komposisi kelas berubah. F1/recall menurun pada C untuk kedua model. LR FP naik3 dan FN naik56; RF FP turun5 dan FN naik42. Counts harus dibaca bersama denominator; FN C lebih banyak tidak boleh ditafsirkan tanpa FNR dan jumlah phishing. FPR LR naik, RF turun. Tidak dapat menyatakan pemisahan domain menyebabkan seluruh selisih secara kausal.

| split | bagian | baris | proporsi | sah | phishing | domain_unik | phishing_prevalence_percent |
|---|---|---|---|---|---|---|---|
| acak | uji | 35306 | 0.150002124 | 20228 | 15078 | 31495 | 42.7066221 |
| domain | uji | 36229 | 0.15392361 | 20485 | 15744 | 29657 | 43.4568992 |

## Kesalahan klasifikasi dan denominator

| model | scenario | samples | legitimate | phishing | tn | fp | fn | tp | total_errors | error_rate | FNR_percent | FPR_percent |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| LR | A | 35306 | 20228 | 15078 | 20218 | 10 | 12 | 15066 | 22 | 0.000623123548 | 0.079586152 | 0.0494364248 |
| LR | B | 35306 | 20228 | 15078 | 20221 | 7 | 204 | 14874 | 211 | 0.00597632131 | 1.35296458 | 0.0346054973 |
| LR | C | 36229 | 20485 | 15744 | 20475 | 10 | 260 | 15484 | 270 | 0.00745259323 | 1.65142276 | 0.048816207 |
| RF | A | 35306 | 20228 | 15078 | 20228 | 0 | 6 | 15072 | 6 | 0.000169942786 | 0.039793076 | 0 |
| RF | B | 35306 | 20228 | 15078 | 20213 | 15 | 127 | 14951 | 142 | 0.00402197927 | 0.842286775 | 0.0741546371 |
| RF | C | 36229 | 20485 | 15744 | 20475 | 10 | 169 | 15575 | 179 | 0.00494079329 | 1.0734248 | 0.048816207 |

error_analysis.csv berisi validation dan test. FNR=FN/jumlah phishing; FPR=FP/jumlah legitimate; error_rate=(FP+FN)/N. Kolom fn_share_all_samples/fp_share_all_samples memakai denominator N, sedangkan fn_share_errors/fp_share_errors memakai total error. Ini proporsi berbeda dan tidak saling dipertukarkan. Error didominasi FN. RF/A memiliki 6 FN dan 0 FP pada test, tetapi tidak membuktikan FPR populasi nol. B/C harus dibandingkan melalui rate serta denominator, bukan counts mentah saja.

## Efisiensi komputasi

| model | skenario | training_seconds | uji_batch_ms | batch_size | RF_minus_LR_training_seconds | RF_over_LR_training_ratio | RF_minus_LR_inference_ms | RF_over_LR_inference_ratio | measurement |
|---|---|---|---|---|---|---|---|---|---|
| LR | A | 2.396193 | 4.1047 | 1024 | 14.889308 | 7.21373487 | 6.73920001 | 2.64182523 | pipeline.fit seconds; inference median5, warmup1, batch1024, thread1; excludes URL extraction and page retrieval |
| LR | B | 0.8504769 | 2.7464 | 1024 | 5.1500204 | 7.05545007 | 7.2296 | 3.63239149 | pipeline.fit seconds; inference median5, warmup1, batch1024, thread1; excludes URL extraction and page retrieval |
| LR | C | 1.1082669 | 2.5335 | 1024 | 4.7542236 | 5.28978218 | 6.89609999 | 3.72196566 | pipeline.fit seconds; inference median5, warmup1, batch1024, thread1; excludes URL extraction and page retrieval |
| RF | A | 17.285501 | 10.8439 | 1024 | 14.889308 | 7.21373487 | 6.73920001 | 2.64182523 | pipeline.fit seconds; inference median5, warmup1, batch1024, thread1; excludes URL extraction and page retrieval |
| RF | B | 6.0004973 | 9.976 | 1024 | 5.1500204 | 7.05545007 | 7.2296 | 3.63239149 | pipeline.fit seconds; inference median5, warmup1, batch1024, thread1; excludes URL extraction and page retrieval |
| RF | C | 5.8624905 | 9.42959999 | 1024 | 4.7542236 | 5.28978218 | 6.89609999 | 3.72196566 | pipeline.fit seconds; inference median5, warmup1, batch1024, thread1; excludes URL extraction and page retrieval |

LR lebih cepat daripada RF pada setiap skenario untuk pipeline.fit dan batch inference. A lebih lambat daripada B untuk kedua model, disertai F1/recall lebih tinggi. RF mempertahankan F1/recall lebih tinggi dengan biaya komputasi lebih besar. Perubahan B/C tidak hanya terkait metode split: ukuran dan komposisi train berbeda. Semua waktu berasal dari satu run Tahap5, tidak diukur ulang. Inference median5/warmup1/thread1 pada batch1024; preprocessing pipeline dan predict_proba masuk, ekstraksi URL/pengambilan halaman tidak masuk. Jangan menyebut timing end-to-end atau keunggulan latency stabil di semua perangkat.

## Reproduksibilitas

Seluruh threshold, confusion counts dan metrik validation/test yang tersedia pada historical_comparison_full.csv memiliki selisih tepat nol dengan CSV historis. Waktu inference berbeda, selisih absolut maksimum 1.889 ms/batch. Training time historis tidak tersedia. Prediksi historis per record tidak tersedia; kesamaan statistik/threshold tidak membuktikan keanggotaan/prediksi historis identik. Python3.13.0 berbeda dari historis3.14.4; CPU/OS berbeda, lima versi paket utama tercatat sama. Tidak mengklaim reproducibility sempurna.

## Jawaban research question

| Pertanyaan penelitian | Bukti eksperimen | Nilai metrik | Interpretasi | Keterbatasan | Lokasi artefak pendukung |
|---|---|---|---|---|---|
| LR: bagaimana pembatasan fitur mengubah F1/recall/FPR? | B minus A, membership acak identik | F1 -0.631337 pp; recall -1.273378 pp; FPR -0.014831 pp | F1 dan recall turun ketika 23 atribut halaman terpilih dikeluarkan; arah FPR bergantung model. | Selected features; satu dataset/seed; tidak ada uji signifikansi. | scenario_deltas.csv; ../eksperimen_utama/metrik_utama.csv; ../split_membership.csv.gz |
| LR: bagaimana protokol domain mengubah F1/recall/FPR dengan fitur identik? | C minus B; 15 fitur identik, C nol irisan domain | F1 -0.160036 pp; recall -0.298458 pp; FPR +0.014211 pp | F1 dan recall turun pada realisasi split C; FPR LR naik, RF turun. | Test dan prevalensi berubah; bukan efek kausal domain yang terisolasi. | scenario_deltas.csv; ../hasil/ringkasan_split.csv; ../hasil/irisan_domain.csv |
| RF: bagaimana pembatasan fitur mengubah F1/recall/FPR? | B minus A, membership acak identik | F1 -0.452740 pp; recall -0.802494 pp; FPR +0.074155 pp | F1 dan recall turun ketika 23 atribut halaman terpilih dikeluarkan; arah FPR bergantung model. | Selected features; satu dataset/seed; tidak ada uji signifikansi. | scenario_deltas.csv; ../eksperimen_utama/metrik_utama.csv; ../split_membership.csv.gz |
| RF: bagaimana protokol domain mengubah F1/recall/FPR dengan fitur identik? | C minus B; 15 fitur identik, C nol irisan domain | F1 -0.098715 pp; recall -0.231138 pp; FPR -0.025338 pp | F1 dan recall turun pada realisasi split C; FPR LR naik, RF turun. | Test dan prevalensi berubah; bukan efek kausal domain yang terisolasi. | scenario_deltas.csv; ../hasil/ringkasan_split.csv; ../hasil/irisan_domain.csv |

## Keterbatasan dan batas klaim

Lihat LIMITATIONS.md untuk ketimpangan struktur kelas, shortcut potensial, satu dataset/seed, selected features, perubahan komposisi B/C, provenance yang belum lengkap, timing, kesamaan historis terbatas dan status baseline. Tidak ada bukti baru leakage terkonfirmasi dan tidak ada dasar klaim signifikansi statistik.

## Integritas, artefak dan pengulangan analisis

Seluruh output tahap ini berada di analysis/. Notebook analysis_results.ipynb menyimpan source dan hasil eksekusi, dapat dijalankan dengan cwd analysis dan interpreter .venv tanpa training ulang. Ia membaca metrik/prediksi lama dan menulis ulang hanya output analysis. Root notebook, dataset, hasil historis dan hasil eksperimen tidak diubah. Snapshot checksum sebelum/sesudah dicatat pada validation_manifest.json oleh orkestrator.

File baru: ANALYSIS_REPORT.md, RESEARCH_QUESTION_ANSWERS.md, LIMITATIONS.md, performance_comparison.csv, scenario_deltas.csv, error_analysis.csv, efficiency_analysis.csv, CLAIM_EVIDENCE_MATRIX.md, analysis_results.ipynb, serta validation_manifest.json sebagai bukti validasi/integritas. Tidak commit/push.

## Rekomendasi visualisasi tahap berikutnya

1. Plot titik F1/recall/FPR per model dan A/B/C, dengan sumbu FPR terpisah agar skala kecil terbaca. Hindari error bar karena ketidakpastian belum diestimasi.
2. Plot delta B-A dan C-B dalam pp, pisahkan panel dan beri catatan test B/C berbeda; bukan diagram efek kausal.
3. Confusion matrix dengan count serta normalisasi menurut kelas aktual. Tampilkan N legitimate/phishing pada tiap panel.
4. Plot F1 versus batch inference time dengan label konfigurasi; nyatakan satu run, non-end-to-end, tanpa klaim benchmark perangkat universal.
5. Diagram komposisi test B/C dan irisan domain historis sebagai konteks interpretasi. Tidak menambah subgroup evaluasi model.

Satu pekerjaan berikutnya: review hasil dan batas klaim bersama tim untuk menyepakati baseline selected features dan bentuk visualisasi pelaporan; tidak perlu training baru hanya untuk mengejar angka historis.
