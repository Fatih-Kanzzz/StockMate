import streamlit as st
from kasir import format_rupiah
from database.transaksi_db import ambil_ringkasan_dashboard


def render():
    st.title("🏠 Dashboard")
    st.caption("Ringkasan aktivitas toko Stationery StockMate.")

    ringkasan = ambil_ringkasan_dashboard()

    kolom1, kolom2, kolom3, kolom4 = st.columns(4)

    kolom1.metric(
        "Penjualan Hari Ini",
        format_rupiah(ringkasan["penjualan"])
    )

    kolom2.metric(
        "Transaksi Hari Ini",
        ringkasan["jumlah_transaksi"]
    )

    kolom3.metric(
        "Jenis Produk",
        ringkasan["jumlah_produk"]
    )

    kolom4.metric(
        "Stok Menipis",
        ringkasan["stok_menipis"]
    )

    st.divider()

    st.subheader("📦 Perlu Restok")

    if not ringkasan["produk_menipis"]:
        st.success("Semua produk memiliki stok di atas batas minimum.")
    else:
        data_stok = [
            {"Nama Produk": nama, "Sisa Stok": stok}
            for nama, stok in ringkasan["produk_menipis"]
        ]

        st.dataframe(
            data_stok,
            hide_index=True,
            use_container_width=True
        )
