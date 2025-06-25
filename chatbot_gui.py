import tkinter as tk
from tkinter import scrolledtext, filedialog
import time
import requests
import os
from responses import responses

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        root.title("Pytha Bot")
        root.configure(bg="#f5f6fa")
        # Membuat root window responsive
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)
        # Judul dan deskripsi
        self.title_label = tk.Label(root, text="Pytha Bot", font=("Segoe UI", 18, "bold"), bg="#f5f6fa", fg="#273c75")
        self.title_label.grid(row=0, column=0, pady=(15, 0), sticky="ew")
        self.desc_label = tk.Label(root, text="Asisten Chat Sederhana Berbasis Python", font=("Segoe UI", 10), bg="#f5f6fa", fg="#353b48")
        self.desc_label.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        # Catat waktu mulai percakapan
        self.start_time = time.time()
        # Area percakapan dengan scrollbar
        self.conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20, font=("Segoe UI", 11))
        self.conversation_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.conversation_area.tag_configure('user', foreground='#0097e6', font=("Segoe UI", 11, "bold"))
        self.conversation_area.tag_configure('bot', foreground='#353b48', font=("Segoe UI", 11))
        self.conversation_area.tag_configure('separator', foreground='#b2bec3', font=("Segoe UI", 11, "bold"))
        self.conversation_area.tag_configure('info', foreground='#636e72', font=("Segoe UI", 11, "italic"))
        # Frame untuk masukan teks dan tombol kirim
        self.entry_frame = tk.Frame(root, bg="#f5f6fa")
        self.entry_frame.grid(row=3, column=0, pady=10, sticky="ew")
        root.rowconfigure(3, weight=0)
        root.grid_columnconfigure(0, weight=1)
        # Entry untuk input pengguna dengan placeholder
        self.input_entry = tk.Entry(self.entry_frame, width=50, font=("Segoe UI", 11), fg="#888")
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
        self.input_entry.insert(0, "Ketik pesan di sini...")
        self.input_entry.bind("<FocusIn>", self.clear_placeholder)
        self.input_entry.bind("<FocusOut>", self.add_placeholder)
        self.input_entry.bind("<Return>", self.send_message)  # Kirim ketika tekan Enter
        # Tombol untuk mengirim pesan
        self.send_button = tk.Button(self.entry_frame, text="Kirim", command=self.send_message, bg="#00a8ff", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self.send_button.pack(side=tk.LEFT)
        # Tombol untuk membersihkan chat
        self.clear_button = tk.Button(root, text="Bersihkan Chat", command=self.clear_chat, bg="#e84118", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.clear_button.grid(row=4, column=0, pady=(0, 10), sticky="ew")
        # Tampilkan pesan sambutan
        self.insert_text("Pytha: Selamat datang di Pytha bot!", sender='bot')

    def clear_placeholder(self, event):
        if self.input_entry.get() == "Ketik pesan di sini...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.config(fg="#222")

    def add_placeholder(self, event):
        if not self.input_entry.get():
            self.input_entry.insert(0, "Ketik pesan di sini...")
            self.input_entry.config(fg="#888")

    def clear_chat(self):
        self.conversation_area.configure(state='normal')
        self.conversation_area.delete(1.0, tk.END)
        self.conversation_area.configure(state='disabled')
        # Tambahkan jarak, separator, dan pesan dengan UX lebih baik
        self.insert_text("\n", sender=None)
        self.insert_text("••••••••••••••••••••••••••••••••••••••••", sender='separator')
        self.insert_text("\nChat telah dibersihkan. Mulai percakapan baru!\n", sender='info')

    def insert_text(self, text, sender=None):
        """Menambahkan teks ke area percakapan dengan warna berbeda."""
        self.conversation_area.configure(state='normal')
        if sender == 'user':
            self.conversation_area.insert(tk.END, text + "\n", 'user')
        elif sender == 'bot':
            self.conversation_area.insert(tk.END, text + "\n", 'bot')
        elif sender == 'separator':
            self.conversation_area.insert(tk.END, text + "\n", 'separator')
        elif sender == 'info':
            self.conversation_area.insert(tk.END, text + "\n", 'info')
        else:
            self.conversation_area.insert(tk.END, text + "\n")
        self.conversation_area.configure(state='disabled')
        self.conversation_area.yview(tk.END)

    def download_file(self, url, target_directory):
        """Mendownload file dari URL dan menyimpannya ke direktori yang dipilih."""
        try:
            # Pastikan direktori tujuan ada, jika tidak ada maka dibuat
            if not os.path.exists(target_directory):
                os.makedirs(target_directory)
            file_name = os.path.basename(url)
            file_path = os.path.join(target_directory, file_name)
            # Lakukan download dengan streaming agar tidak membebani memori
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Tangani error HTTP
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
            self.insert_text(f"Pytha: File berhasil didownload ke {file_path}", sender='bot')
        except requests.exceptions.RequestException as e:
            self.insert_text(f"Pytha: Terjadi kesalahan saat mendownload file: {e}", sender='bot')

    def send_message(self, event=None):
        """Mengambil input dari pengguna, memproses, dan menampilkan respons."""
        user_input = self.input_entry.get().strip()
        if user_input == "Ketik pesan di sini..." or not user_input:
            return
        # Tampilkan pesan dari pengguna
        self.insert_text("Kamu: " + user_input, sender='user')
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(fg="#222")
        # Jika input adalah perintah untuk keluar
        if user_input.lower() in ['exit', 'quit']:
            self.insert_text("Pytha: Keluar dari program dalam 3 detik...", sender='bot')
            self.root.after(3000, self.quit_chat)
            return
        # Cek apakah perintah untuk mendownload file
        if user_input.lower().startswith("download"):
            parts = user_input.split()
            if len(parts) < 2:
                self.insert_text("Pytha: Mohon masukkan URL file yang valid setelah perintah download.", sender='bot')
                return
            url = parts[1]
            target_directory = filedialog.askdirectory(title="Pilih Direktori Tujuan")
            if not target_directory:
                self.insert_text("Pytha: Direktori tujuan tidak dipilih. Proses download dibatalkan.", sender='bot')
                return
            self.insert_text("Pytha: Sedang mendownload file, harap tunggu...", sender='bot')
            self.download_file(url, target_directory)
            return
        # Cari respons berdasarkan kata kunci dari dictionary responses
        respon_ditemukan = False
        for keyword, reply in responses.items():
            if keyword in user_input.lower():
                self.insert_text("Pytha: " + reply, sender='bot')
                respon_ditemukan = True
                break
        # Jika tidak ada kecocokan respons, tampilkan input pengguna
        if not respon_ditemukan:
            self.insert_text(f"Pytha: Kamu mengatakan '{user_input}'", sender='bot')

    def quit_chat(self):
        """Menghitung waktu percakapan dan keluar dari program."""
        end_time = time.time()
        elapsed_time = int(end_time - self.start_time)
        self.insert_text(f"Pytha: Total waktu percakapan kamu adalah {elapsed_time} detik.", sender='bot')
        self.insert_text("Pytha: Sampai jumpa!", sender='bot')
        # Tutup jendela setelah 1 detik untuk memberikan waktu membaca pesan
        self.root.after(1000, self.root.destroy)
