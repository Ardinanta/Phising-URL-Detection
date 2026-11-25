# Usulan Keputusan Baseline TTKI P1

Tanggal: 25 November 2026. Status: **MENUNGGU PERSETUJUAN TIM**. Instruksi Tahap 3 mengizinkan mendokumentasikan usulan; tidak menjadi bukti persetujuan seluruh tim. Judul, research question, LR/RF, dan rancangan A/B/C tetap.

## Konfigurasi yang diusulkan

| Skenario | Selected features | Split |
|---|---|---|
| A | 15 fitur leksikal deterministik + 23 atribut halaman terpilih (38 prediktor) | Random stratified, target 70/15/15, seed 42 |
| B | 15 fitur leksikal yang sama dengan bagian leksikal A | Keanggotaan train/validation/test identik dengan A |
| C | 15 fitur leksikal identik dengan B | Domain-grouped, domain terdaftar tanpa irisan antarsplit |

Gunakan istilah **selected features**, bukan **all features**. A/B mengukur kontribusi 23 atribut halaman terpilih dengan representasi leksikal dan keanggotaan split yang sama. B/C membandingkan protokol split dengan fitur identik; sampel test dan komposisinya dapat berbeda. Phishing adalah kelas positif 1 dari label asli 0; F1 phishing adalah metrik utama.

## Daftar fitur tetap

Daftar lengkap dan urutannya mengikuti [experiment_feature_sets.csv](experiment_feature_sets.csv), [feature_registry.csv](feature_registry.csv), N1 cell 2 dan 4, serta hasil/manifest_data.json baris 11-51. N1 = 01_Audit_dan_Split.ipynb; N2 = 02_Eksperimen_dan_Evaluasi.ipynb. Nomor cell mulai 1 termasuk Markdown. Tidak ada fitur ditambah/dihapus melalui keputusan ini.

15 fitur leksikal: panjang_url, panjang_host, panjang_path, panjang_query, titik_host, huruf_url, angka_url, karakter_lain, strip_host, segmen_path, persen_url, sama_dengan_query, ampersand_query, https, host_ip.

23 atribut halaman: LineOfCode, LargestLineLength, HasTitle, HasFavicon, Robots, IsResponsive, NoOfURLRedirect, NoOfSelfRedirect, HasDescription, NoOfPopup, NoOfiFrame, HasExternalFormSubmit, HasSocialNet, HasSubmitButton, HasHiddenFields, HasPasswordField, HasCopyrightInfo, NoOfImage, NoOfCSS, NoOfJS, NoOfSelfRef, NoOfEmptyRef, NoOfExternalRef.

## Dasar dan batas eksklusi

Keputusan include/exclude/replace/transform pada register dipertahankan. Pengenal tidak menjadi prediktor; label hanya target; fitur leksikal bawaan terkait diganti representasi lokal tanpa mengklaim kesetaraan rumus. Fitur yang tidak tercakup merupakan pembatasan eksperimen, bukan pernyataan bahwa fitur itu tidak relevan.

URLSimilarityIndex, TLDLegitimateProb, URLCharProb dan CharContinuationRate dikeluarkan secara konservatif karena rumus/referensi upstream belum lengkap. DomainTitleMatchScore dan URLTitleMatchScore juga tidak digunakan; eksklusi skor judul perlu diterima sebagai batas cakupan, bukan klaim leakage. Bank, Pay dan Crypto tetap dikeluarkan; lokasi pencocokan kata serta alasan spesifik upstream belum terverifikasi. **Tidak ada leakage terkonfirmasi hanya dari nama fitur atau eksklusi tersebut.** Potensi kontaminasi statistik bersyarat pada bagaimana referensi dibentuk; bukti itu belum tersedia.

Definisi rinci sumber, provenance Kaggle, interpretasi penanda missing dan keterbatasan struktur legitimate tetap seperti [FEATURE_AUDIT.md](FEATURE_AUDIT.md). Tim perlu menerima batasan tersebut sebelum finalisasi klaim baseline.

## Protokol dan lingkup utama

N2 cell 4 mem-fit imputasi dan standardisasi hanya train, memilih threshold F1 pada validation, lalu memakai threshold tersebut pada test. Parameter tetap; tidak ditemukan tuning test pada kode. Riwayat keputusan manual belum terverifikasi. Konfigurasi N2 cell 6 memberi A/B penanda split acak sama dan B/C daftar LEXICAL sama. Keanggotaan run historis belum diverifikasi ulang.

Subgroup analysis dan subgroup reweighting **tidak termasuk enam eksperimen utama LR/RF x A/B/C**. Artefak tambahan lama tetap dipertahankan sebagai sejarah. Kode tambahan masih satu alur notebook; menjalankan seluruh N2 akan turut menjalankannya. Tahap ini tidak mengubah notebook atau menjalankannya.

## Dampak terhadap hasil historis

Pertahankan hasil historis sebagai hasil konfigurasi aktual terpilih; jangan menamainya hasil reproduksi baru. Penerimaan definisi yang sama tidak otomatis mewajibkan training ulang. Perubahan daftar fitur/split/preprocessing di tahap selanjutnya memerlukan evaluasi ulang konfigurasi terdampak dan dokumentasi revisi setelah test lama telah terlihat.

## Persetujuan yang belum tersedia

- Tim menerima A sebagai selected features 15+23 beserta batas eksklusi dan provenance.
- Tim menerima definisi fitur lokal dan domain dengan private suffix sebagaimana implementasi.
- Tim menerima pemisahan analisis tambahan dari jawaban utama P1.

Belum ada nama pemberi persetujuan atau tanggal persetujuan tim. Jangan menafsirkan dokumen ini sebagai persetujuan final. Sumber: FEATURE_AUDIT.md; BASELINE_VALIDATION.md; dua register CSV; README baris 19-27; N1 cell 2/4/6; N2 cell 4/6; kedua manifest hasil.
