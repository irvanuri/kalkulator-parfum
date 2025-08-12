import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# === Background dan overlay test dengan Unsplash ===
IMAGE_URL = "https://images.unsplash.com/photo-1615634260167-c8cdede054de?fm=jpg&ixid=M3wxMjA3fDB8MHxwaG90by1yZWxhdGVkfDM4fHx8ZW58MHx8fHx8&ixlib=rb-4.0.3&q=60&w=3000"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), 
                    url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        color: white;
    }}

    /* Semua heading & teks punya shadow biar jelas */
    h1, h2, h3, p, span {{
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }}

    /* Khusus h1 jadi hitam */
    h1 {{
        color: black !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# === DATA RASIO ===
RASIO_OPTIONS = {
    "1:1": (1, 1),
    "2:1": (2, 1),
    "3:1": (3, 1),
    "4:1": (4, 1),
}

# === ML SEDERHANA UNTUK PREDIKSI ===
def train_ml():
    X = np.arange(10, 101).reshape(-1, 1)  # volume 10-100 ml
    y = X  # identitas (output = input)
    model = LinearRegression()
    model.fit(X, y)
    return model

model_ml = train_ml()

# === HITUNG KOMPOSISI ===
def hitung_komposisi(volume, rasio_bibit, rasio_alkohol, persen_fixative):
    total_parts = rasio_bibit + rasio_alkohol
    bibit = round((rasio_bibit / total_parts) * volume, 1)
    alkohol = round((rasio_alkohol / total_parts) * volume, 1)
    fixative = round((persen_fixative / 100) * volume, 1) if persen_fixative > 0 else 0
    return bibit, alkohol, fixative

# === UI STREAMLIT ===
st.title("💐 Kalkulator Komposisi Parfum")

kategori = st.selectbox("Pilih kategori parfum", ["Eau de Parfum", "Eau de Toilette", "Eau de Cologne", "Custom"])

if kategori == "Eau de Parfum":
    default_rasio = "2:1"
elif kategori == "Eau de Toilette":
    default_rasio = "1:1"
elif kategori == "Eau de Cologne":
    default_rasio = "1:2"
else:
    default_rasio = "1:1"

rasio_str = st.selectbox("Pilih rasio Bibit:Alkohol", list(RASIO_OPTIONS.keys()), index=list(RASIO_OPTIONS.keys()).index(default_rasio))
rasio_bibit, rasio_alkohol = RASIO_OPTIONS[rasio_str]

volume_input = st.number_input("Masukkan volume parfum (ml)", min_value=1, step=1, format="%d")

fixative_opsional = st.checkbox("Tambahkan Fixative?")
persen_fixative = st.slider("Persentase Fixative (%)", 0, 20, 5) if fixative_opsional else 0

if st.button("Hitung Komposisi"):
    if volume_input % 1 != 0:
        volume_pred = model_ml.predict([[volume_input]])[0][0]
    else:
        volume_pred = volume_input

    bibit, alkohol, fixative = hitung_komposisi(volume_pred, rasio_bibit, rasio_alkohol, persen_fixative)

    # Format ke 1 desimal dan ganti titik jadi koma
    data = pd.DataFrame({
        "No": [1, 2, 3],
        "Komponen": ["Bibit", "Alkohol", "Fixative"],
        "Volume (ml)": [bibit, alkohol, fixative]
    })

    data["Volume (ml)"] = data["Volume (ml)"].round(1).astype(str).str.replace(".", ",")

    st.table(data)

    st.markdown(
        "<p style='color:yellow; font-weight:bold;'>Ketahanan parfum tergantung kualitas bahan seperti Bibit, Alkohol serta Fixative serta bahan lainnya yang dipakai.<br>KEEP SMART AND LET'S MAKE YOUR PERFUME</p>",
        unsafe_allow_html=True
    )

















