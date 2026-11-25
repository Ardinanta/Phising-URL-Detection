# Validasi Baseline TTKI P1

Tanggal: 25 November 2026. Acuan commit `d80117b50f179cfefe91f1c138706264a2934cc7`, branch `develop`. Dokumentasi saja; tidak ada training ulang atau perubahan source/dataset/hasil. Istilah N1/N2 dan penomoran cell dijelaskan di [FEATURE_AUDIT.md](FEATURE_AUDIT.md).

## Kondisi Git sebelum penulisan

Branch aktif develop; working tree tidak menunjukkan perubahan pada `git status --short`. Remote origin fetch/push: https://github.com/Ardinanta/Phising-URL-Detection.git. Commit terbaru d80117b, feat: add phising detection. Git memberi peringatan akses global ignore [LOCAL_USER_PATH] Tidak dilakukan fetch, perubahan branch, commit, atau push; keadaan remote terkini belum diverifikasi.

## Kesimpulan

Baseline A layak **bersyarat sebagai 38 fitur terpilih**, belum tervalidasi sebagai seluruh fitur relevan yang lolos audit. B/C memakai 15 fitur lokal yang sama. Seluruh 56 kolom telah didaftarkan; kelengkapan register bukan berarti definisi resmi semua fitur sudah diverifikasi. Teks lengkap paper tidak dapat dibaca dan metadata UCI tidak memuat rumus rinci. Keputusan fitur pada register mendeskripsikan implementasi, bukan persetujuan ilmiah baru atas semua eksklusi.

## Validasi protokol berdasarkan kode

| Ketentuan | Bukti | Penilaian dan batas verifikasi |
|---|---|---|
| A/B keanggotaan train/validation/test identik | N2 cell 6 config A/B sama-sama acak; N2 cell 4 memakai data[split] | Sesuai pada kode; cache fitur tidak tersedia sehingga keanggotaan run historis belum diperiksa ulang |
| B/C daftar fitur identik | N2 cell 6 sama-sama LEXICAL dari manifest | Sesuai; register aktual 15 fitur masing-masing |
| A = 15+23 | N1 cell 2; manifest_data.json baris 11?51; N2 cell 6 | Sesuai konfigurasi tersimpan, cakupan relevansi belum lengkap |
| Preprocessing fit train saja | N2 cell 4 make_pipeline lalu model.fit(train[columns], train[phishing]) | Sesuai; imputasi median semua model, StandardScaler hanya LR |
| Ambang dipilih validation | N2 cell 4 evaluate -> choose_threshold(val_y,val_scores,...) | Sesuai; hasil utama memaksimalkan F1; tie FPR rendah lalu threshold tinggi |
| Test tidak untuk tuning | N2 cell 4; N2 cell 2 PARAMS tetap | Tidak ditemukan tuning test pada kode. Test dipakai timing dan evaluasi; sejarah pemilihan manual parameter/fitur belum terverifikasi |
| Phishing positif | N1 cell 2 label==0 menjadi 1; N2 cell 4 labels=[0,1], predict_proba[:,1] | Konsisten pada kode; tidak ada assertion classes_ eksplisit |
| Split domain terdaftar | N1 cell 4 top_domain_under_public_suffix, private suffix aktif; cell 6 GroupShuffleSplit | Sesuai kode; IP/suffix tak dikenal fallback host; nol irisan didukung CSV, belum direproduksi |
| Deduplikasi sebelum split | N1 cell 2 drop_duplicates(URL), cell 6 split | Sesuai; memilih record pertama, dampak perbedaan halaman URL duplikat belum ditelusuri |
| Pembobotan dipisahkan dari enam utama | N2 cell 6 main_rows/weighted_rows dan file output berbeda | Terpisah logis dan file, tetapi satu loop/cell eksekusi serta helper evaluate masih memproduksi subgroup untuk utama; bukan pemisahan eksekusi penuh |

## Temuan kritis

1. A/B mengukur pengaruh 23 atribut halaman terpilih; belum membuktikan perbandingan seluruh fitur relevan melawan lexical-only. DomainTitleMatchScore, URLTitleMatchScore, Bank, Pay dan Crypto dikeluarkan tanpa alasan rinci per fitur dalam kode/README.
2. URLSimilarityIndex, TLDLegitimateProb, URLCharProb tidak digunakan. Risiko statistik referensi bersifat potensial; tidak ada bukti kontaminasi atau leakage terkonfirmasi. CharContinuationRate juga derived dan dikeluarkan, tetapi rumus belum terverifikasi.
3. Fitur pengganti tidak otomatis ekuivalen. panjang_host bukan domain terdaftar; titik_host bukan NoOfSubDomain; sama_dengan_query/ampersand_query hanya query; persen_url bukan detektor obfuscation sumber.
4. Seluruh legitimate mentah berada pada struktur akar (hasil/audit_struktur_mentah.csv baris 2?4). FPR rendah terbatas pada bentuk legitimate yang tersedia, termasuk pada split C.
5. Pembobotan dan subgroup sudah ada, tetapi di luar enam eksperimen P1 yang diminta. File terpisah tidak membuatnya bagian sah rancangan utama. Tidak ada analisis baru yang ditambahkan melalui audit ini.
6. Manifest hasil dan output notebook adalah bukti tersimpan, bukan reproduksi sekarang. Cache hasil/fitur_internal.csv.gz tidak tersedia; tidak ada model/prediksi/keanggotaan split tersimpan untuk penelusuran mandiri. N2 membaca checksum manifest tanpa memvalidasi cache langsung.
7. Requirements memakai rentang versi. Audit sebelumnya menemukan interpreter terminal Python 3.10.6, sedangkan N1 memakai hashlib.file_digest dan README baris 7 mensyaratkan >=3.11. Kondisi itu dicatat sebagai temuan audit sebelumnya, bukan pengujian environment ulang tahap ini.

## Kelayakan hasil lama dan kebutuhan evaluasi ulang

Enam baris hasil utama berada di hasil/metrik_utama.csv baris 2?7, dengan log N2 cell 6 dan tabel cell 8. Pertahankan semuanya sebagai hasil historis konfigurasi yang tercatat. Jangan menganggapnya hasil baru atau hasil baseline yang daftar fiturnya kelak berubah.

| Keputusan tim | Konsekuensi |
|---|---|
| Menerima 15+23 sebagai baseline fitur terpilih dan menjelaskan keterbatasannya | Tidak ada alasan dari audit fitur ini saja untuk wajib menjalankan ulang enam model; verifikasi reproducibility masih diperlukan sebelum finalisasi |
| Mengubah daftar fitur A | Evaluasi ulang LR/A dan RF/A diperlukan; B/C hanya dapat dipertahankan jika input, split dan protokolnya tetap serta dapat ditelusuri |
| Mengubah fitur leksikal B/C (yang juga menjadi bagian A) | Evaluasi ulang konfigurasi terdampak, berpotensi seluruh enam |
| Mengubah deduplikasi, split, label, threshold rule atau preprocessing | Evaluasi ulang seluruh konfigurasi yang terkena; hasil lama tetap arsip |
| Mempertahankan pembobotan tambahan | Butuh keputusan cakupan terpisah; tidak dicampur ke jawaban utama P1; audit ini tidak merekomendasikan perluasan metode |

Tidak ditemukan bukti yang memaksa pembatalan semua hasil lama. Sebaliknya belum cukup bukti untuk menyebutnya hasil final yang independen terverifikasi. Test telah terlihat; perubahan metodologi berikutnya harus dijelaskan secara transparan sebagai revisi setelah hasil tersedia, bukan dipresentasikan sebagai keputusan sebelum eksperimen.

## Keputusan yang membutuhkan kesepakatan tim

- Apakah istilah baseline berarti 38 fitur terpilih atau seluruh fitur relevan yang lolos audit? Jika terpilih, tuliskan alasan setiap eksklusi dan sesuaikan klaim; belum mengubah dokumen tim maupun kode.
- Apakah skor judul dan Bank/Pay/Crypto relevan bagi A setelah definisi upstream diverifikasi?
- Apakah definisi 15 fitur lokal dan private suffix diterima sebagai definisi operasional penelitian?
- Tegaskan bahwa subgroup/reweighting di luar enam hasil utama. Tidak ada penghapusan artefak yang diperlukan pada tahap audit.
- Lengkapi versi/tanggal unduh/lisensi salinan Kaggle dan sumber extractor jika tersedia dari anggota tim.

## Satu pekerjaan berikutnya

Review dan bekukan register fitur bersama tim, terutama lima fitur judul/keyword dan tiga fitur statistik yang diminta. Prasyarat: bukti definisi/rule sumber bila tersedia serta klarifikasi acuan proposal lokal yang disebut N2 cell 1 tetapi tidak ada pada repositori. Kriteria selesai: keputusan tertulis setiap fitur, definisi A/B/C disepakati, cakupan tambahan dipisahkan, dan daftar konfigurasi yang perlu evaluasi ulang ditetapkan tanpa memakai skor test sebagai dasar seleksi. Jangan training sebelum keputusan tersebut.

## Artefak dan sumber

- [Register 56 kolom](feature_registry.csv): satu record per kolom asli, termasuk tipe lokal, definisi/status, sumber input, URL-only, penggunaan A/B/C, keputusan, alasan, leakage, provenance dan lokasi bukti.
- [Fitur model aktual](experiment_feature_sets.csv): 38 record unik; A=38, B=15, C=15. URL, label, struktur, penanda split dan domain terdaftar tidak dihitung sebagai prediktor.
- [Audit lengkap](FEATURE_AUDIT.md): matriks seluruh kolom, 15 rumus lokal, 23 atribut halaman, sumber dan keterbatasan.
- Sumber resmi: https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset dan https://doi.org/10.1016/j.cose.2023.103545 . Definisi rinci yang tidak dapat dibaca tetap belum terverifikasi.
