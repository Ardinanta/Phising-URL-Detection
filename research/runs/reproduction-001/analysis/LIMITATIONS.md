# Keterbatasan dan Batas Klaim

Tahap6 menganalisis artefak tersimpan tanpa training/tuning atau perubahan fitur/split.
## Struktur kelas tidak seimbang

Seluruh 134850 legitimate mentah adalah akar; path/query hanya phishing. Panjang path/query dapat menjadi shortcut korpus. Ini potensi shortcut learning, bukan bukti mekanisme yang dipelajari setiap model atau leakage terkonfirmasi.

Bukti: ../hasil/audit_struktur_mentah.csv baris 2-4.

## Satu dataset

Domain baru dalam PhiUSIIL tidak membuktikan generalisasi lintas sumber, waktu atau deployment. FPR hanya mewakili jenis legitimate yang tersedia.

Bukti: ../hasil/ringkasan_split.csv; ../hasil/audit_struktur_mentah.csv.

## Satu seed

Seed42 menghasilkan satu realisasi split/model. Tidak ada pengulangan seed, interval ketidakpastian atau pengujian signifikansi pada tahap ini. Selisih dilaporkan deskriptif.

Bukti: ../eksperimen_utama/manifest_eksperimen.json seed.

## Baseline selected features

A memakai 15 leksikal+23 atribut halaman terpilih, bukan seluruh fitur sumber atau seluruh fitur relevan yang terbukti lengkap. Hasil A/B terbatas pada penambahan 23 atribut tersebut.

Bukti: ../../../docs/audit/FEATURE_AUDIT.md; ../eksperimen_utama/actual_parameters.json.

## Komposisi B/C berbeda

Test B=35306, phishing15078, legitimate20228; C=36229, phishing15744, legitimate20485. Membership/protokol berbeda; jangan mengatribusikan semua perubahan kepada domain secara kausal atau membandingkan counts tanpa denominator.

Bukti: ../hasil/ringkasan_split.csv baris 4 dan 7; ../split_membership.csv.gz.

## Provenance belum lengkap

Versi/tanggal unduh/lisensi salinan Kaggle dan definisi upstream beberapa fitur belum lengkap. Skor statistik yang dikeluarkan tidak otomatis menyebabkan leakage; eksklusi konservatif dan cakupan eksperimen harus dibedakan.

Bukti: ../../../docs/audit/feature_registry.csv; ../../../docs/audit/FEATURE_AUDIT.md.

## Pengukuran waktu

Satu run, satu perangkat, median5 pada batch1024. Train pipeline.fit; inferensi mencakup preprocessing/predict_proba tetapi mengecualikan ekstraksi URL dan pengambilan halaman. Bukan latensi end-to-end atau benchmark stabilitas. Tidak ada distribusi lima waktu mentah tersimpan.

Bukti: ../eksperimen_utama/manifest_eksperimen.json; ../eksperimen_utama/metrik_utama.csv.

## Kesamaan historis terbatas

Threshold, confusion counts dan metrik agregat cocok tepat pada CSV. Prediksi/membership historis per record tidak tersedia; tidak dapat mengklaim kesamaan per record atau reproducibility sempurna. Python/perangkat berbeda.

Bukti: ../eksperimen_utama/historical_comparison_full.csv; ../EXPERIMENT_REPORT.md.

## Persetujuan baseline

Otorisasi training pengguna hanya untuk reproduksi historis. Persetujuan final baseline seluruh tim masih menunggu.

Bukti: ../../../docs/audit/BASELINE_DECISION.md; ../stage5_execution/authorization.json.

## Validation versus test

Threshold memaksimalkan F1 validation; F1 validation pada threshold terpilih merupakan hasil seleksi pada validation, bukan estimasi independen. Test tidak dipakai memilih threshold, fitur atau parameter dalam runner.

Bukti: ../02_Eksperimen_Utama.executed.ipynb cell 4-5.

## Tidak ada hasil subgroup baru

Tahap6 tidak menambah subgroup/reweighting. Counts struktur mentah digunakan hanya untuk membatasi interpretasi dataset, bukan mengevaluasi subgroup model baru.

Bukti: analysis_results.ipynb; ../hasil/audit_struktur_mentah.csv.

Tidak ada dasar untuk menyebut perbedaan signifikan secara statistik. Tidak ada bukti baru yang mengonfirmasi data leakage. Tidak mengklaim model terbaik untuk seluruh kondisi operasional.
