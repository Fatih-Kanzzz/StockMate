import streamlit as st
from database.produk_db import ambil_produk
from database.transaksi_db import simpan_transaksi
from kasir import format_rupiah, tambah_ke_keranjang, hitung_total


def render():
    produk = ambil_produk()
    # HEADER

    st.markdown(
        '<div class="brand">Checkout Order</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="muted">'
        'Pilih produk dan susun pesanan pelanggan.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")


    # AREA KATALOG + KERANJANG

    katalog, panel_keranjang = st.columns(
        [1.8, 1],
        gap="large",
    )

    with katalog:
        pencarian = st.text_input(
            "🔎 Cari produk",
            placeholder="Cari nama produk...",
            key="pencarian",
        )

        kategori = st.selectbox(
            "Kategori produk",
            [
                "Semua Kategori",
                "Buku",
                "Alat Tulis",
                "Kertas",
                "Elektronik",
            ],
        )

        produk_ditampilkan = []

        for item in produk:
            cocok_nama = pencarian.lower() in item["nama"].lower()
            cocok_kategori = (
                kategori == "Semua Kategori"
                or item["kategori"] == kategori
            )

            if cocok_nama and cocok_kategori:
                produk_ditampilkan.append(item)

        st.caption(f"{len(produk_ditampilkan)} produk ditemukan")

        for awal in range(0, len(produk_ditampilkan), 2):
            kolom_produk = st.columns(2)

            for posisi, kolom in enumerate(kolom_produk):
                indeks = awal + posisi

                if indeks >= len(produk_ditampilkan):
                    break

                item = produk_ditampilkan[indeks]

                with kolom:
                    status_stok = (
                        "Habis" if item["stok"] == 0
                        else "Stok menipis" if item["stok"] <= 5
                        else f"Stok: {item['stok']}"
                    )

                    kelas_stok = (
                        "stock low-stock"
                        if item["stok"] <= 5
                        else "stock"
                    )

                    st.markdown(
                        f"""
                        <div class="product-card">
                            <div class="product-image">
                                {item['gambar']}
                            </div>
                            <div class="product-name">
                                {item['nama']}
                            </div>
                            <p class="muted">{item['kategori']}</p>
                            <div class="product-price">
                                {format_rupiah(item['harga'])}
                            </div>
                            <br>
                            <span class="{kelas_stok}">
                                {status_stok}
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.button(
                        "＋ Tambah ke Keranjang",
                        key=f"tambah_{item['id']}",
                        use_container_width=True,
                        type="primary",
                        disabled=item["stok"] == 0,
                        on_click=tambah_ke_keranjang,
                        args=(st.session_state.keranjang, item["id"]),
                    )

    with panel_keranjang:
        st.markdown("### 🛒 Order Details")
        st.caption("Daftar belanja pelanggan")
        st.divider()

        if not st.session_state.keranjang:
            st.info("Keranjang masih kosong. Tambahkan produk.")
        else:
            for id_produk in list(st.session_state.keranjang.keys()):
                item = next(
                    (p for p in produk if p["id"] == id_produk),
                    None,
                )

                if item is None:
                    continue

                jumlah = st.session_state.keranjang[id_produk]

                with st.container(border=True):
                    st.markdown(f"**{item['gambar']} {item['nama']}**")
                    st.caption(format_rupiah(item["harga"]) + " / unit")

                    kolom_kurang, kolom_jumlah, kolom_tambah, kolom_hapus = (
                        st.columns([1, 1, 1, 1])
                    )

                    with kolom_kurang:
                        if st.button(
                            "−",
                            key=f"kurang_{id_produk}",
                            use_container_width=True,
                        ):
                            if jumlah <= 1:
                                del st.session_state.keranjang[id_produk]
                            else:
                                st.session_state.keranjang[id_produk] -= 1
                            st.rerun()

                    with kolom_jumlah:
                        st.write(f"**{jumlah}**")

                    with kolom_tambah:
                        if st.button(
                            "+",
                            key=f"lebih_{id_produk}",
                            use_container_width=True,
                            disabled=jumlah >= item["stok"],
                        ):
                            st.session_state.keranjang[id_produk] += 1
                            st.rerun()

                    with kolom_hapus:
                        if st.button(
                            "✕",
                            key=f"hapus_{id_produk}",
                            use_container_width=True,
                        ):
                            del st.session_state.keranjang[id_produk]
                            st.rerun()

                    st.markdown(
                        f"Subtotal: **{format_rupiah(item['harga'] * jumlah)}**"
                    )

        st.divider()

        total = hitung_total(st.session_state.keranjang)
        st.markdown("##### Ringkasan Pembayaran")
        st.markdown(f"Subtotal: {format_rupiah(total)}")
        st.markdown(f"**Total: {format_rupiah(total)}**")

        pembayaran = st.number_input(
            "Uang pembayaran (Rp)",
            min_value=0,
            step=5000,
            value=0,
        )

        kembalian = pembayaran - total

        if pembayaran > 0:
            if kembalian >= 0:
                st.success(f"Kembalian: {format_rupiah(kembalian)}")
            else:
                st.warning(
                    f"Uang kurang: {format_rupiah(abs(kembalian))}"
                )

    
        if st.button(
            "✓ Proses Transaksi",
            type="primary",
            use_container_width=True,
            disabled=total == 0 or pembayaran < total,
        ):
            try:
                hasil = simpan_transaksi(
                    st.session_state.keranjang,
                    int(pembayaran),
                )

                st.session_state.keranjang = {}
                st.session_state.transaksi_siap = hasil

                st.success(
                    f"Transaksi #{hasil['id']} berhasil disimpan!"
                )
                st.info(
                    f"Total: {format_rupiah(hasil['total'])} | "
                    f"Kembalian: {format_rupiah(hasil['kembalian'])}"
                )

                st.rerun()

            except Exception as e:
                st.error(f"Transaksi gagal: {e}")
