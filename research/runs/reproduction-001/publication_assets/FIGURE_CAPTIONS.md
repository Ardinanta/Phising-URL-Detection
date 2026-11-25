# Caption Gambar Ilmiah

## fig_01_methodology_flow

Alur metodologi konfigurasi historis P1. Ekstraksi leksikal deterministik mendahului split; seluruh praproses yang memerlukan fit hanya menggunakan train. Validation memilih ambang dan test mengevaluasi ambang beku.

Satuan: Baris, kolom, jumlah fitur.
Sumber (relatif run): hasil/manifest_data.json; 01_Audit_dan_Split.ipynb cell 2/4/6; 02_Eksperimen_Utama.ipynb cell 3–6.
Batas interpretasi: Diagram mendeskripsikan konfigurasi yang direproduksi; persetujuan baseline tim masih menunggu.
Rekomendasi bagian: Methods.

## fig_02_experimental_scenarios

Tiga skenario eksperimen dengan selected features. B − A mengubah cakupan fitur; C − B mengubah protokol serta keanggotaan data, dengan fitur leksikal tetap.

Satuan: Jumlah fitur.
Sumber (relatif run): analysis/performance_comparison.csv; eksperimen_utama/actual_parameters.json.
Batas interpretasi: A bukan seluruh fitur PhiUSIIL; C − B bukan efek kausal domain yang terisolasi.
Rekomendasi bagian: Methods.

## fig_03_f1_comparison

Perbandingan F1 test LR dan RF pada A/B/C. Sumbu Y diperbesar ke 99,0–100,08%; tidak dimulai dari nol.

Satuan: Persen (%).
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: Point plot tanpa error bar. B/C memakai test berbeda; satu seed.
Rekomendasi bagian: Results.

## fig_04_recall_comparison

Perbandingan Recall phishing test LR dan RF pada A/B/C. Sumbu Y diperbesar ke 98,0–100,08%; tidak dimulai dari nol.

Satuan: Persen (%).
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: Point plot tanpa error bar. B/C memakai test berbeda; satu seed.
Rekomendasi bagian: Results.

## fig_05_fpr_comparison

Perbandingan FPR test LR dan RF pada A/B/C. FPR ditampilkan pada panel terpisah dengan sumbu Y mulai nol.

Satuan: Persen (%).
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: Point plot tanpa error bar. B/C memakai test berbeda; satu seed.
Rekomendasi bagian: Results.

## fig_06_scenario_deltas

Perubahan F1, recall dan FPR: B dikurangi A serta C dikurangi B. Tanda menunjukkan arah perubahan terhadap skenario awal; garis horizontal menandai nol.

Satuan: Poin persentase (pp).
Sumber (relatif run): analysis/scenario_deltas.csv.
Batas interpretasi: pp bukan perubahan relatif persen. B/C berbeda dalam komposisi dan membership test; tidak ada klaim kausal atau signifikansi.
Rekomendasi bagian: Results.

## fig_07a_confusion_matrix_counts

Confusion matrix enam konfigurasi test; baris adalah kelas aktual, kolom kelas prediksi. Count aktual ditulis pada setiap sel; rentang warna bersama 0–20.500 record.

Satuan: Jumlah record.
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/error_analysis.csv.
Batas interpretasi: N₀ legitimate dan N₁ phishing tercantum per panel. Nol FP tidak membuktikan FPR populasi nol; test C berbeda dari A/B.
Rekomendasi bagian: Results.

## fig_07b_confusion_matrix_normalized

Confusion matrix enam konfigurasi test; baris adalah kelas aktual, kolom kelas prediksi. Normalisasi per baris menggunakan denominator kelas aktual; rentang warna bersama 0–100%.

Satuan: Persen kelas aktual (%).
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/error_analysis.csv.
Batas interpretasi: N₀ legitimate dan N₁ phishing tercantum per panel. Nol FP tidak membuktikan FPR populasi nol; test C berbeda dari A/B.
Rekomendasi bagian: Results.

## fig_08a_training_time

Waktu training pipeline.fit per konfigurasi pada perangkat reproduksi yang sama.

Satuan: Detik.
Sumber (relatif run): analysis/efficiency_analysis.csv; eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: Satu run/perangkat. Inferensi median5 setelah warm-up1, thread1; ekstraksi URL dan pengambilan halaman tidak tercakup. Bukan end-to-end.
Rekomendasi bagian: Results.

## fig_08b_inference_time

Waktu inferensi pipeline per konfigurasi pada perangkat reproduksi yang sama.

Satuan: ms per 1.024 sampel.
Sumber (relatif run): analysis/efficiency_analysis.csv; eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: Satu run/perangkat. Inferensi median5 setelah warm-up1, thread1; ekstraksi URL dan pengambilan halaman tidak tercakup. Bukan end-to-end.
Rekomendasi bagian: Results.

## fig_09_f1_efficiency_tradeoff

Hubungan deskriptif antara F1 test dan waktu inferensi enam konfigurasi. Sumbu Y diperbesar ke 99,0–100,12%.

Satuan: F1 persen (%); inferensi ms / 1.024 sampel.
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/efficiency_analysis.csv.
Batas interpretasi: Satu perangkat/run; bukan end-to-end. Tidak ada garis frontier atau klaim model terbaik universal; test C berbeda.
Rekomendasi bagian: Results.

## fig_10_url_structure_distribution

Distribusi struktur URL sebelum deduplikasi. Seluruh 134.850 legitimate berada pada akar; kelompok path/query hanya berisi phishing pada salinan ini.

Satuan: Jumlah record mentah.
Sumber (relatif run): hasil/audit_struktur_mentah.csv.
Batas interpretasi: Ketimpangan struktur menunjukkan potensi shortcut dataset, bukan leakage terkonfirmasi.
Rekomendasi bagian: Discussion.

## fig_11_domain_overlap

Jumlah irisan domain terdaftar pada tiga pasangan bagian. Split C memiliki nol irisan pada seluruh pasangan; split acak memiliki irisan nonnol.

Satuan: Jumlah domain.
Sumber (relatif run): hasil/irisan_domain.csv.
Batas interpretasi: Domain mengikuti tldextract5.3.1, private suffix aktif, fallback host untuk IP/suffix tak dikenal. Nol irisan tidak membuktikan generalisasi lintas korpus.
Rekomendasi bagian: Results.

## fig_12_roc_curves

Kurva ROC test dari probabilitas aktual per record, dipisah menurut A/B/C. Garis LR/RF dapat bertumpuk karena AUC mendekati satu; sumbu penuh 0–100% dipertahankan.

Satuan: FPR dan TPR persen (%); AUC proporsi 0–1.
Sumber (relatif run): eksperimen_utama/predictions/*_uji.csv.gz; eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: C memiliki membership test berbeda. Kurva bukan rekonstruksi dari satu nilai AUC; tidak ada interval ketidakpastian.
Rekomendasi bagian: Results.
