import streamlit as st
from kasir import format_rupiah
from database.transaksi_db import ambil_riwayat_transaksi, ambil_detail_transaksi


def render():
    st.title("🧾 Riwayat Transaksi")
    st.caption("Daftar transaksi yang tersimpan di StockMate.")

    riwayat = ambil_riwayat_transaksi()

    if not riwayat:
        st.info("Belum ada transaksi yang tersimpan.")
    else:
        pencarian_transaksi = st.text_input(
            "Cari nomor transaksi",
            placeholder="Masukkan ID transaksi...",
        )

        if pencarian_transaksi.strip():
            if pencarian_transaksi.isdigit():
                id_dicari = int(pencarian_transaksi)
                riwayat = [
                    t for t in riwayat
                    if t["id"] == id_dicari
                ]
            else:
                riwayat = []

        if not riwayat:
            st.warning("Transaksi tidak ditemukan.")

        for transaksi in riwayat:
            with st.expander(
                f"Transaksi #{transaksi['id']} | "
                f"{transaksi['tanggal']} | "
                f"{format_rupiah(transaksi['total'])}"
            ):
                st.write(
                    f"**Total:** "
                    f"{format_rupiah(transaksi['total'])}"
                )
                st.write(
                    f"**Pembayaran:** "
                    f"{format_rupiah(transaksi['pembayaran'])}"
                )
                st.write(
                    f"**Kembalian:** "
                    f"{format_rupiah(transaksi['kembalian'])}"
                )

                st.markdown("**Barang yang dibeli**")

                detail = ambil_detail_transaksi(transaksi["id"])

                st.dataframe(
                    [
                        {
                            "Produk": item["nama_produk"],
                            "Harga": format_rupiah(
                                item["harga_satuan"]
                            ),
                            "Jumlah": item["jumlah"],
                            "Subtotal": format_rupiah(
                                item["subtotal"]
                            ),
                        }
                        for item in detail
                    ],
                    use_container_width=True,
                    hide_index=True,
                )
