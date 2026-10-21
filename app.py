import streamlit as st

from style import style
from database.connection import init_db
from views import kasir as halaman_kasir
from views import dashboard as halaman_dashboard
from views import inventaris as halaman_inventaris
from views import riwayat as halaman_riwayat
from views import laporan as halaman_laporan


st.set_page_config(
    page_title="StockMate | Kasir",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

style()
init_db()

# Data yang perlu bertahan selama pengguna berpindah menu disimpan di session_state.
if "keranjang" not in st.session_state:
    st.session_state.keranjang = {}

if "pencarian" not in st.session_state:
    st.session_state.pencarian = ""

with st.sidebar:
    st.markdown(
        '<div class="brand">🛍️ StockMate</div>',
        unsafe_allow_html=True,
    )
    st.caption("Smart Store Management")
    st.divider()

    menu = st.radio(
        "NAVIGASI",
        [
            "🛒 Kasir",
            "🏠 Dashboard",
            "📦 Inventaris",
            "🧾 Riwayat Transaksi",
            "📊 Laporan",
        ],
        index=0,
    )

    st.divider()
    st.caption("Versi 1.0 · Prototype")

# app.py hanya memilih halaman. Isi setiap halaman berada di folder views/.
if menu == "🛒 Kasir":
    halaman_kasir.render()
elif menu == "🏠 Dashboard":
    halaman_dashboard.render()
elif menu == "📦 Inventaris":
    halaman_inventaris.render()
elif menu == "🧾 Riwayat Transaksi":
    halaman_riwayat.render()
elif menu == "📊 Laporan":
    halaman_laporan.render()
