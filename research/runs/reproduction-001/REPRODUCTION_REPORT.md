# Reproduction Report - reproduction-001

Tanggal: 2026-11-25T17:31:02.230566+07:00. Reproduksi konfigurasi historis saja; persetujuan final baseline tetap menunggu tim. Notebook kedua dan training tidak dijalankan.

## Isolasi dan input

Working directory kernel diverifikasi melalui preflight: `[REPOSITORY_ROOT]\runs\reproduction-001`. Output `[REPOSITORY_ROOT]\runs\reproduction-001\hasil` awalnya kosong. Input notebook dan dataset disalin byte-identik; checksum sebelum eksekusi tersimpan pada run_manifest.json. Salinan notebook asli dipertahankan; hasil eksekusi disimpan terpisah sebagai 01_Audit_dan_Split.executed.ipynb. Tidak ada hasil historis dipakai sebagai input eksekusi. Hasil historis hanya dibaca sesudahnya untuk pembandingan.

Branch develop, commit d80117b50f179cfefe91f1c138706264a2934cc7. Interpreter `[REPOSITORY_ROOT]\.venv\Scripts\python.exe`, Python 3.13.0. Paket: {"numpy": "2.5.2", "pandas": "3.0.5", "scikit-learn": "1.9.1", "matplotlib": "3.11.1", "tldextract": "5.3.1", "threadpoolctl": "3.8.0", "ipykernel": "7.4.0"}. OS Windows-11-10.0.26200-SP0; CPU AMD64 Family 23 Model 160 Stepping 0, AuthenticAMD; RAM 7817785344 byte. Seed 42.

## Hasil setiap cell

| Cell | Jenis | Status | Detik | Execution count |
|---|---|---|---|---|
| 1 | markdown | MARKDOWN preserved | - | - |
| 2 | code | PASS | 6.55 | 2 |
| 3 | markdown | MARKDOWN preserved | - | - |
| 4 | code | PASS | 10.604 | 3 |
| 5 | markdown | MARKDOWN preserved | - | - |
| 6 | code | PASS | 19.668 | 4 |

Kernel bersih menjalankan preflight sebelum cell penelitian. Karena preflight memakai satu execution count, cell kode pertama dapat bernomor 2. Isi source cell tidak diubah; Markdown dipertahankan.

## Perbandingan hasil historis dan reproduksi

| Aspek diuji | Historis | Reproduksi | Selisih | Status | Keterangan |
|---|---|---|---|---|---|
| baris mentah | 235795 | 235795 | 0 | cocok |  |
| kolom asli | 56 | 56 | 0 | cocok |  |
| phishing mentah | 100945 | 100945 | 0 | cocok |  |
| legitimate mentah | 134850 | 134850 | 0 | cocok |  |
| URL unik | 235370 | 235370 | 0 | cocok |  |
| pengulangan teks URL | 425 | 425 | 0 | cocok |  |
| konflik label URL | 0 | 0 | 0 | cocok |  |
| baris bersih | 235370 | 235370 | 0 | cocok |  |
| phishing bersih | 100520 | 100520 | 0 | cocok |  |
| legitimate bersih | 134850 | 134850 | 0 | cocok |  |
| fitur leksikal | 15 | 15 | 0 | cocok |  |
| atribut halaman | 23 | 23 | 0 | cocok |  |
| tabel ringkasan_split.csv | seluruh nilai historis | seluruh nilai historis | - | cocok | Toleransi numerik absolut 1e-12; urutan baris diperiksa |
| tabel irisan_domain.csv | seluruh nilai historis | seluruh nilai historis | - | cocok | Toleransi numerik absolut 1e-12; urutan baris diperiksa |
| tabel audit_struktur_mentah.csv | seluruh nilai historis | seluruh nilai historis | - | cocok | Toleransi numerik absolut 1e-12; urutan baris diperiksa |
| tabel distribusi_struktur_split.csv | seluruh nilai historis | seluruh nilai historis | - | cocok | Toleransi numerik absolut 1e-12; urutan baris diperiksa |
| acak/latih/baris | 164759.0 | 164759.0 | 0.0 | cocok |  |
| acak/latih/proporsi | 0.7 | 0.7 | 0.0 | cocok |  |
| acak/latih/sah | 94395.0 | 94395.0 | 0.0 | cocok |  |
| acak/latih/phishing | 70364.0 | 70364.0 | 0.0 | cocok |  |
| acak/latih/domain_unik | 140191.0 | 140191.0 | 0.0 | cocok |  |
| acak/validasi/baris | 35305.0 | 35305.0 | 0.0 | cocok |  |
| acak/validasi/proporsi | 0.1499978756850915 | 0.1499978756850915 | 0.0 | cocok |  |
| acak/validasi/sah | 20227.0 | 20227.0 | 0.0 | cocok |  |
| acak/validasi/phishing | 15078.0 | 15078.0 | 0.0 | cocok |  |
| acak/validasi/domain_unik | 31418.0 | 31418.0 | 0.0 | cocok |  |
| acak/uji/baris | 35306.0 | 35306.0 | 0.0 | cocok |  |
| acak/uji/proporsi | 0.1500021243149084 | 0.1500021243149084 | 0.0 | cocok |  |
| acak/uji/sah | 20228.0 | 20228.0 | 0.0 | cocok |  |
| acak/uji/phishing | 15078.0 | 15078.0 | 0.0 | cocok |  |
| acak/uji/domain_unik | 31495.0 | 31495.0 | 0.0 | cocok |  |
| domain/latih/baris | 164785.0 | 164785.0 | 0.0 | cocok |  |
| domain/latih/proporsi | 0.7001104643752389 | 0.7001104643752389 | 0.0 | cocok |  |
| domain/latih/sah | 94076.0 | 94076.0 | 0.0 | cocok |  |
| domain/latih/phishing | 70709.0 | 70709.0 | 0.0 | cocok |  |
| domain/latih/domain_unik | 138396.0 | 138396.0 | 0.0 | cocok |  |
| domain/validasi/baris | 34356.0 | 34356.0 | 0.0 | cocok |  |
| domain/validasi/proporsi | 0.1459659259888686 | 0.1459659259888686 | 0.0 | cocok |  |
| domain/validasi/sah | 20289.0 | 20289.0 | 0.0 | cocok |  |
| domain/validasi/phishing | 14067.0 | 14067.0 | 0.0 | cocok |  |
| domain/validasi/domain_unik | 29656.0 | 29656.0 | 0.0 | cocok |  |
| domain/uji/baris | 36229.0 | 36229.0 | 0.0 | cocok |  |
| domain/uji/proporsi | 0.1539236096358924 | 0.1539236096358924 | 0.0 | cocok |  |
| domain/uji/sah | 20485.0 | 20485.0 | 0.0 | cocok |  |
| domain/uji/phishing | 15744.0 | 15744.0 | 0.0 | cocok |  |
| domain/uji/domain_unik | 29657.0 | 29657.0 | 0.0 | cocok |  |
| irisan acak/latih/validasi | 2576 | 2576 | 0 | cocok |  |
| irisan acak/latih/uji | 2581 | 2581 | 0 | cocok |  |
| irisan acak/validasi/uji | 1184 | 1184 | 0 | cocok |  |
| irisan domain/latih/validasi | 0 | 0 | 0 | cocok |  |
| irisan domain/latih/uji | 0 | 0 | 0 | cocok |  |
| irisan domain/validasi/uji | 0 | 0 | 0 | cocok |  |
| checksum CSV | a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6 | a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6 | - | cocok |  |
| Python | 3.14.4 | 3.13.0 | - | tidak cocok | Perbedaan environment yang diketahui; tidak mengubah definisi atau seed |
| versi numpy | 2.5.2 | 2.5.2 | - | cocok |  |
| versi pandas | 3.0.5 | 3.0.5 | - | cocok |  |
| versi scikit-learn | 1.9.1 | 1.9.1 | - | cocok |  |
| versi tldextract | 5.3.1 | 5.3.1 | - | cocok |  |
| Keanggotaan historis per baris | Artefak per baris tidak tersedia | Membership baru disimpan | - | belum dapat diverifikasi | Kesamaan statistik agregat tidak membuktikan membership historis identik |

## Validasi independen

Pemeriksaan berjalan dalam proses host terpisah dari kernel, membaca kembali CSV dan fitur internal; tidak memakai variabel atau fungsi notebook yang sedang dieksekusi. Rumus leksikal dan aturan domain diterapkan ulang sesuai definisi historis; ini validasi implementasi, bukan metode penelitian baru. Membership disimpan per URL unik menggunakan ID record sumber dan SHA-256 URL. Tidak ada URL mentah dalam laporan atau membership.

| Pemeriksaan | Status | Bukti/rincian |
|---|---|---|
| schema_internal | PASS | {'rows': 235370, 'columns': 42, 'lexical': 15, 'page': 23} |
| internal_rows_labels | PASS | Label positif 1 tepat untuk label asli 0; baris mengikuti urutan deduplikasi keep-first |
| page_features_integrity | PASS | Seluruh 23 kolom dibandingkan dengan CSV deduplikasi |
| missing_model_inputs | PASS | Tidak ada missing pada fitur/target/penanda split aktual |
| lexical_all_rows | PASS | 15 fitur dihitung ulang pada seluruh URL unik secara terpisah dari kernel |
| structure_all_rows | PASS | Query nonkosong diprioritaskan, lalu segmen path, lalu akar |
| unique_stable_ids | PASS | SHA-256 UTF-8 teks URL asli unik; tidak mencetak URL mentah |
| acak_exactly_once | PASS | Setiap ID baris teralokasi tepat sekali; tidak ada bagian tidak dikenal/missing |
| acak_latih_both_classes | PASS | Kedua kelas ada |
| acak_validasi_both_classes | PASS | Kedua kelas ada |
| acak_uji_both_classes | PASS | Kedua kelas ada |
| acak_latih_validasi_disjoint_urls_rows | PASS | {'url_overlap': 0, 'row_overlap': 0} |
| acak_latih_uji_disjoint_urls_rows | PASS | {'url_overlap': 0, 'row_overlap': 0} |
| acak_validasi_uji_disjoint_urls_rows | PASS | {'url_overlap': 0, 'row_overlap': 0} |
| domain_exactly_once | PASS | Setiap ID baris teralokasi tepat sekali; tidak ada bagian tidak dikenal/missing |
| domain_latih_both_classes | PASS | Kedua kelas ada |
| domain_validasi_both_classes | PASS | Kedua kelas ada |
| domain_uji_both_classes | PASS | Kedua kelas ada |
| domain_latih_validasi_disjoint_urls_rows | PASS | {'url_overlap': 0, 'row_overlap': 0} |
| domain_latih_validasi_zero_domains | PASS | {'domain_overlap': 0} |
| domain_latih_uji_disjoint_urls_rows | PASS | {'url_overlap': 0, 'row_overlap': 0} |
| domain_latih_uji_zero_domains | PASS | {'domain_overlap': 0} |
| domain_validasi_uji_disjoint_urls_rows | PASS | {'url_overlap': 0, 'row_overlap': 0} |
| domain_validasi_uji_zero_domains | PASS | {'domain_overlap': 0} |
| independent_summary_matches | PASS | Agregat dihitung dari membership dan domain ekstraksi independen |
| independent_overlap_matches | PASS | Irisan dan proporsi dibandingkan artefak notebook |
| A_B_membership_design | PASS | Config N2 cell 6 dan filter N2 cell 4 menggunakan kolom split acak yang sama; notebook 2 tidak dijalankan |
| B_C_identical_features | PASS | Pemeriksaan AST N2 cell 6; 15 fitur identik |
| manifest_feature_lists | PASS | Daftar dan urutan sesuai kode salinan identik |
| manifest_audit | PASS | Dihitung ulang dari CSV lokal |
| raw_structure_counts | PASS | Seluruh baris mentah, termasuk URL berulang, dihitung ulang |
| historical_files_unchanged | PASS | {'files': 25, 'changed': []} |

Definisi domain: tldextract 5.3.1, snapshot PSL bawaan, private suffix aktif, tanpa pembaruan jaringan, cache_dir=None; hostname dibuang titik akhirnya lalu IDNA ASCII. IP memakai host utuh; suffix tak dikenal juga fallback host. Hitungan fallback/private: {"tldextract": "5.3.1", "private_suffix": true, "network_suffix_urls": [], "cache_dir": null, "ip_fallback_rows": 606, "unknown_suffix_fallback_rows": 766, "private_suffix_rows": 26790, "normalization": "hostname rstrip dot then IDNA ASCII; top_domain_under_public_suffix or full host"}.

A/B memakai satu kolom acak pada artefak baru dan konfigurasi N2 cell 6; membership identik secara desain untuk run baru. N2 tidak dieksekusi. Tidak ada artefak keanggotaan historis per baris, sehingga kesamaan historis per baris tetap belum dapat diverifikasi meskipun seluruh statistik agregat cocok.

## Missing values, fitur, dan label

Pandas default NA pada seluruh 56 kolom: {}. Pembacaan literal keep_default_na=False pada Title/TLD menemukan string kosong: {}. Perbedaan parser missing bukan bukti hilangnya data baru; makna semantik token belum terverifikasi. Model input terpilih, target dan penanda split diperiksa tidak missing. Label positif diturunkan dari label asli 0. Fitur internal berukuran 235370 baris x 42 kolom: target, 23 halaman, struktur, 15 leksikal, dan dua penanda split. Domain tidak disimpan dalam cache historis; untuk validasi domain direkonstruksi dan hanya hash-nya disimpan.

SHA-256 fitur internal: `e7678de14cae2ed296d22d2b2644196af551ae12550dab5170413ce000ea3d8a`. Seluruh 15 fitur dibandingkan pada semua URL unik; seluruh 23 atribut halaman dibandingkan dengan record deduplikasi. Cache gzip berhasil dibaca. Tidak ada cache fitur historis untuk perbandingan byte; gzip dapat mengandung timestamp sehingga checksum gzip bukan bukti kesetaraan konten lintas run.

## Error, warning, dan perbedaan

Error cell: 0. Stream notebook tersimpan: []. Kernel launcher memberi warning TCP tanpa enkripsi pada proses lokal; kernel dimatikan setelah eksekusi. Tidak ada URL dataset dikunjungi. Git tetap memberi warning global ignore tidak dapat diakses. Python berubah dari 3.14.4 historis ke 3.13.0; paket audit tercatat sama. Perbedaan metadata environment tidak dipaksa hilang.

## Perlindungan historis

Checksum sebelum/sesudah pada 25 file lama: semua sama. Cakupan termasuk dataset asli, kedua notebook asli, seluruh hasil/ historis, requirements dan dokumentasi audit yang sudah ada. Bukti: historical_integrity_before.json dan historical_integrity_after.json. Tidak ada commit/push/reset atau perubahan source.

## Artefak baru

Daftar file run pada saat laporan disusun:
- `01_Audit_dan_Split.executed.ipynb`
- `01_Audit_dan_Split.ipynb`
- `02_Eksperimen_dan_Evaluasi.ipynb`
- `artifact_checksums.json`
- `comparison.csv`
- `Dataset\PhiUSIIL_Phishing_URL_Dataset.csv`
- `hasil\audit_struktur_mentah.csv`
- `hasil\distribusi_struktur_split.csv`
- `hasil\fitur_internal.csv.gz`
- `hasil\irisan_domain.csv`
- `hasil\manifest_data.json`
- `hasil\ringkasan_split.csv`
- `historical_integrity_after.json`
- `historical_integrity_before.json`
- `independent_overlap.csv`
- `independent_split_summary.csv`
- `missing_values.csv`
- `requirements-lock.txt`
- `run_manifest.json`
- `split_membership.csv.gz`
- `validation_results.json`
- `REPRODUCTION_REPORT.md` (laporan ini).

Output notebook: hasil/manifest_data.json, hasil/audit_struktur_mentah.csv, hasil/ringkasan_split.csv, hasil/irisan_domain.csv, hasil/distribusi_struktur_split.csv dan hasil/fitur_internal.csv.gz. Checksum artefak tercatat di artifact_checksums.json. comparison.csv menyimpan tabel pembandingan terstruktur; validation_results.json menyimpan seluruh pemeriksaan. Orkestrator lokal .venv/stage4_execute.py dan .venv/stage4_validate.py diabaikan Git.

## Kesiapan notebook kedua dan satu pekerjaan berikutnya

Prasyarat data N2 siap jika seluruh validasi PASS: cache, manifest dan fitur baru berada dalam direktori run yang sama, dan interpreter .venv sudah teruji. Belum ada training atau metrik reproduksi baru. Baseline tetap menunggu persetujuan tim. N2 historis cell 6 masih menjalankan pembobotan tambahan dan evaluate pada cell 4 menghitung subgroup; menjalankan seluruh notebook akan melampaui enam eksperimen utama. Jangan menjalankan N2 sebelum cakupan berikutnya disetujui.

Satu pekerjaan berikutnya: review hasil reproduksi bersama tim dan sepakati cakupan eksekusi enam eksperimen utama serta baseline selected features, termasuk perlakuan terhadap alur pembobotan tambahan pada salinan notebook. Selanjutnya baru otorisasi eksekusi eksperimen pada output run terisolasi.

## Catatan penutupan validasi

Status akhir: **PASS**. Checksum seluruh salinan input tetap cocok, source semua cell notebook hasil eksekusi identik dengan source salinan awal, dan pip freeze aktual cocok tepat dengan lockfile run.

Dua error terjadi pada skrip pendamping validasi sebelum laporan final: SyntaxError akibat penyusunan newline string dan KeyError akibat pemisah path Windows pada indeks checksum. Keduanya diperbaiki hanya pada skrip .venv/stage4_validate.py; validasi independen diulang dan lulus. Notebook penelitian dieksekusi satu kali, tidak mengalami error, dan tidak diubah. Masalah skrip pendamping ini bukan perbedaan metodologi atau kegagalan notebook.

Pemeriksaan missing tambahan: pandas default NA pada pembacaan aktual tidak menemukan missing; string kosong Title/TLD juga nol. Audit sebelumnya memakai daftar penanda case-insensitive yang lebih luas. Jumlah token yang cocok daftar itu pada run ini: {"TLD": 19, "Title": 5}. Ini kandidat penanda, bukan missing semantik terkonfirmasi; tidak ada missing input model yang ditemukan.

Status Git akhir: branch develop, commit d80117b tidak berubah; docs/, requirements-lock.txt dan runs/ untracked. Tidak ada diff tracked, commit atau push. Peringatan global ignore tetap ada. Skrip pendamping hanya berada dalam .venv yang diabaikan Git.
