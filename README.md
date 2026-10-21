# StockMate 📚

**StockMate** adalah aplikasi kasir dan manajemen inventaris berbasis Python, Streamlit, dan SQLite untuk toko alat tulis.

> **Status:** Prototype dalam pengembangan. Persetujuan dosen untuk penggunaan sebagai proyek UAS masih menunggu konfirmasi.

## Fitur
- Kasir: katalog, keranjang, total belanja, pembayaran, dan kembalian.
- Dashboard: ringkasan penjualan dan produk dengan stok menipis.
- Inventaris: melihat, menambah, dan memperbarui produk.
- Riwayat transaksi: melihat transaksi dan rincian barang.
- Laporan: ringkasan serta grafik penjualan berdasarkan rentang tanggal.
- SQLite: menyimpan produk, transaksi, dan detail transaksi.

## Struktur folder
```text
StockMate-refactor/
├── views/
│   ├── kasir.py
│   ├── dashboard.py
│   ├── inventaris.py
│   ├── riwayat.py
│   └── laporan.py
├── database/
│   ├── connection.py
│   ├── produk_db.py
│   └── transaksi_db.py
├── data/
│   ├── data_produk.py
│   └── stockmate.db
├── .streamlit/
│   └── config.toml
├── app.py
├── kasir.py
├── style.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Menjalankan aplikasi

1. Pastikan Python sudah terpasang.
2. Buat dan aktifkan virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Instal dependensi:

   ```powershell
   pip install -r requirements.txt
   ```

4. Jalankan aplikasi:

   ```powershell
   streamlit run app.py
   ```

## Pembagian kode
- `app.py`: konfigurasi aplikasi dan navigasi.
- `views/`: antarmuka untuk setiap halaman.
- `database/connection.py`: lokasi database dan inisialisasi tabel.
- `database/produk_db.py`: operasi data produk.
- `database/transaksi_db.py`: transaksi, riwayat, ringkasan dashboard, dan laporan.
- `kasir.py`: logika keranjang dan perhitungan kasir.
- `style.py`: CSS tampilan.
- `data/`: data awal produk dan file database SQLite.

## Catatan
Proyek ini merupakan sarana belajar pemrograman Python, antarmuka aplikasi, dan database. Struktur kode ini adalah hasil refactoring awal dan perlu diuji kembali di lingkungan lokal sebelum digunakan sebagai versi utama.
