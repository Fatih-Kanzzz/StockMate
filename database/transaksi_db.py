import sqlite3
from datetime import datetime
from database.connection import DB_PATH


def simpan_transaksi(keranjang, pembayaran):
    if not keranjang:
        raise ValueError("Keranjang masih kosong.")

    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.execute("PRAGMA foreign_keys = ON")

        daftar_id = list(keranjang.keys())
        total = 0
        rincian = []

        # Periksa produk, jumlah, dan stok terbaru
        for id_produk, jumlah in keranjang.items():
            item = koneksi.execute(
                """
                SELECT id, nama, harga, stok
                FROM produk
                WHERE id = ?
                """,
                (id_produk,),
            ).fetchone()

            if item is None:
                raise ValueError(
                    f"Produk ID {id_produk} tidak ditemukan."
                )

            if jumlah <= 0:
                raise ValueError("Jumlah produk tidak valid.")

            if jumlah > item[3]:
                raise ValueError(
                    f"Stok {item[1]} tidak mencukupi."
                )

            subtotal = item[2] * jumlah
            total += subtotal

            rincian.append(
                (item[0], item[1], jumlah, item[2], subtotal)
            )

        if pembayaran < total:
            raise ValueError("Uang pembayaran tidak mencukupi.")

        kembalian = pembayaran - total

        # Simpan ringkasan transaksi
        kursor = koneksi.execute(
            """
            INSERT INTO transaksi
            (tanggal, total, pembayaran, kembalian)
            VALUES (?, ?, ?, ?)
            """,
            (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total,
                pembayaran,
                kembalian,
            ),
        )

        id_transaksi = kursor.lastrowid

        # Simpan rincian barang dan kurangi stok
        for id_produk, nama, jumlah, harga, subtotal in rincian:
            koneksi.execute(
                """
                INSERT INTO detail_transaksi
                (transaksi_id, produk_id, nama_produk,
                 jumlah, harga_satuan, subtotal)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    id_transaksi,
                    id_produk,
                    nama,
                    jumlah,
                    harga,
                    subtotal,
                ),
            )

            hasil = koneksi.execute(
                """
                UPDATE produk
                SET stok = stok - ?
                WHERE id = ? AND stok >= ?
                """,
                (jumlah, id_produk, jumlah),
            )

            if hasil.rowcount != 1:
                raise ValueError(
                    f"Gagal memperbarui stok {nama}."
                )

        return {
            "id": id_transaksi,
            "total": total,
            "pembayaran": pembayaran,
            "kembalian": kembalian,
        }


def ambil_riwayat_transaksi():
    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.row_factory = sqlite3.Row

        hasil = koneksi.execute("""
            SELECT
                id,
                tanggal,
                total,
                pembayaran,
                kembalian
            FROM transaksi
            ORDER BY id DESC
        """).fetchall()

        return [dict(item) for item in hasil]


def ambil_detail_transaksi(id_transaksi):
    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.row_factory = sqlite3.Row

        hasil = koneksi.execute("""
            SELECT
                nama_produk,
                harga_satuan,
                jumlah,
                subtotal
            FROM detail_transaksi
            WHERE transaksi_id = ?
            ORDER BY id
        """, (id_transaksi,)).fetchall()

        return [dict(item) for item in hasil]


def ambil_ringkasan_dashboard():
    hari_ini = datetime.now().strftime("%Y-%m-%d")

    with sqlite3.connect(DB_PATH) as koneksi:
        # Total penjualan hari ini
        penjualan = koneksi.execute(
            """
            SELECT COALESCE(SUM(total), 0)
            FROM transaksi
            WHERE tanggal LIKE ?
            """,
            (f"{hari_ini}%",)
        ).fetchone()[0]

        # Jumlah transaksi hari ini
        jumlah_transaksi = koneksi.execute(
            """
            SELECT COUNT(*)
            FROM transaksi
            WHERE tanggal LIKE ?
            """,
            (f"{hari_ini}%",)
        ).fetchone()[0]

        # Jumlah seluruh produk
        jumlah_produk = koneksi.execute(
            "SELECT COUNT(*) FROM produk"
        ).fetchone()[0]

        # Produk dengan stok 5 atau kurang
        stok_menipis = koneksi.execute(
            "SELECT COUNT(*) FROM produk WHERE stok <= 5"
        ).fetchone()[0]

        # Daftar produk yang stoknya menipis
        produk_menipis = koneksi.execute(
            """
            SELECT nama, stok
            FROM produk
            WHERE stok <= 5
            ORDER BY stok ASC
            """
        ).fetchall()

    return {
        "penjualan": penjualan,
        "jumlah_transaksi": jumlah_transaksi,
        "jumlah_produk": jumlah_produk,
        "stok_menipis": stok_menipis,
        "produk_menipis": produk_menipis,
    }


def ambil_laporan_penjualan(tanggal_mulai, tanggal_akhir):
    with sqlite3.connect(DB_PATH) as koneksi:
        koneksi.row_factory = sqlite3.Row

        ringkasan = koneksi.execute(
            """
            SELECT
                COALESCE(SUM(total), 0) AS omzet,
                COUNT(*) AS jumlah_transaksi,
                COALESCE(AVG(total), 0) AS rata_rata
            FROM transaksi
            WHERE date(tanggal) BETWEEN ? AND ?
            """,
            (tanggal_mulai, tanggal_akhir)
        ).fetchone()

        penjualan_harian = koneksi.execute(
            """
            SELECT
                date(tanggal) AS tanggal,
                SUM(total) AS omzet
            FROM transaksi
            WHERE date(tanggal) BETWEEN ? AND ?
            GROUP BY date(tanggal)
            ORDER BY date(tanggal)
            """,
            (tanggal_mulai, tanggal_akhir)
        ).fetchall()

    return {
        "omzet": ringkasan["omzet"],
        "jumlah_transaksi": ringkasan["jumlah_transaksi"],
        "rata_rata": ringkasan["rata_rata"],
        "harian": [dict(item) for item in penjualan_harian],
    }
