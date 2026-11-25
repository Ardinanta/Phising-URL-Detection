# Caption Tabel Ilmiah

## table_01_dataset_summary

Ringkasan audit dataset mentah dan setelah deduplikasi.

Satuan: Jumlah record/kolom/URL.
Sumber (relatif run): hasil/manifest_data.json; hasil/audit_struktur_mentah.csv.
Batas interpretasi: Label asli0 phishing,1 legitimate; target model membalik phishing menjadi1. Provenance versi Kaggle belum lengkap.
Rekomendasi bagian: Methods.

## table_02_experimental_scenarios

Definisi skenario historis yang direproduksi.

Satuan: Jumlah fitur.
Sumber (relatif run): eksperimen_utama/actual_parameters.json; analysis/performance_comparison.csv.
Batas interpretasi: A adalah selected features; persetujuan final baseline tim masih menunggu.
Rekomendasi bagian: Methods.

## table_03_split_distribution

Ukuran, distribusi kelas dan domain unik setiap bagian.

Satuan: Record, domain, persen (%).
Sumber (relatif run): hasil/ringkasan_split.csv.
Batas interpretasi: Target70/15/15; rasio domain-grouped diarahkan pada kelompok domain sehingga rasio baris berbeda.
Rekomendasi bagian: Methods.

## table_04_domain_overlap

Irisan domain antarbagiannya dan proporsi record bagian kedua yang domainnya termasuk irisan.

Satuan: Jumlah domain; persen (%).
Sumber (relatif run): hasil/irisan_domain.csv.
Batas interpretasi: Proporsi bukan persentase domain. Private suffix dan fallback mengikuti implementasi historis.
Rekomendasi bagian: Results.

## table_05_model_parameters

Parameter estimator aktual dan aturan pipeline/evaluasi.

Satuan: Nilai parameter; batch dan pengulangan.
Sumber (relatif run): eksperimen_utama/actual_parameters.json; eksperimen_utama/manifest_eksperimen.json.
Batas interpretasi: Semua parameter default estimator aktual dicatat; fit hanya train, threshold hanya validation.
Rekomendasi bagian: Methods.

## table_06_test_performance

Performa test enam konfigurasi. CSV memakai presisi penuh; Markdown enam angka desimal pada persen.

Satuan: Metrik persen (%); threshold proporsi.
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv.
Batas interpretasi: Nol FP/FPR sampel tidak membuktikan FPR populasi nol; test C berbeda.
Rekomendasi bagian: Results.

## table_07_scenario_deltas

Selisih B minus A dan C minus B dengan arah dan satuan eksplisit pada nama kolom.

Satuan: pp untuk metrik; record untuk FP/FN; detik training; ms/1024 inferensi.
Sumber (relatif run): analysis/scenario_deltas.csv.
Batas interpretasi: pp bukan persen relatif. C/B berbeda dalam membership dan komposisi test; tidak ada klaim kausal.
Rekomendasi bagian: Results.

## table_08_confusion_matrix

Confusion counts test dan denominator setiap kelas.

Satuan: Jumlah record.
Sumber (relatif run): eksperimen_utama/metrik_utama.csv; analysis/performance_comparison.csv; analysis/error_analysis.csv.
Batas interpretasi: Counts B/C tidak dibandingkan tanpa denominator. Nol FP bukan jaminan populasi.
Rekomendasi bagian: Results.

## table_09_computational_efficiency

Waktu training dan inferensi aktual serta rasio RF terhadap LR pada skenario sama.

Satuan: Detik; ms/1024; rasio.
Sumber (relatif run): analysis/efficiency_analysis.csv.
Batas interpretasi: Satu perangkat/run, bukan end-to-end; rasio sama diulang pada kedua model untuk konteks.
Rekomendasi bagian: Results.

## table_10_reproducibility

Ringkasan pembandingan presisi penuh dengan hasil historis dan batas bukti per record.

Satuan: Selisih proporsi/count; timing ms/1024; versi environment.
Sumber (relatif run): eksperimen_utama/historical_comparison_full.csv; eksperimen_utama/manifest_eksperimen.json.
Batas interpretasi: Tidak mengklaim reproducibility sempurna; tidak ada training time historis untuk dibandingkan.
Rekomendasi bagian: Discussion.

