# Environment Setup TTKI P1

Tanggal: 25 November 2026. Setup dan smoke test saja; tidak ada eksekusi notebook penelitian, ekstraksi dataset penuh, split ulang, atau training.

## Git dan batas perubahan

Branch develop, commit d80117b50f179cfefe91f1c138706264a2934cc7. Origin fetch/push https://github.com/Ardinanta/Phising-URL-Detection.git. Sebelum tahap ini hanya docs/ hasil Tahap 2 yang untracked. Global ignore Git tidak dapat dibaca. Tidak fetch/commit/push/reset. requirements.txt, dataset, notebook, hasil historis dan dokumen Tahap 2 dipertahankan.

## Interpreter yang ditemukan

| Lokasi | Versi/status | Pemakaian |
|---|---|---|
| [LOCAL_INSTALLATION]| 3.10.6; default PATH | Tidak dipakai setup; tidak memiliki file_digest |
| [LOCAL_USER_PATH] | 3.13.0, 64 bit | Interpreter mandiri untuk .venv project |
| [LOCAL_INSTALLATION]| 3.13.2 | Interpreter bundled pgAdmin; tidak dipakai |
| [LOCAL_INSTALLATION]| 3.10.6 | Venv project lain; tidak dipakai |
| WindowsApps/python.exe dan python3.exe | Alias ditemukan Get-Command; bukan versi runtime terverifikasi | Tidak dipakai |

`py -0p` melaporkan No installed Pythons found, meskipun instalasi pengguna 3.13.0 dapat dijalankan langsung. `where.exe python` menunjuk Laragon. Pemeriksaan meliputi PATH, Launcher, lokasi instalasi umum dan pencarian file; bukan jaminan inventaris seluruh disk karena pencarian rekursif luas dihentikan setelah interpreter mandiri sesuai ditemukan. Tidak ada Python global dipasang.

## Virtual environment dan instalasi

.venv tidak ada sebelum tahap ini; dibuat baru memakai Python 3.13.0. pyvenv.cfg menyatakan include-system-site-packages=false. Semua paket dipasang melalui .venv/Scripts/python.exe -m pip; package global tidak diubah. Akses indeks pip awal terhalang sandbox socket WinError 10013; percobaan jaringan dengan izin eskalasi berhasil. Kegagalan awal itu bukan bukti versi paket tidak tersedia.

Versi historis NumPy/pandas/scikit-learn/matplotlib/tldextract diprioritaskan dan berhasil dipasang menggunakan wheel Python 3.13. Dependency lain mengikuti requirements.txt. Perintah instalasi yang berhasil:

```powershell
.\.venv\Scripts\python.exe -m pip install --no-cache-dir --disable-pip-version-check --retries 1 --only-binary=:all: -r requirements.txt numpy==2.5.2 pandas==3.0.5 scikit-learn==1.9.1 matplotlib==3.11.1 tldextract==5.3.1
```

## Versi aktual dan perbandingan historis

| Komponen | Aktual .venv | Manifest historis | Status |
|---|---|---|---|
| Python | 3.13.0 | 3.14.4 | Berbeda; tidak mengklaim environment identik |
| numpy | 2.5.2 | 2.5.2 | Sama |
| pandas | 3.0.5 | 3.0.5 | Sama |
| scikit-learn | 1.9.1 | 1.9.1 | Sama |
| matplotlib | 3.11.1 | 3.11.1 | Sama |
| tldextract | 5.3.1 | 5.3.1 | Sama |
| threadpoolctl | 3.8.0 | Tidak dicatat | Tidak dapat dibandingkan |
| ipykernel | 7.4.0 | Tidak dicatat | Tidak dapat dibandingkan |

OS aktual: `Windows-11-10.0.26200-SP0`; historis: `Windows-11-10.0.26300-SP0`.

CPU aktual: `AMD64 Family 23 Model 160 Stepping 0, AuthenticAMD`; historis: `AMD64 Family 23 Model 96 Stepping 1, AuthenticAMD`.

RAM fisik terdeteksi: 7817785344 byte (7.28 GiB). RAM historis tidak dicatat. CIM OS/CPU awal access denied; platform Python dan psutil berhasil dipakai.

Semua dependency aktual diekspor melalui pip freeze ke [requirements-lock.txt](../../requirements-lock.txt). Lockfile memuat dependency transitif; tidak mengunci Python, OS, CPU, BLAS atau hash wheel. Dependency transitif historis tidak dicatat, sehingga kesetaraan penuh tidak dapat dipastikan.

## Hasil smoke test aktual

| Pemeriksaan | Hasil |
|---|---|
| imports | PASS: seven requested libraries imported |
| file_digest | PASS: synthetic BytesIO digest |
| dataset | PASS: pandas read 5 rows, 56 columns; URL values not printed or visited |
| offline_psl | PASS: built-in snapshot, synthetic example.com only; network disabled for extractor |
| kernel | PASS: real kernel launched; seven libraries imported; sys.executable matches .venv; no notebook/training executed |
| internal_features_static | N1 cell 2/4/6 provides data read, URL extraction, split, cache write; imports available; full generation NOT executed |
| 01_Audit_dan_Split.ipynb | 6 cells, 3 code cells; JSON and AST PASS; no cells executed |
| 02_Eksperimen_dan_Evaluasi.ipynb | 8 cells, 4 code cells; JSON and AST PASS; no cells executed |
| pip check | No broken requirements found. |

Tidak ada URL dataset dicetak atau dikunjungi. PSL diuji hanya memakai hostname sintetis example.com dengan suffix_list_urls=() dan cache_dir=None. Uji file_digest memakai BytesIO sintetis. Pembacaan dataset dibatasi lima baris. AST parsing tidak menjalankan kode notebook.

Kernel nyata diluncurkan, mengimpor tujuh library utama, memeriksa sys.executable dan file_digest, kemudian dimatikan. Kernelspec project berada di `.venv/share/jupyter/kernels/ttki-p1/kernel.json`; argv menunjuk interpreter .venv. Tidak mendaftarkan kernel global/user. Pemilihan kernel pada UI VS Code belum diverifikasi; pilih Select Kernel -> Python Environments -> interpreter .venv/Scripts/python.exe. Untuk Jupyter gunakan executable Jupyter dari .venv atau JUPYTER_PATH yang menunjuk .venv/share/jupyter. Tidak perlu instalasi kernelspec global.

## Kesiapan notebook dan blocker

- N1: prasyarat import, file_digest, parser, pembacaan data dan PSL lulus. N1 cell 2/4/6 secara statis menyediakan pembentukan fitur dan cache; generasi penuh belum dijalankan sehingga keberhasilan seluruh data belum dibuktikan.
- N2: library dan parser lulus, tetapi hasil/fitur_internal.csv.gz belum tersedia. Harus dihasilkan N1 pada direktori output run baru. Jangan memakai manifest historis untuk cache baru tanpa mencatat checksum/provenance run.
- Persetujuan baseline selected features masih menunggu tim; lihat BASELINE_DECISION.md.
- Reproduksi belum aman jika notebook dijalankan langsung dari root: OUT tetap Path("hasil") dan file lama akan ditimpa.
- N2 cell 6 tetap menjalankan subgroup/reweighting selain utama. Setup tidak mengubah atau menonaktifkannya; batas enam eksperimen perlu ditegaskan sebelum eksekusi berikutnya.
- Python 3.13.0 dan perangkat berbeda dari manifest; hasil/timing tidak dijamin identik meskipun lima versi library sama.

## Strategi output baru tanpa menimpa hasil historis

Rekomendasi tahap berikutnya: buat direktori kerja kosong terpisah, misalnya `runs/<tanggal>-<run-id>/`, berisi salinan identik kedua notebook, Dataset/ berisi salinan CSV dengan checksum sama, dan hasil/ kosong. Jalankan kernel .venv dengan working directory direktori run itu, bukan root repositori. Karena SOURCE dan OUT relatif, notebook asli tidak perlu diubah dan kedua notebook run mengakses cache yang sama dalam hasil/ run. Jangan menyalin hasil historis ke hasil/ run. Verifikasi cwd aktual kernel dan ketiadaan nama output sebelum eksekusi; hanya memilih file notebook di subfolder belum cukup menjamin cwd.

Catat run-id, commit, checksum CSV/notebook, lockfile, Python/perangkat, definisi fitur, split membership dan lokasi output. Arsip hasil/ root dibiarkan utuh. Alternatif override OUT membutuhkan alur runner tersendiri karena masing-masing notebook menetapkan ulang OUT; belum dibuat dalam Tahap 3. Strategi terisolasi ini baru rekomendasi, tidak ada direktori run atau dataset duplikat dibuat.

## Satu pekerjaan berikutnya

Konfirmasi usulan baseline selected features bersama tim dan siapkan run N1 terisolasi dengan pemeriksaan cwd/output sebelum eksekusi. Kriteria siap: persetujuan tercatat, hasil historis terlindungi, kernel .venv dipilih, dan output baru mengarah ke hasil/ dalam direktori run. Jangan menjalankan N2 sebelum cache audit baru lolos pemeriksaan dan cakupan tambahan diputuskan.

## Bukti dan artefak

- N1 cell 2 baris sumber 16-17: SOURCE dan OUT; cell 4 baris 35 serta cell 6 baris 36/39/43: penulisan artefak.
- N2 cell 2 baris sumber 19/21: OUT dan cache; cell 6 baris 23/29 dan cell 8 baris 22: penulisan hasil.
- requirements.txt asli baris 1-7; hasil/manifest_data.json baris 53-58; hasil/manifest_eksperimen.json baris 18-27.
- Artefak lokal smoke di .venv/stage3_smoke.py dan .venv/stage3_smoke_result.json, keduanya diabaikan Git bersama venv. Kernelspec juga hanya dalam venv.
- File baru yang dibagikan: BASELINE_DECISION.md, ENVIRONMENT_SETUP.md, requirements-lock.txt. Empat file dokumentasi Tahap 2 tidak diubah.
