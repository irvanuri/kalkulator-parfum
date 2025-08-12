import csv
from colorama import Fore, Style, init
from tabulate import tabulate
from sklearn.linear_model import LinearRegression
import numpy as np

init(autoreset=True)

# === DATA RASIO ===
RASIO_LIST = {
    "1": (1, 1),
    "2": (2, 1),
    "3": (3, 1),
    "4": (1, 2),
    "5": (2, 3)
}

# === TRAINING MODEL UNTUK SETIAP RASIO ===
models = {}
for key, (bibit_ratio, alkohol_ratio) in RASIO_LIST.items():
    X = []
    y_bibit = []
    y_alkohol = []
    for vol in range(10, 101):
        total_part = bibit_ratio + alkohol_ratio
        bibit_ml = (bibit_ratio / total_part) * vol
        alkohol_ml = (alkohol_ratio / total_part) * vol
        X.append([vol])
        y_bibit.append(bibit_ml)
        y_alkohol.append(alkohol_ml)

    model_bibit = LinearRegression().fit(X, y_bibit)
    model_alkohol = LinearRegression().fit(X, y_alkohol)
    models[key] = (model_bibit, model_alkohol)

# === FUNGSI HITUNG KOMPOSISI ===
def hitung_komposisi_ml(volume, ratio_key, use_fixative=False, persen_fixative=5):
    model_bibit, model_alkohol = models[ratio_key]
    bibit = round(model_bibit.predict([[volume]])[0])
    alkohol = round(model_alkohol.predict([[volume]])[0])
    fixative = 0
    if use_fixative:
        fixative = round((persen_fixative / 100) * volume)
        alkohol = volume - (bibit + fixative)
    return bibit, fixative, alkohol

# === PILIH RASIO ===
def pilih_rasio():
    print("\nPilih rasio Bibit : Alkohol")
    for kode, (b, a) in RASIO_LIST.items():
        print(f"{kode}. {b}:{a}")
    while True:
        pilihan = input("Masukkan pilihan rasio: ").strip()
        if pilihan in RASIO_LIST:
            return pilihan
        else:
            print(Fore.RED + "⚠ Pilihan tidak valid." + Style.RESET_ALL)

# === MENU VOLUME ===
def pilih_volume():
    while True:
        try:
            vol = float(input("Masukkan volume parfum (ml): "))
            if 10 <= vol <= 100:
                return vol
            else:
                print(Fore.RED + "⚠ Volume harus 10–100 ml" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "⚠ Masukkan angka valid!" + Style.RESET_ALL)

# === MENU FIXATIVE ===
def pilih_fixative():
    while True:
        pilihan = input("Gunakan fixative? (y/n): ").strip().lower()
        if pilihan == "y":
            return True
        elif pilihan == "n":
            return False
        else:
            print("⚠ Pilihan tidak valid.")

# === MAIN PROGRAM ===
def main():
    print(Fore.GREEN + Style.BRIGHT + "=== Kalkulator Komposisi Parfum (ML Mode) ===" + Style.RESET_ALL)
    ratio_key = pilih_rasio()
    volume = pilih_volume()
    use_fix = pilih_fixative()

    bibit, fixative, alkohol = hitung_komposisi_ml(volume, ratio_key, use_fixative=use_fix)

    headers = ["Volume (ml)", "Bibit (ml)", "Fixative (ml)", "Alkohol (ml)"]
    tabel = [[volume, bibit, fixative, alkohol]]

    print("\n" + tabulate(tabel, headers=headers, tablefmt="fancy_grid"))

    print(Fore.CYAN + "\nThe longevity of a perfume depends on the quality of ingredients such as the fragrance concentrate, alcohol, fixative, and other materials used.")
    print("💡 KEEP SMART AND LET'S MAKE YOUR PERFUME!\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
