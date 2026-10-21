from database.produk_db import ambil_produk

def format_rupiah(angka):
    return f"Rp{angka:,.0f}".replace(",", ".")

def tambah_ke_keranjang(keranjang, id_produk):
    daftar_produk = ambil_produk()

    item = next(
        (p for p in daftar_produk if p["id"] == id_produk),
        None,
    )

    if item is None:
        return keranjang

    jumlah_sekarang = keranjang.get(id_produk, 0)

    if jumlah_sekarang < item["stok"]:
        keranjang[id_produk] = jumlah_sekarang + 1

    return keranjang


def hitung_total(keranjang):
    daftar_produk = ambil_produk()
    total = 0

    for id_produk, jumlah in keranjang.items():
        item = next(
            (p for p in daftar_produk if p["id"] == id_produk),
            None,
        )

        if item is not None:
            total += item["harga"] * jumlah

    return total
