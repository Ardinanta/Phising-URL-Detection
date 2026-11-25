# Jawaban Research Question Berdasarkan Bukti

RQ tetap: bagaimana F1 kelas phishing, recall dan FPR LR/RF berubah ketika fitur dibatasi menjadi leksikal URL dan test dipisahkan berdasarkan domain terdaftar?

Semua selisih dihitung presisi penuh; pp berarti poin persentase, yaitu 100 x selisih proporsi. Pembulatan hanya penyajian.

| Pertanyaan penelitian | Bukti eksperimen | Nilai metrik | Interpretasi | Keterbatasan | Lokasi artefak pendukung |
|---|---|---|---|---|---|
| LR: bagaimana pembatasan fitur mengubah F1/recall/FPR? | B minus A, membership acak identik | F1 -0.631337 pp; recall -1.273378 pp; FPR -0.014831 pp | F1 dan recall turun ketika 23 atribut halaman terpilih dikeluarkan; arah FPR bergantung model. | Selected features; satu dataset/seed; tidak ada uji signifikansi. | scenario_deltas.csv; ../eksperimen_utama/metrik_utama.csv; ../split_membership.csv.gz |
| LR: bagaimana protokol domain mengubah F1/recall/FPR dengan fitur identik? | C minus B; 15 fitur identik, C nol irisan domain | F1 -0.160036 pp; recall -0.298458 pp; FPR +0.014211 pp | F1 dan recall turun pada realisasi split C; FPR LR naik, RF turun. | Test dan prevalensi berubah; bukan efek kausal domain yang terisolasi. | scenario_deltas.csv; ../hasil/ringkasan_split.csv; ../hasil/irisan_domain.csv |
| RF: bagaimana pembatasan fitur mengubah F1/recall/FPR? | B minus A, membership acak identik | F1 -0.452740 pp; recall -0.802494 pp; FPR +0.074155 pp | F1 dan recall turun ketika 23 atribut halaman terpilih dikeluarkan; arah FPR bergantung model. | Selected features; satu dataset/seed; tidak ada uji signifikansi. | scenario_deltas.csv; ../eksperimen_utama/metrik_utama.csv; ../split_membership.csv.gz |
| RF: bagaimana protokol domain mengubah F1/recall/FPR dengan fitur identik? | C minus B; 15 fitur identik, C nol irisan domain | F1 -0.098715 pp; recall -0.231138 pp; FPR -0.025338 pp | F1 dan recall turun pada realisasi split C; FPR LR naik, RF turun. | Test dan prevalensi berubah; bukan efek kausal domain yang terisolasi. | scenario_deltas.csv; ../hasil/ringkasan_split.csv; ../hasil/irisan_domain.csv |

Kesimpulan deskriptif: fitur halaman terpilih memberi skor F1/recall lebih tinggi pada split A/B yang sama. Dengan fitur leksikal tetap, split C menunjukkan F1/recall lebih rendah dari B pada run ini. FPR tidak bergerak seragam. Tidak ada klaim kausal mutlak atau signifikansi statistik.

Status baseline tim tetap menunggu persetujuan; otorisasi reproduksi tidak menggantikannya.
