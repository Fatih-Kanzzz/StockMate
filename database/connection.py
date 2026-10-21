import sqlite3
from pathlib import Path
from data.data_produk import produk

# Database disimpan di folder data/ agar terpisah dari kode program.
DB_PATH = Path(__file__).resolve().parent.parent / "data" / "stockmate.db"


def init_db():
    # Membuka database atau membuatnya jika belum ada
    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.execute("""
            CREATE TABLE IF NOT EXISTS produk (
                id INTEGER PRIMARY KEY,
                nama TEXT NOT NULL,
                kategori TEXT NOT NULL,
                harga INTEGER NOT NULL,
                stok INTEGER NOT NULL,
                gambar TEXT
            )
        """)

        koneksi.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                total INTEGER NOT NULL,
                pembayaran INTEGER NOT NULL,
                kembalian INTEGER NOT NULL
            )
        """)

        koneksi.execute("""
            CREATE TABLE IF NOT EXISTS detail_transaksi (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaksi_id INTEGER NOT NULL,
                produk_id INTEGER NOT NULL,
                nama_produk TEXT NOT NULL,
                jumlah INTEGER NOT NULL,
                harga_satuan INTEGER NOT NULL,
                subtotal INTEGER NOT NULL,
                FOREIGN KEY (transaksi_id) REFERENCES transaksi(id),
                FOREIGN KEY (produk_id) REFERENCES produk(id)
            )
        """)

        # Periksa apakah tabel produk masih kosong
        jumlah_produk = koneksi.execute(
            "SELECT COUNT(*) FROM produk"
        ).fetchone()[0]

        if jumlah_produk == 0:
            koneksi.executemany("""
                INSERT INTO produk
                (id, nama, kategori, harga, stok, gambar)
                VALUES (?, ?, ?, ?, ?, ?)
            """, [
                (
                    item["id"],
                    item["nama"],
                    item["kategori"],
                    item["harga"],
                    item["stok"],
                    item["gambar"],
                )
                for item in produk
            ])

    print("Database StockMate berhasil disiapkan!")
