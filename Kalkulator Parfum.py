import streamlit as st
import pandas as pd

# === FUNGSI PERHITUNGAN ===
def hitung_komposisi(total_ml, ratio_bibit, ratio_alkohol, persen_fixative=0):
    fixative = round((persen_fixative / 100) * total_ml) if persen_fixative > 0 else 0
    sisa_volume = total_ml - fixative
    total_ratio = ratio_bibit + ratio_alkohol
    bibit = round((ratio_bibit / total_ratio) * sisa_volume)
    alkohol = round((ratio_alkohol / total_ratio) * sisa_volume)
    return bibit, alkohol, fixative

def buat_tabel(volume_list, ratio_bibit, ratio_alkohol, persen_fixative=0):
    data = []
    for volume in volume_list:
        bibit, alkohol, fixative = hitung_komposisi(volume, ratio_bibit, ratio_alkohol, persen_fixative)
        data.append([volume, bibit, alkohol, fixative])
    return data

# === STREAMLIT UI ===
st.title("💐 Kalkulator Parfum - Rasio Bibit : Alkohol + Opsional Fixative")

# Pilihan rasio yang diperluas
pilihan_rasio = [
    "1:1", "2:1", "3:1", "4:1", "5:1",
    "1:2", "1:3", "1:4", "1:5",
    "2:3", "3:2", "4:3", "3:4"
]

rasio_pilihan = st.selectbox(
    "Pilih perbandingan Bibit : Alkohol",
    pilihan_rasio
)
ratio_bibit, ratio_alkohol = map(int, rasio_pilihan.split(":"))

# Pilihan fixative
pakai_fixative = st.checkbox("Gunakan Fixative")
persen_fixative = 0
if pakai_fixative:
    persen_fixative = st.number_input(
        "Persentase Fixative (%)", min_value=1, max_value=50, value=5
    )

# Pilih volume
mode_volume = st.radio("Pilih opsi volume:", ["Otomatis 10–100ml", "Custom"])

if mode_volume == "Otomatis 10–100ml":
    volume_list = list(range(10, 105, 5))
else:
    volume_input = st.text_input(
        "Masukkan volume (pisahkan dengan koma, contoh: 15, 30, 50):", "15, 30, 50"
    )
    try:
        volume_list = [int(v.strip()) for v in volume_input.split(",") if v.strip()]
    except ValueError:
        st.error("⚠ Masukkan angka volume yang valid.")
        volume_list = []

# Tampilkan hasil jika ada volume
if volume_list:
    tabel = buat_tabel(volume_list, ratio_bibit, ratio_alkohol, persen_fixative)
    df = pd.DataFrame(tabel, columns=["Total Volume (ml)", "Bibit (ml)", "Alkohol (ml)", "Fixative (ml)"])
    df = df.astype(int)  # tanpa koma

    st.subheader(
        f"Hasil Komposisi (Rasio Bibit:Alkohol = {ratio_bibit}:{ratio_alkohol}, Fixative = {persen_fixative}%)"
    )
    st.table(df)

    # Download CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="💾 Download CSV",
        data=csv_data,
        file_name="komposisi_parfum.csv",
        mime="text/csv"
    )
