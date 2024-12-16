import tkinter as tk
from tkinter import messagebox
import time
import sys
sys.setrecursionlimit(80000)  # Increase the limit to 2000 or higher as needed

# Daftar Stopwords
stopwords = {
    'yang', 'untuk', 'dengan', 'di', 'ke', 'pada', 'adalah', 'itu', 'dan', 'tersebut',
    'saya', 'kami', 'mereka', 'memiliki', 'menjadi', 'menyebabkan', 'menggunakan', 'untuk',
    'seperti', 'mempunyai', 'menulis', 'berada', 'menghadapi', 'belajar', 'setiap',
    'akan', 'sudah', 'sedang', 'dari', 'dalam', 'sebuah', 'hingga' , 'ini' , 'aku', 'hari' ,'kita', 'semoga', 'merasa', 'daerah', 'sangat', 'masyarakat', 'lebih', 'banyak', 'oleh', 'memberikan'
}

# Fungsi rekursif Merge Sort
def merge_sort_rekursif(data):
    if len(data) > 1:
        mid = len(data) // 2
        left_half = data[:mid]
        right_half = data[mid:]

        merge_sort_rekursif(left_half)
        merge_sort_rekursif(right_half)

        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i][1] > right_half[j][1]:
                data[k] = left_half[i]
                i += 1
            else:
                data[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            data[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            data[k] = right_half[j]
            j += 1
            k += 1

    return data

# Fungsi iteratif Selection Sort
def selection_sort_iteratif(data):
    n = len(data)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if data[j][1] > data[max_idx][1]:
                max_idx = j
        data[i], data[max_idx] = data[max_idx], data[i]

    return data

# Fungsi iteratif untuk menghitung frekuensi hanya kata yang muncul di lebih dari satu postingan
def hitung_frekuensi_valid_iteratif(postingan_list):
    kata_ke_postingan = {}
    for idx, postingan in enumerate(postingan_list):
        kata_set = set([kata.strip('.,!?') for kata in postingan.lower().split() if kata.strip('.,!?') not in stopwords])
        for kata in kata_set:
            if kata not in kata_ke_postingan:
                kata_ke_postingan[kata] = set()
            kata_ke_postingan[kata].add(idx)
    # Hanya ambil kata yang muncul di lebih dari satu postingan
    return {kata: len(postingan_idx) for kata, postingan_idx in kata_ke_postingan.items() if len(postingan_idx) > 1}

# Fungsi rekursif untuk menghitung frekuensi hanya kata yang muncul di lebih dari satu postingan
def hitung_frekuensi_valid_rekursif(postingan_list, idx=0, hasil_sementara=None):
    if hasil_sementara is None:
        hasil_sementara = {}

    if idx >= len(postingan_list):  # Basis rekursif
        # Hanya ambil kata yang muncul di lebih dari satu postingan
        return {kata: len(postingan_idx) for kata, postingan_idx in hasil_sementara.items() if len(postingan_idx) > 1}

    # Proses postingan saat ini
    postingan = postingan_list[idx]
    kata_set = set([kata.strip('.,!?') for kata in postingan.lower().split() if kata.strip('.,!?') not in stopwords])

    for kata in kata_set:
        if kata not in hasil_sementara:
            hasil_sementara[kata] = set()
        hasil_sementara[kata].add(idx)

    # Rekursi dengan hasil akumulasi
    return hitung_frekuensi_valid_rekursif(postingan_list, idx + 1, hasil_sementara)

# Fungsi utama untuk hitung frekuensi dan sorting
def hitung_waktu_eksekusi(teks, freq_recursive=False, sort_recursive=False):
    postingan_list = [post.strip() for post in teks.split('.') if post.strip()]
    mulai = time.perf_counter()

    # Hitung frekuensi
    if freq_recursive:
        hasil_frekuensi = hitung_frekuensi_valid_rekursif(postingan_list)
    else:
        hasil_frekuensi = hitung_frekuensi_valid_iteratif(postingan_list)

    # Sorting hasil
    data = list(hasil_frekuensi.items())
    if sort_recursive:
        data = merge_sort_rekursif(data)
    else:
        data = selection_sort_iteratif(data)

    selesai = time.perf_counter()
    waktu_eksekusi = (selesai - mulai) * 1_000_000  # Waktu dalam mikrodetik
    return data, len(postingan_list), waktu_eksekusi

# Fungsi untuk tombol "Cari Tren"
def cari_tren():
    teks = input_teks.get("1.0", tk.END).strip()
    if not teks:
        messagebox.showwarning("Peringatan", "Masukkan teks terlebih dahulu!")
        return

    # Ambil pilihan pengguna dari radio button
    freq_recursive = freq_var.get() == 1
    sort_recursive = sort_var.get() == 1

    hasil, jumlah_postingan, waktu_eksekusi = hitung_waktu_eksekusi(teks, freq_recursive, sort_recursive)
    tampilkan_hasil(hasil, waktu_eksekusi, freq_recursive, sort_recursive, jumlah_postingan)

# Fungsi untuk menampilkan hasil di area output
def tampilkan_hasil(hasil, waktu_eksekusi, freq_recursive, sort_recursive, jumlah_postingan):
    output_teks.delete("1.0", tk.END)
    metode_freq = "Rekursif" if freq_recursive else "Iteratif"
    metode_sort = "Rekursif" if sort_recursive else "Iteratif"
    output_teks.insert(tk.END, f"Metode Frekuensi: {metode_freq}\n")
    output_teks.insert(tk.END, f"Metode Sorting: {metode_sort}\n")
    output_teks.insert(tk.END, f"Waktu eksekusi: {waktu_eksekusi:.2f} µs\n")
    output_teks.insert(tk.END, f"Jumlah Postingan: {jumlah_postingan}\n")
    output_teks.insert(tk.END, "\nTop tweet hangat:\n")
    for kata, frekuensi in hasil[:10]:
        output_teks.insert(tk.END, f"{kata}: {frekuensi} Postingan\n")

# Membuat jendela aplikasi
root = tk.Tk()
root.title("Aplikasi Trend Twitter")
root.configure(bg="black")

# Layout input
frame_input = tk.Frame(root, bg="black")
frame_input.pack(pady=10)
label_input = tk.Label(frame_input, text="Masukkan Data Postingan: ", font=("Arial", 12, "bold"), fg="white", bg="black")
label_input.pack(anchor="w")
input_teks = tk.Text(frame_input, height=10, width=50, font=("Arial", 12), bg="gray", fg="white", insertbackground="white")
input_teks.pack()

# Layout opsi
frame_opsi = tk.Frame(root, bg="black")
frame_opsi.pack(pady=5)

# Opsi perhitungan frekuensi
label_opsi_freq = tk.Label(frame_opsi, text="Metode Perhitungan Frekuensi:", font=("Arial", 12, "bold"), fg="white", bg="black")
label_opsi_freq.grid(row=0, column=0, sticky="w", pady=5)
freq_var = tk.IntVar(value=0)  # 0: Iteratif, 1: Rekursif
radio_iteratif_freq = tk.Radiobutton(frame_opsi, text="Iteratif", variable=freq_var, value=0, font=("Arial", 12), bg="black", fg="white", selectcolor="black")
radio_rekursif_freq = tk.Radiobutton(frame_opsi, text="Rekursif", variable=freq_var, value=1, font=("Arial", 12), bg="black", fg="white", selectcolor="black")
radio_iteratif_freq.grid(row=1, column=0, sticky="w")
radio_rekursif_freq.grid(row=2, column=0, sticky="w")

# Opsi metode sorting
label_opsi_sort = tk.Label(frame_opsi, text="Metode Sorting:", font=("Arial", 12, "bold"), fg="white", bg="black")
label_opsi_sort.grid(row=0, column=1, sticky="w", padx=20, pady=5)
sort_var = tk.IntVar(value=0)  # 0: Iteratif, 1: Rekursif
radio_iteratif_sort = tk.Radiobutton(frame_opsi, text="Iteratif", variable=sort_var, value=0, font=("Arial", 12), bg="black", fg="white", selectcolor="black")
radio_rekursif_sort = tk.Radiobutton(frame_opsi, text="Rekursif", variable=sort_var, value=1, font=("Arial", 12), bg="black", fg="white", selectcolor="black")
radio_iteratif_sort.grid(row=1, column=1, sticky="w")
radio_rekursif_sort.grid(row=2, column=1, sticky="w")

# Tombol untuk cari tren
frame_tombol = tk.Frame(root, bg="black")
frame_tombol.pack(pady=5)
button_cari = tk.Button(frame_tombol, text="Cari Tren", command=cari_tren, font=("Arial", 12), bg="#1DA1F2", fg="white", activebackground="white", activeforeground="black")
button_cari.pack()

# Layout output
frame_output = tk.Frame(root, bg="black")
frame_output.pack(pady=10)
label_output = tk.Label(frame_output, text="Hasil:", font=("Arial", 12, "bold"), fg="white", bg="black")
label_output.pack(anchor="w")
output_teks = tk.Text(frame_output, height=18, width=55, font=("Arial", 12), bg="gray", fg="white", state=tk.NORMAL, insertbackground="white")
output_teks.pack()

# Menjalankan aplikasi
root.mainloop()
