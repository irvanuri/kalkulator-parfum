import csv
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)

# === DATA KATEGORI PARFUM ===
KATEGORI_PARFUM = {
    "1": {"nama": "Eau de Parfum", "persen_bibit": 20, "persen_fixative": 5},
    "2": {"nama": "Eau de Toilette", "persen_bibit": 15, "persen_fixative": 5},
    "3": {"nama": "Eau de Cologne", "persen_bibit": 8, "persen_fixative": 5}
}

# === FUNGSI PERHITUNGAN ===
def hitung_komposisi(total_ml, persen_bibit, persen_fixative=5):
    bibit = round((persen_bibit / 100) * total_ml, 2)
    fixative = round((persen_fixative / 100) * total_ml, 2)
    alkohol = round(total_ml - (bibit + fixative), 2)
    return bibit, fixative, alkohol

def buat_tabel(volume_list, persen_bibit, persen_fixative=5):
    data = []
    for volume in volume_list:
        bibit, fixative, alkohol = hitung_komposisi(volume, persen_bibit, persen_fixative)
        data.append([f"{volume} ml", f"{bibit} ml", f"{fixative} ml", f"{alkohol} ml"])
    return data

# === FUNGSI EXPORT CSV ===
def export_csv(data, headers, filename="komposisi_parfum.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([h.replace(Fore.MAGENTA, "").replace(Style.RESET_ALL, "") for h in headers])
        for row in data:
            writer.writerow(row)
    print(Fore.GREEN + f"\n✅ Data berhasil disimpan ke {filename}\n" + Style.RESET_ALL)

# === MENU PILIH KATEGORI ===
def pilih_kategori():
    print(Fore.GREEN + Style.BRIGHT + "=== Kalkulator Komposisi Parfum ===" + Style.RESET_ALL)
    print("Pilih kategori parfum:")
    for kode, info in KATEGORI_PARFUM.items():
        print(Fore.CYAN + f"{kode}. {info['nama']} ({info['persen_bibit']}% Bibit, {info['persen_fixative']}% Fixative)")
    print("4. Custom (masukkan persentase sendiri)" + Style.RESET_ALL)

    while True:
        pilihan = input(Fore.YELLOW + "\nMasukkan pilihan (1–4): " + Style.RESET_ALL).strip()
        if pilihan in KATEGORI_PARFUM:
            return KATEGORI_PARFUM[pilihan]
        elif pilihan == "4":
            try:
                persen_bibit = float(input("Masukkan persentase bibit parfum (%): "))
                persen_fixative = float(input("Masukkan persentase fixative (%): "))
                return {"nama": "Custom", "persen_bibit": persen_bibit, "persen_fixative": persen_fixative}
            except ValueError:
                print(Fore.RED + "⚠ Masukkan angka yang valid!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "⚠ Pilihan tidak valid. Coba lagi." + Style.RESET_ALL)

# === MENU PILIH VOLUME ===
def pilih_volume():
    print("\nPilih opsi volume:")
    print("1. Otomatis 10ml–100ml (kelipatan 5ml)")
    print("2. Masukkan volume sendiri (pisahkan dengan koma)")

    while True:
        pilihan = input(Fore.YELLOW + "\nMasukkan pilihan (1/2): " + Style.RESET_ALL).strip()
        if pilihan == "1":
            return list(range(10, 105, 5))
        elif pilihan == "2":
            try:
                volume_list = [float(v.strip()) for v in input("Masukkan volume (contoh: 15, 30, 50): ").split(",")]
                if all(10 <= v <= 100 for v in volume_list):
                    return volume_list
                else:
                    print(Fore.RED + "⚠ Volume harus antara 10–100 ml" + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "⚠ Masukkan angka valid!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "⚠ Pilihan tidak valid." + Style.RESET_ALL)

# === MENU UTAMA ===
def main():
    kategori = pilih_kategori()
    volume_list = pilih_volume()

    # Buat tabel hasil
    tabel = buat_tabel(volume_list, kategori["persen_bibit"], kategori["persen_fixative"])
    headers = [Fore.MAGENTA + "Volume" + Style.RESET_ALL,
               Fore.MAGENTA + "Bibit" + Style.RESET_ALL,
               Fore.MAGENTA + "Fixative" + Style.RESET_ALL,
               Fore.MAGENTA + "Alkohol" + Style.RESET_ALL]

    print("\n" + Fore.GREEN + Style.BRIGHT + f"=== Komposisi untuk {kategori['nama']} ===" + Style.RESET_ALL)
    print(tabulate(tabel, headers=headers, tablefmt="fancy_grid"))

    # Simpan ke CSV
    simpan = input(Fore.YELLOW + "\nSimpan hasil ke CSV? (y/n): " + Style.RESET_ALL).strip().lower()
    if simpan == "y":
        export_csv(tabel, headers)

    # Simpan ke riwayat
    with open("riwayat_perhitungan.txt", "a", encoding="utf-8") as f:
        f.write(f"{kategori['nama']} - Persen Bibit: {kategori['persen_bibit']}%, Fixative: {kategori['persen_fixative']}%\n")
        for row in tabel:
            f.write(", ".join(row) + "\n")
        f.write("\n")

    print(Fore.CYAN + "Riwayat perhitungan disimpan ke riwayat_perhitungan.txt\n" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
