import csv
import streamlit as st
import pandas as pd

# === DATA KATEGORI PARFUM ===
KATEGORI_PARFUM = {
    "Eau de Parfum": {"persen_bibit": 20, "persen_fixative": 5},
    "Eau de Toilette": {"persen_bibit": 15, "persen_fixative": 5},
    "Eau de Cologne": {"persen_bibit": 8, "persen_fixative": 5},
}

# === FUNGSI PERHITUNGAN ===
def hitung_komposisi(total_ml, persen_bibit, persen_fixative=5):
    bibit = round((persen_bibit / 100) * total_ml)
    fixative = round((persen_fixative / 100) * total_ml)
    alkohol = round(total_ml - (bibit + fixative))
    return bibit, fixative, alkohol

def buat_tabel(volume_list, persen_bibit, persen_fixative=5):
    data = []
    for volume in volume_list:
        bibit, fixative, alkohol = hitung_komposisi(volume, persen_bibit, persen_fixative)
        data.append([volume, bibit, fixative, alkohol])
    return data

# === STREAMLIT UI ===
st.title("💐 Kalkulator Komposisi Parfum")

# Pilih kategori parfum
kategori_pilihan = st.selectbox(
    "Pilih kategori parfum:",
    list(KATEGORI_PARFUM.keys()) + ["Custom"]
)

if kategori_pilihan == "Custom":
    persen_bibit = st.number_input("Persentase bibit parfum (%)", min_value=0, max_value=100, value=20)
    persen_fixative = st.number_input("Persentase fixative (%)", min_value=0, max_value=100, value=5)
else:
    persen_bibit = KATEGORI_PARFUM[kategori_pilihan]["persen_bibit"]
    persen_fixative = KATEGORI_PARFUM[kategori_pilihan]["persen_fixative"]

# Pilih volume
mode_volume = st.radio("Pilih opsi volume:", ["Otomatis 10–100ml", "Custom"])

if mode_volume == "Otomatis 10–100ml":
    volume_list = list(range(10, 105, 5))
else:
    volume_input = st.text_input("Masukkan volume (pisahkan dengan koma, contoh: 15, 30, 50):", "15, 30, 50")
    try:
        volume_list = [float(v.strip()) for v in volume_input.split(",") if v.strip()]
    except ValueError:
        st.error("⚠ Masukkan angka volume yang valid.")
        volume_list = []

# Tampilkan hasil jika ada volume
if volume_list:
    tabel = buat_tabel(volume_list, persen_bibit, persen_fixative)
    df = pd.DataFrame(tabel, columns=["Volume (ml)", "Bibit (ml)", "Fixative (ml)", "Alkohol (ml)"])
    df = df.astype(int)

    st.subheader(f"Hasil Komposisi untuk {kategori_pilihan}")
    st.table(df)

    # Download CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Download CSV",
        data=csv_data,
        file_name="komposisi_parfum.csv",
        mime="text/csv"
    )


