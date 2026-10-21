import streamlit as st
from database.produk_db import ambil_produk, tambah_produk, perbarui_produk
from kasir import format_rupiah


def render():
    st.title("📦 Inventaris Produk")
    st.caption("Kelola produk, harga, dan persediaan toko.")

    produk = ambil_produk()

    kolom1, kolom2, kolom3 = st.columns(3)

    kolom1.metric("Total Produk", len(produk))
    kolom2.metric(
        "Total Stok",
        sum(item["stok"] for item in produk)
    )
    kolom3.metric(
        "Stok Menipis",
        sum(1 for item in produk if item["stok"] <= 5)
    )

    st.divider()

    pencarian_inventaris = st.text_input(
        "🔎 Cari produk inventaris",
        placeholder="Masukkan nama produk..."
    )

    produk_difilter = [
        item for item in produk
        if pencarian_inventaris.lower() in item["nama"].lower()
    ]

    st.subheader("Daftar Produk")

    data_tabel = [
        {
            "ID": item["id"],
            "Nama Produk": item["nama"],
            "Kategori": item["kategori"],
            "Harga": format_rupiah(item["harga"]),
            "Stok": item["stok"],
            "Status": (
                "Habis" if item["stok"] == 0
                else "Menipis" if item["stok"] <= 5
                else "Tersedia"
            ),
        }
        for item in produk_difilter
    ]

    st.dataframe(
        data_tabel,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    st.subheader("➕ Tambah Produk")

    with st.form("form_tambah_produk"):
        nama_baru = st.text_input("Nama produk")
        kategori_baru = st.selectbox(
            "Kategori",
            ["Buku", "Alat Tulis", "Kertas", "Elektronik", "Lainnya"]
        )
        harga_baru = st.number_input(
            "Harga (Rp)",
            min_value=1,
            step=500
        )
        stok_baru = st.number_input(
            "Stok awal",
            min_value=0,
            step=1
        )

        tambah_dikirim = st.form_submit_button(
            "Simpan Produk",
            use_container_width=True
        )

        if tambah_dikirim:
            if not nama_baru.strip():
                st.error("Nama produk tidak boleh kosong.")
            else:
                try:
                    tambah_produk(
                        nama_baru.strip(),
                        kategori_baru,
                        int(harga_baru),
                        int(stok_baru)
                    )
                    st.success("Produk berhasil ditambahkan!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menambahkan produk: {e}")

    st.divider()

    st.subheader("✏️ Perbarui Harga dan Stok")

    if produk:
        pilihan_produk = st.selectbox(
            "Pilih produk",
            produk,
            format_func=lambda item: (
                f"{item['nama']} (Stok: {item['stok']})"
            ),
            key="pilihan_produk_inventaris"
        )

        with st.form("form_perbarui_produk"):
            harga_update = st.number_input(
                "Harga baru (Rp)",
                min_value=1,
                value=int(pilihan_produk["harga"]),
                step=500
            )
            stok_update = st.number_input(
                "Stok baru",
                min_value=0,
                value=int(pilihan_produk["stok"]),
                step=1
            )

            perbarui_dikirim = st.form_submit_button(
                "Simpan Perubahan",
                use_container_width=True
            )

            if perbarui_dikirim:
                try:
                    perbarui_produk(
                        pilihan_produk["id"],
                        int(harga_update),
                        int(stok_update)
                    )
                    st.success("Data produk berhasil diperbarui!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal memperbarui produk: {e}")
