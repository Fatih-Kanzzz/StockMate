import sqlite3
from database.connection import DB_PATH


def ambil_produk():
    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.row_factory = sqlite3.Row

        hasil = koneksi.execute(
            "SELECT * FROM produk ORDER BY id"
        ).fetchall()

        return [dict(item) for item in hasil]


def tambah_produk(nama, kategori, harga, stok, gambar="📦"):
    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.execute(
            """
            INSERT INTO produk (nama, kategori, harga, stok, gambar)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nama, kategori, harga, stok, gambar)
        )


def perbarui_produk(id_produk, harga, stok):
    with sqlite3.connect(DB_PATH) as koneksi:
        hasil = koneksi.execute(
            """
            UPDATE produk
            SET harga = ?, stok = ?
            WHERE id = ?
            """,
            (harga, stok, id_produk)
        )

        if hasil.rowcount == 0:
            raise ValueError("Produk tidak ditemukan.")
