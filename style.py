import streamlit as st

def style():
    st.markdown("""
    <style>
        .stApp {
            background: #F7F9FC;
            color: #202938;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] .brand {
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] {
            background: #145A42;
            border-right: 1px solid #104B37;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: #145A42;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown {
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] hr {
            border-color: #39765F;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .brand {
            font-size: 27px;
            font-weight: 800;
            color: #087F5B;
        }

        .muted {
            color: #8490A0;
            font-size: 13px;
        }

        .product-card {
            background: white;
            border: 1px solid #E8EDF3;
            border-radius: 16px;
            padding: 14px;
            margin-bottom: 8px;
        }

        .product-image {
            background: #F0F3F7;
            border-radius: 12px;
            height: 115px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 58px;
            margin-bottom: 12px;
        }

        .product-name {
            font-size: 15px;
            font-weight: 700;
            color: #243247;
            min-height: 40px;
        }

        .product-price {
            font-size: 17px;
            font-weight: 800;
            color: #087F5B;
        }

        .stock {
            display: inline-block;
            padding: 5px 9px;
            border-radius: 20px;
            background: #E8FAF0;
            color: #16804A;
            font-size: 11px;
        }

        .low-stock {
            background: #FFF4D8;
            color: #A66A00;
        }
        .cart-box {
            background: white;
            border: 1px solid #E8EDF3;
            border-radius: 16px;
            padding: 16px;
        }

        div.stButton > button {
            border-radius: 10px;
            font-weight: 600;
        }

        div.stButton > button[kind="primary"] {
            background: #087F5B;
            border-color: #087F5B;
        }

        hr {
            border-color: #E8EDF3;
        }
    </style>
    """, unsafe_allow_html=True)