import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import json
import os

# Daftar tugas
tugas = []

# Fungsi untuk menyimpan tugas ke file
def simpan_tugas():
    with open('tugas.json', 'w') as f:
        json.dump(tugas, f)

# Fungsi untuk memuat tugas dari file
def muat_tugas():
    global tugas
    if os.path.exists('tugas.json'):
        with open('tugas.json', 'r') as f:
            tugas = json.load(f)
        tampilkan_tugas()

# Fungsi untuk menambah tugas
def tambah_tugas():
    tugas_baru = ent_tugas.get()
    if tugas_baru != "":
        tugas.append({'task': tugas_baru, 'checked': False})
        ent_tugas.delete(0, tk.END)  # Menghapus teks di entry setelah ditambahkan
        tampilkan_tugas()
        simpan_tugas()  # Simpan tugas setelah ditambahkan
    else:
        messagebox.showwarning("Input Error", "Tugas tidak boleh kosong.")

# Fungsi untuk menghapus tugas
def hapus_tugas(idx):
    tugas.pop(idx)
    tampilkan_tugas()
    simpan_tugas()  # Simpan tugas setelah dihapus

# Fungsi untuk menampilkan tugas di Frame
def tampilkan_tugas():
    # Menghapus semua item sebelumnya
    for widget in frame_tugas.winfo_children():
        widget.destroy()

    # Menambahkan tugas baru
    for idx, t in enumerate(tugas):
        # Membuat frame untuk setiap tugas
        frame_item = ttk.Frame(frame_tugas, padding=10, bootstyle="light")
        frame_item.pack(fill="x", pady=5, padx=10)

        # Variabel untuk status centang
        var = tk.BooleanVar(value=t['checked'])
        check_button = ttk.Checkbutton(
            frame_item,
            text=t['task'],
            variable=var,
            command=lambda idx=idx, var=var: centang_tugas(idx, var),
            bootstyle="round-toggle",
        )
        check_button.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

        # Update warna berdasarkan status centang
        if t['checked']:
            frame_item.config(bootstyle="success")  # Mengubah warna frame menjadi hijau jika dicentang
        
        # Tombol hapus tugas dengan desain tombol rounded
        hapus_btn = ttk.Button(
            frame_item,
            text="🗑️",  # Ikon tempat sampah
            command=lambda idx=idx: hapus_tugas(idx),
            bootstyle="danger-outline",
            width=3
        )
        hapus_btn.pack(side=tk.RIGHT, padx=10)

# Fungsi untuk mengubah status centang tugas dan warnanya
def centang_tugas(idx, var):
    tugas[idx]['checked'] = var.get()  # Simpan status centang sebagai boolean
    if tugas[idx]['checked']:
        # Mengubah warna menjadi hijau jika dicentang
        frame_tugas.winfo_children()[idx].config(bootstyle="success")
    else:
        # Mengubah warna kembali menjadi default jika tidak dicentang
        frame_tugas.winfo_children()[idx].config(bootstyle="light")
    simpan_tugas()  # Simpan tugas setelah status centang diubah

# Membuat window utama dengan tema dari ttkbootstrap
root = ttk.Window(themename="minty")
root.title("To-Do List")
root.geometry("500x600")  # Set ukuran window

# Menggunakan font modern
custom_font = ("Helvetica", 12, "bold")

# Membuat style untuk ttk.Button
style = ttk.Style()
style.configure("TButton", font=custom_font)

# Membuat frame untuk input tugas
frame_input = ttk.Frame(root, padding=20)
frame_input.pack(pady=20, fill="x")

# Label dan entry untuk menambah tugas
label = ttk.Label(frame_input, text="Masukkan Tugas:", font=custom_font)
label.pack(side=tk.LEFT, padx=5)

# Entry untuk input tugas
ent_tugas = ttk.Entry(frame_input, width=30, font=custom_font)
ent_tugas.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

# Tombol untuk menambah tugas
tambah_btn = ttk.Button(
    root,
    text="➕ Tambah Tugas",  # Ikon tambah
    command=tambah_tugas,
    bootstyle="success",
    padding=10,
    style="TButton"  # Menggunakan style yang sudah dikonfigurasi
)
tambah_btn.pack(pady=10, fill="x", padx=20)

# Frame untuk menampilkan daftar tugas
frame_tugas = ttk.Frame(root, padding=10)
frame_tugas.pack(pady=10, fill="both", expand=True, padx=20)

# Menambahkan judul daftar tugas
judul_tugas = ttk.Label(frame_tugas, text="Daftar Tugas", font=("Helvetica", 14, "bold"), bootstyle="inverse-light")
judul_tugas.pack(fill="x", pady=5)

# Memuat tugas saat aplikasi dimulai
muat_tugas()

# Menjalankan aplikasi
root.mainloop()