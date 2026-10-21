import streamlit as st
from datetime import datetime, timedelta
from database.transaksi_db import ambil_laporan_penjualan
from kasir import format_rupiah


def render():
    st.title("📊 Laporan Penjualan")
    st.caption("Ringkasan transaksi berdasarkan periode.")

    kolom_tanggal1, kolom_tanggal2 = st.columns(2)

    with kolom_tanggal1:
        tanggal_mulai = st.date_input(
            "Tanggal mulai",
            value=datetime.now().date().replace(day=1),
            key="laporan_mulai"
        )

    with kolom_tanggal2:
        tanggal_akhir = st.date_input(
            "Tanggal akhir",
            value=datetime.now().date(),
            key="laporan_akhir"
        )

    if tanggal_mulai > tanggal_akhir:
        st.error("Tanggal mulai tidak boleh melewati tanggal akhir.")
        st.stop()

    laporan = ambil_laporan_penjualan(
        tanggal_mulai.isoformat(),
        tanggal_akhir.isoformat()
    )

    st.divider()

    kolom1, kolom2, kolom3 = st.columns(3)

    kolom1.metric(
        "Total Omzet",
        format_rupiah(laporan["omzet"])
    )

    kolom2.metric(
        "Jumlah Transaksi",
        laporan["jumlah_transaksi"]
    )

    kolom3.metric(
        "Rata-rata Transaksi",
        format_rupiah(laporan["rata_rata"])
    )

    st.divider()
    st.subheader("Grafik Penjualan Harian")


    if laporan["harian"]:
        jumlah_hari = (tanggal_akhir - tanggal_mulai).days + 1

        omzet_per_tanggal = {
            item["tanggal"]: item["omzet"]
            for item in laporan["harian"]
        }

        data_grafik = [
            {
                "Tanggal": (
                    tanggal_mulai + timedelta(days=i)
                ).isoformat(),
                "Omzet": omzet_per_tanggal.get(
                    (
                        tanggal_mulai + timedelta(days=i)
                    ).isoformat(),
                    0
                )
            }
            for i in range(jumlah_hari)
        ]


        st.bar_chart(
            data_grafik,
            x="Tanggal",
            y="Omzet"
        )

        st.subheader("Rincian Penjualan")

        st.dataframe(
            [
                {
                    "Tanggal": item["tanggal"],
                    "Omzet": format_rupiah(item["omzet"])
                }
                for item in laporan["harian"]
            ],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("Belum ada transaksi pada periode ini.")
