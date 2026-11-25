# Matriks Klaim dan Bukti

| Klaim | Lokasi bukti | Nilai/field pendukung | Batas klaim |
|---|---|---|---|
| RF mempunyai F1/recall lebih tinggi dari LR di A/B/C | performance_comparison.csv; ../eksperimen_utama/metrik_utama.csv | RF_minus_LR_test_f1_pp dan recall_pp | Deskriptif pada enam hasil ini; RF B memiliki FPR lebih tinggi dari LR B. |
| Pembatasan fitur B minus A menurunkan F1/recall kedua model | scenario_deltas.csv; ../split_membership.csv.gz | Dua baris B minus A; membership prediksi A/B diperiksa sama | Tidak berarti semua fitur halaman sumber diperlukan; hanya 23 atribut terpilih dibandingkan. |
| C minus B menurunkan F1/recall pada run ini | scenario_deltas.csv; ../hasil/ringkasan_split.csv | Dua baris C minus B | Membership/prevalensi berubah; bukan kausalitas domain mutlak. |
| C memiliki nol irisan domain antarsplit | ../hasil/irisan_domain.csv; ../split_membership.csv.gz | Baris domain: ketiga pasangan 0 | Definisi PSL private dan fallback sesuai Tahap4; bukan generalisasi lintas korpus. |
| FPR LR turun A->B lalu naik B->C; RF sebaliknya | scenario_deltas.csv; error_analysis.csv | delta_fpr_pp, fp/legitimate | Jumlah FP kecil; tidak disertai ketidakpastian; zero FP RF/A bukan jaminan FPR populasi nol. |
| RF/A menghasilkan kesalahan test paling sedikit | error_analysis.csv | Test RF/A: FP0, FN6, N35306 | Bukan bukti performa populasi sempurna atau keunggulan signifikan. |
| LR lebih cepat pada training dan inferensi di tiap skenario | efficiency_analysis.csv | RF_over_LR ratios >1 | Hanya satu pengukuran run; waktu bukan end-to-end. |
| Agregat dan threshold sama dengan historis, timing berbeda | ../eksperimen_utama/historical_comparison_full.csv | Seluruh non-timing absolute_difference=0 | Tidak membuktikan kesamaan prediksi historis per record. |
| Semua legitimate mentah pada struktur akar | ../hasil/audit_struktur_mentah.csv | Akar134850, path0, query0 legitimate | Potensi shortcut dataset, bukan leakage terkonfirmasi. |
| Tidak ada klaim signifikansi statistik | LIMITATIONS.md | Tidak ada uji signifikansi/interval/pengulangan seed | Perbedaan hanya deskriptif. |
| Integritas input dan hasil lama terjaga | validation_manifest.json | Checksum inventory dan snapshot before/after | Tidak ada training atau modifikasi metrik sumber. |
| Keputusan baseline belum disetujui seluruh tim | ../../../docs/audit/BASELINE_DECISION.md; ../stage5_execution/authorization.json | Status pending; otorisasi training terpisah | Dokumen analisis tidak menetapkan metode baru. |

Tabel jawaban RQ yang memuat nilai aktual tersedia di RESEARCH_QUESTION_ANSWERS.md. Semua path relatif terhadap direktori analysis.
