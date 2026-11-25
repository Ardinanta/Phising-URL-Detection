# Audit Fitur TTKI P1

Tanggal audit: 25 November 2026. Commit acuan: `d80117b50f179cfefe91f1c138706264a2934cc7`, branch `develop`.

Audit ini hanya menghasilkan dokumentasi. Notebook, dataset, hasil, dependency, dan rancangan penelitian tidak diubah; tidak ada training atau eksekusi notebook. Pemeriksaan CSV dan parsing JSON notebook adalah inspeksi, bukan reproduksi eksperimen.

## Bukti dan batas verifikasi

- N1 = [01_Audit_dan_Split.ipynb](../../../01_Audit_dan_Split.ipynb); N2 = [02_Eksperimen_dan_Evaluasi.ipynb](../../../02_Eksperimen_dan_Evaluasi.ipynb). Nomor cell mulai 1 termasuk Markdown. N1 cell 2: seleksi/deduplikasi/target; cell 4: ekstraksi; cell 6: split. N2 cell 2: manifest/parameter; cell 4: fit/threshold/metrik; cell 6: konfigurasi utama dan pembobotan.
- [README](../../../README.md) baris 19?27 mendefinisikan skenario dan tambahan; baris 39 mengakui provenance Kaggle belum terverifikasi.
- [manifest_data](../../../hasil/manifest_data.json) baris 11?51 memuat daftar fitur; [manifest_eksperimen](../../../hasil/manifest_eksperimen.json) baris 2?27 memuat parameter dan environment tersimpan. Manifest bukan log reproduksi baru.
- [UCI resmi](https://archive.ics.uci.edu/dataset/967/phiusiil+phishing+url+dataset), diakses melalui halaman `/dataset/967/` dan indeks pencarian resmi pada tanggal audit. Metadata mengonfirmasi label asli, peran FILENAME, dan sumber umum URL/halaman. Tabel deskripsi rinci tidak tersedia dalam konten yang dapat dibaca. UCI menyebut beberapa fitur derived, tetapi tidak menjelaskan rumusnya pada halaman tersebut.
- [Paper sumber](https://doi.org/10.1016/j.cose.2023.103545): DOI redirect tidak dapat dibaca, ScienceDirect memberi 403. Cuplikan penerbit mendukung keberadaan mekanisme USI, tidak cukup untuk mengesahkan rumus setiap kolom. Tidak memakai definisi dari repositori pihak ketiga sebagai fakta resmi.

Definisi rinci yang belum didukung sumber ditandai **belum terverifikasi**. Interpretasi berdasarkan nama bukan definisi resmi. Tipe data pada register adalah tipe nilai CSV hasil inspeksi seluruh record, bukan klaim dtype historis pandas atau tipe resmi UCI. Kolom integer dapat mencakup indikator; status biner tidak diasumsikan hanya dari nama.

## Identitas data lokal

CSV memiliki 235,795 baris, 56 kolom, 235,370 URL unik, 425 URL tambahan identik, dan 0 URL konflik label. Label asli: {'1': 134850, '0': 100945}. Missing string kosong: {}. Pemeriksaan ini tidak mendeteksi semua kemungkinan sentinel semantik. Tidak ada field string kosong. Audit sebelumnya dengan penanda missing umum (termasuk NA/null) menandai Title=5 dan TLD=19; penanda tersebut dapat pula berupa teks literal yang sah. UCI menyatakan tidak ada missing. Status semantik penanda tersebut perlu ditelusuri; jangan menganggap semuanya nilai hilang terkonfirmasi.

SHA-256 lokal: `a236549cd369cd80bd478ff8e1779cbf44c58d5c3f79f7a51a1adbed7d06d1c6`; cocok dengan manifest. Kesamaan checksum tidak membuktikan versi Kaggle atau tanggal unduh. UCI menghitung 54 fitur; CSV memiliki 56 kolom karena terdapat FILENAME dan target.

## Matriks seluruh 56 kolom

Matriks lengkap 16 field tersedia di [feature_registry.csv](feature_registry.csv). Tabel di bawah menyajikan seluruh baris beserta keputusan. Tidak ada fitur asli leksikal numerik yang digunakan langsung; penggunaan pengganti dibedakan dari penggunaan kolom asli. URL dan label berperan sebagai input ekstraksi/target, bukan prediktor mentah.

| Kolom | Tipe lokal | Kategori | A langsung | B langsung | C langsung | Keputusan | Alasan |
|---|---|---|---|---|---|---|---|
| FILENAME | text | identifier | tidak | tidak | tidak | exclude | Pengenal tidak menjadi prediktor; sesuai saran UCI. |
| URL | text | URL lexical | tidak | tidak | tidak | replace | URL menjadi input ekstraksi 15 fitur; teks mentah tidak masuk model. |
| URLLength | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal panjang_url; kesetaraan numerik tidak diasumsikan. |
| Domain | text | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| DomainLength | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal panjang_host; kesetaraan numerik tidak diasumsikan. |
| IsDomainIP | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal host_ip; kesetaraan numerik tidak diasumsikan. |
| TLD | text | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| URLSimilarityIndex | real | statistik/derived | tidak | tidak | tidak | exclude | Eksklusi konservatif: rumus atau referensi statistik belum terverifikasi, bukan leakage terbukti. |
| CharContinuationRate | real | statistik/derived | tidak | tidak | tidak | exclude | Eksklusi konservatif: rumus atau referensi statistik belum terverifikasi, bukan leakage terbukti. |
| TLDLegitimateProb | real | statistik/derived | tidak | tidak | tidak | exclude | Eksklusi konservatif: rumus atau referensi statistik belum terverifikasi, bukan leakage terbukti. |
| URLCharProb | real | statistik/derived | tidak | tidak | tidak | exclude | Eksklusi konservatif: rumus atau referensi statistik belum terverifikasi, bukan leakage terbukti. |
| TLDLength | integer | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| NoOfSubDomain | integer | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| HasObfuscation | integer | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| NoOfObfuscatedChar | integer | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| ObfuscationRatio | real | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| NoOfLettersInURL | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal huruf_url; kesetaraan numerik tidak diasumsikan. |
| LetterRatioInURL | real | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| NoOfDegitsInURL | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal angka_url; kesetaraan numerik tidak diasumsikan. |
| DegitRatioInURL | real | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| NoOfEqualsInURL | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal sama_dengan_query; kesetaraan numerik tidak diasumsikan. |
| NoOfQMarkInURL | integer | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| NoOfAmpersandInURL | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal ampersand_query; kesetaraan numerik tidak diasumsikan. |
| NoOfOtherSpecialCharsInURL | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal karakter_lain; kesetaraan numerik tidak diasumsikan. |
| SpacialCharRatioInURL | real | URL lexical | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| IsHTTPS | integer | URL lexical | tidak | tidak | tidak | replace | Diganti fitur lokal https; kesetaraan numerik tidak diasumsikan. |
| LineOfCode | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| LargestLineLength | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasTitle | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| Title | text | webpage | tidak | tidak | tidak | exclude | Tidak tercakup dalam 15 fitur terpilih; alasan eksklusi spesifik tidak didokumentasikan, bukan fitur yang terbukti tidak relevan. |
| DomainTitleMatchScore | real | webpage+URL | tidak | tidak | tidak | exclude | Eksklusi konservatif skor derived; aturan pembentukan belum terverifikasi; tidak membuktikan leakage. |
| URLTitleMatchScore | real | webpage+URL | tidak | tidak | tidak | exclude | Eksklusi konservatif skor derived; aturan pembentukan belum terverifikasi; tidak membuktikan leakage. |
| HasFavicon | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| Robots | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| IsResponsive | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfURLRedirect | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfSelfRedirect | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasDescription | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfPopup | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfiFrame | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasExternalFormSubmit | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasSocialNet | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasSubmitButton | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasHiddenFields | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| HasPasswordField | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| Bank | integer | lainnya: keyword belum terverifikasi | tidak | tidak | tidak | exclude | Eksklusi belum memiliki alasan ilmiah per fitur dalam repositori; sumber pencocokan kata perlu diverifikasi. |
| Pay | integer | lainnya: keyword belum terverifikasi | tidak | tidak | tidak | exclude | Eksklusi belum memiliki alasan ilmiah per fitur dalam repositori; sumber pencocokan kata perlu diverifikasi. |
| Crypto | integer | lainnya: keyword belum terverifikasi | tidak | tidak | tidak | exclude | Eksklusi belum memiliki alasan ilmiah per fitur dalam repositori; sumber pencocokan kata perlu diverifikasi. |
| HasCopyrightInfo | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfImage | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfCSS | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfJS | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfSelfRef | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfEmptyRef | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| NoOfExternalRef | integer | webpage | ya | tidak | tidak | include | Atribut halaman terpilih untuk pembanding informasi non-URL; bukan bukti seluruh fitur halaman sudah tercakup. |
| label | integer | target | tidak | tidak | tidak | transform | Target dipetakan ke phishing=1; tidak pernah menjadi prediktor. |

## Audit 15 fitur ekstraksi mandiri

Seluruh fitur berikut merupakan integer deterministik dari teks URL, digunakan A/B/C. Input adalah URL yang telah dideduplikasi; host diparsing, titik akhirnya dibuang, lalu diubah menjadi IDNA ASCII. Tidak ada statistik lintas baris atau label dalam rumus ini. Implementasi: N1 cell 4 `describe_url`, daftar/order N1 cell 2, pemakaian N2 cell 6. Definisi lokal terbukti dari kode, tetapi ekuivalensi dengan fitur bawaan tidak diasumsikan.

| Fitur dan definisi operasional | Perhitungan | Fitur asli terkait | Masalah metodologis |
|---|---|---|---|
| `panjang_url` | `len(url)` | URLLength | Panjang teks asli; Unicode dihitung sebagai karakter Python, bukan byte. |
| `panjang_host` | `len(host)` | DomainLength | Host tanpa titik akhir, IDNA ASCII; belum tentu domain sumber atau domain terdaftar. |
| `panjang_path` | `len(parsed.path)` | tidak ada | Path belum di-percent-decode. |
| `panjang_query` | `len(parsed.query)` | tidak ada | Query tanpa tanda ?; belum di-decode. |
| `titik_host` | `host.count(".")` | NoOfSubDomain: bukan pengganti setara | Jumlah titik host bukan jumlah subdomain; PSL tidak dipakai menghitung fitur ini. |
| `huruf_url` | `sum(c.isalpha() for c in url)` | NoOfLettersInURL | isalpha mencakup Unicode; aturan sumber belum diketahui. |
| `angka_url` | `sum(c.isdigit() for c in url)` | NoOfDegitsInURL | isdigit mencakup Unicode; bukan hanya ASCII 0-9. |
| `karakter_lain` | `len(url)-huruf_url-angka_url` | NoOfOtherSpecialCharsInURL: kesetaraan belum terbukti | Mencakup seluruh karakter nonhuruf/nondigit, termasuk delimiter. |
| `strip_host` | `host.count("-")` | tidak ada | Hanya host; punycode dapat menambah strip. |
| `segmen_path` | `len([s for s in path.split("/") if s])` | tidak ada | Segmen kosong diabaikan; tidak menormalisasi dot-segments. |
| `persen_url` | `url.count("%")` | NoOfObfuscatedChar/HasObfuscation: bukan pengganti setara | Menghitung %, bukan jumlah karakter obfuscated; escape invalid tetap terhitung. |
| `sama_dengan_query` | `query.count("=")` | NoOfEqualsInURL: cakupan berbeda | Hanya query; bukan seluruh URL. |
| `ampersand_query` | `query.count("&")` | NoOfAmpersandInURL: cakupan berbeda | Hanya query; bukan seluruh URL. |
| `https` | `int(parsed.scheme == "https")` | IsHTTPS | Tidak memeriksa TLS aktual; hanya scheme hasil parser. |
| `host_ip` | `1 jika ip_address(host) berhasil, selain itu 0` | IsDomainIP | Semantik parser IP dan normalisasi host lokal; ekuivalensi sumber belum diuji. |

Tidak ada pengganti eksplisit untuk CharContinuationRate, TLDLength, LetterRatioInURL, DegitRatioInURL, NoOfQMarkInURL, SpacialCharRatioInURL, dan sejumlah fitur lain. Titik host tidak setara dengan NoOfSubDomain; persen URL tidak setara dengan obfuscation; penghitungan query berbeda dari hitungan seluruh URL. Karena itu istilah replace pada register berarti pilihan representasi lokal yang terkait secara konseptual, bukan reproduksi fitur asli.

## Audit seluruh 23 atribut halaman A

Seluruh atribut di bawah dibaca langsung dari CSV oleh N1 cell 2, dipertahankan N1 cell 4, dan hanya masuk A melalui N2 cell 6. Pipeline N2 cell 4 mengimputasi berdasarkan train. Tidak ada ekstraksi HTML ulang atau akses situs. Masing-masing masih memerlukan verifikasi definisi upstream, aturan hitung/boolean, sumber halaman, dan waktu pengambilan.

| Atribut | Interpretasi kerja, bukan definisi resmi | Penilaian |
|---|---|---|
| `LineOfCode` | Jumlah baris kode halaman | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `LargestLineLength` | Panjang baris terbesar pada halaman | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasTitle` | Indikator keberadaan judul | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasFavicon` | Indikator favicon | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `Robots` | Indikator terkait robots; objek/aturan deteksi belum terverifikasi | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `IsResponsive` | Indikator responsivitas halaman | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfURLRedirect` | Jumlah redirect URL | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfSelfRedirect` | Jumlah self-redirect | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasDescription` | Indikator deskripsi halaman | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfPopup` | Jumlah popup | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfiFrame` | Jumlah iframe | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasExternalFormSubmit` | Indikator pengiriman form eksternal | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasSocialNet` | Indikator jejaring sosial | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasSubmitButton` | Indikator tombol submit | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasHiddenFields` | Indikator field tersembunyi | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasPasswordField` | Indikator field password | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `HasCopyrightInfo` | Indikator informasi hak cipta | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfImage` | Jumlah gambar | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfCSS` | Jumlah CSS | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfJS` | Jumlah JavaScript | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfSelfRef` | Jumlah referensi internal/self | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfEmptyRef` | Jumlah referensi kosong | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |
| `NoOfExternalRef` | Jumlah referensi eksternal | Layak bersyarat sebagai informasi non-URL; provenance ekstraksi belum lengkap; bukan leakage terkonfirmasi. |

Redirect adalah perilaku navigasi yang dikelompokkan implementasi sebagai PAGE, bukan selalu properti HTML statis. Robots, self-reference, external-reference, responsive dan external-submit membutuhkan definisi operasional sumber. Kelompok ini tidak boleh diklaim seluruhnya dapat diperoleh dari teks URL.

## Delapan eksklusi yang perlu keputusan eksplisit

| Fitur | Temuan | Rekomendasi audit |
|---|---|---|
| URLSimilarityIndex | Tidak digunakan; referensi pembanding dan pembentukan kolom lokal belum diverifikasi | Eksklusi konservatif dapat dipertahankan untuk baseline terpilih; jangan menyebut leakage terbukti |
| TLDLegitimateProb | Tidak digunakan; populasi pembentuk probabilitas tidak diketahui | Periksa apakah referensi eksternal dibekukan atau melibatkan label evaluasi; risiko bersyarat |
| URLCharProb | Tidak digunakan; estimator dan korpus statistik belum diketahui | Prinsip sama; kemampuan dihitung dari URL baru tidak berarti tidak memerlukan statistik referensi |
| DomainTitleMatchScore | Tidak digunakan; memerlukan URL/domain dan judul secara konseptual | Kandidat informasi halaman; eksklusi belum memiliki alasan lengkap; bukan otomatis leakage |
| URLTitleMatchScore | Tidak digunakan; UCI menyebut derived, rumus belum tersedia | Kandidat informasi halaman; perlu provenance dan alasan keputusan |
| Bank | Tidak digunakan; sumber pencarian kata belum pasti | Verifikasi URL/HTML/judul, aturan pencocokan dan relevansi; tidak cukup alasan nama fitur |
| Pay | Sama | Sama |
| Crypto | Sama | Sama |

Tidak ditemukan kebocoran terkonfirmasi pada input aktual. Label dan pengenal dikeluarkan; fitur statistik di atas juga tidak digunakan. Risiko kontaminasi referensi adalah hipotesis audit, bukan kejadian yang terbukti. Seleksi fitur karena korelasi/skor pada test tidak ditemukan pada kode, tetapi sejarah keputusan manual belum terverifikasi.

## Rekomendasi definisi baseline

Definisi yang dapat dipertanggungjawabkan saat ini: **A-selected = 15 fitur leksikal deterministik hasil ekstraksi lokal ditambah 23 atribut halaman numerik terpilih dari CSV, pada split acak terstratifikasi yang sama dengan B.** Ini nama deskriptif dalam audit, bukan perubahan nama skenario pada kode atau rancangan tim.

A/B mengisolasi penambahan 23 atribut terpilih karena 15 fitur dasar dan penanda split sama. A tidak dapat diklaim baseline seluruh 54 fitur sumber atau seluruh fitur relevan yang lolos audit sebelum alasan eksklusi disepakati. Skor match judul dan keyword dapat relevan untuk A, tetapi tidak boleh ditambahkan otomatis tanpa verifikasi dan keputusan tim. B/C memakai 15 fitur identik; perbandingan mengganti protokol sekaligus sampel test.

Hasil lama tetap disimpan dan boleh dilaporkan sebagai konfigurasi aktual terpilih dengan batasan. Jika tim menerima baseline terpilih secara eksplisit, audit ini sendiri tidak membuktikan kebutuhan training ulang. Jika daftar fitur A diubah, hasil A lama tidak mewakili baseline baru; evaluasi konfigurasi terdampak perlu dijalankan lagi setelah persetujuan. Mengubah definisi B/C, split, deduplikasi atau preprocessing memerlukan evaluasi ulang konfigurasi yang terkena. Jangan memilih definisi berdasarkan test yang sudah terlihat.

## Keterbatasan

Provenance salinan Kaggle, extractor upstream, rumus fitur sumber, dan referensi statistik belum lengkap. Tidak ada pembuktian ulang eksekusi, skor per baris, atau keanggotaan split historis. Cache fitur tidak ada. Seluruh legitimate pada audit tersimpan berada pada kelompok akar (hasil/audit_struktur_mentah.csv baris 2?4); ini batas representasi korpus, bukan bukti otomatis leakage. Satu seed tidak memberi ukuran ketidakpastian. Timing tidak mencakup ekstraksi URL/HTML. Lihat [BASELINE_VALIDATION.md](BASELINE_VALIDATION.md) untuk validasi protokol dan keputusan tim.
