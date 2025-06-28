import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import time
import requests
from chat_io import export_pdf, save_chat, load_chat, copy_chat
from notifier import play_notification
from ui_config import LIGHT_THEME, DARK_THEME, FONT_MAIN, FONT_BOLD, FONT_TITLE, FONT_DESC
from windows_commands import handle_windows_command
from responses import responses
from todo_manager import TodoManager
import os
from fpdf import FPDF

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.is_dark = False
        root.title("Pytha Bot")
        root.configure(bg="#f5f6fa")
        # Menu bar
        menubar = tk.Menu(root)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Tentang Bot", command=self.show_about)
        menubar.add_cascade(label="Info", menu=about_menu)
        root.config(menu=menubar)
        # Mode toggle
        self.mode_button = tk.Button(root, text="🌙 Mode Gelap", command=self.toggle_mode, bg="#dfe6e9", fg="#222", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self.mode_button.grid(row=6, column=0, pady=(0, 5), sticky="e")
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
        # Shortcut keyboard
        root.bind('<Control-s>', lambda e: self.save_chat())
        root.bind('<Control-l>', lambda e: self.load_chat())
        root.bind('<Control-c>', lambda e: self.copy_chat())
        root.bind('<Control-k>', lambda e: self.clear_chat())
        # Tombol untuk mengirim pesan
        self.send_button = tk.Button(self.entry_frame, text="Kirim", command=self.send_message, bg="#00a8ff", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self.send_button.pack(side=tk.LEFT)
        # Tombol untuk membersihkan chat
        self.clear_button = tk.Button(root, text="Bersihkan Chat", command=self.clear_chat, bg="#e84118", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.clear_button.grid(row=4, column=0, pady=(0, 10), sticky="ew")
        # Frame untuk tombol fitur tambahan
        self.feature_frame = tk.Frame(root, bg="#f5f6fa")
        self.feature_frame.grid(row=5, column=0, pady=(0, 10), sticky="ew")
        # Tombol simpan chat
        self.save_button = tk.Button(self.feature_frame, text="Simpan Chat", command=self.save_chat, bg="#44bd32", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.save_button.pack(side=tk.LEFT, padx=5)
        # Tombol buka chat
        self.load_button = tk.Button(self.feature_frame, text="Buka Chat", command=self.load_chat, bg="#273c75", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.load_button.pack(side=tk.LEFT, padx=5)
        # Tombol copy chat
        self.copy_button = tk.Button(self.feature_frame, text="Copy Chat", command=self.copy_chat, bg="#fbc531", fg="#222", font=("Segoe UI", 10), relief=tk.FLAT)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        # Tombol export PDF
        self.export_pdf_button = tk.Button(self.feature_frame, text="Export PDF", command=self.export_pdf, bg="#6c5ce7", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.export_pdf_button.pack(side=tk.LEFT, padx=5)
        # Tombol To-Do List
        self.todo_button = tk.Button(self.feature_frame, text="To-Do List", command=self.show_todo_popup, bg="#00b894", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.todo_button.pack(side=tk.LEFT, padx=5)
        # Tampilkan pesan sambutan
        self.insert_text("Pytha: Selamat datang di Pytha bot!", sender='bot')
        # Inisialisasi daftar tugas
        self.todo_manager = TodoManager()
        self.default_count = 0

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

    def export_pdf(self):
        chat_content = self.conversation_area.get(1.0, tk.END).strip()
        if not chat_content:
            messagebox.showinfo("Info", "Tidak ada chat untuk diekspor.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Export Chat ke PDF")
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in chat_content.splitlines():
                pdf.cell(0, 10, txt=line, ln=1)
            pdf.output(file_path)
            messagebox.showinfo("Sukses", f"Chat berhasil diekspor ke {file_path}")

    def play_notification(self):
        play_notification()

    def insert_text(self, text, sender=None):
        """Menambahkan teks ke area percakapan dengan warna berbeda."""
        self.conversation_area.configure(state='normal')
        timestamp = time.strftime("[%H:%M:%S] ")
        if sender == 'user':
            self.conversation_area.insert(tk.END, timestamp + text + "\n", 'user')
        elif sender == 'bot':
            self.conversation_area.insert(tk.END, timestamp + text + "\n", 'bot')
            self.play_notification()
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

    def save_chat(self):
        chat_content = self.conversation_area.get(1.0, tk.END).strip()
        if not chat_content:
            messagebox.showinfo("Info", "Tidak ada chat untuk disimpan.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Simpan Riwayat Chat")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(chat_content)
            messagebox.showinfo("Sukses", f"Chat berhasil disimpan di {file_path}")

    def load_chat(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], title="Buka Riwayat Chat")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                chat_content = f.read()
            self.conversation_area.configure(state='normal')
            self.conversation_area.delete(1.0, tk.END)
            self.conversation_area.insert(tk.END, chat_content)
            self.conversation_area.configure(state='disabled')
            self.insert_text("\n[Riwayat chat dimuat]", sender='info')

    def copy_chat(self):
        chat_content = self.conversation_area.get(1.0, tk.END).strip()
        if chat_content:
            self.root.clipboard_clear()
            self.root.clipboard_append(chat_content)
            messagebox.showinfo("Disalin", "Seluruh chat telah disalin ke clipboard.")
        else:
            messagebox.showinfo("Info", "Tidak ada chat untuk disalin.")

    def toggle_mode(self):
        self.is_dark = not self.is_dark
        if self.is_dark:
            self.root.configure(bg="#222f3e")
            self.title_label.configure(bg="#222f3e", fg="#feca57")
            self.desc_label.configure(bg="#222f3e", fg="#c8d6e5")
            self.entry_frame.configure(bg="#222f3e")
            self.feature_frame.configure(bg="#222f3e")
            self.conversation_area.configure(bg="#222f3e", fg="#f5f6fa", insertbackground="#f5f6fa")
            self.input_entry.configure(bg="#576574", fg="#f5f6fa", insertbackground="#f5f6fa")
            self.mode_button.configure(text="☀️ Mode Terang", bg="#222f3e", fg="#feca57")
            self.send_button.configure(bg="#0984e3", fg="#f5f6fa")
            self.clear_button.configure(bg="#d63031", fg="#f6f6fa")
            self.save_button.configure(bg="#00b894", fg="#f6f6fa")
            self.load_button.configure(bg="#636e72", fg="#f6f6fa")
            self.copy_button.configure(bg="#fdcb6e", fg="#222f3e")
            # Update tag warna area chat agar kontras di mode gelap
            self.conversation_area.tag_configure('user', foreground='#74b9ff', font=("Segoe UI", 11, "bold"))
            self.conversation_area.tag_configure('bot', foreground='#feca57', font=("Segoe UI", 11))
            self.conversation_area.tag_configure('separator', foreground='#636e72', font=("Segoe UI", 11, "bold"))
            self.conversation_area.tag_configure('info', foreground='#c8d6e5', font=("Segoe UI", 11, "italic"))
            # Placeholder kontras
            if self.input_entry.get() == "" or self.input_entry.get() == "Ketik pesan di sini...":
                self.input_entry.config(fg="#b2bec3")
        else:
            self.root.configure(bg="#f5f6fa")
            self.title_label.configure(bg="#f5f6fa", fg="#273c75")
            self.desc_label.configure(bg="#f5f6fa", fg="#353b48")
            self.entry_frame.configure(bg="#f5f6fa")
            self.feature_frame.configure(bg="#f5f6fa")
            self.conversation_area.configure(bg="#f5f6fa", fg="#222", insertbackground="#222")
            self.input_entry.configure(bg="#fff", fg="#222", insertbackground="#222")
            self.mode_button.configure(text="🌙 Mode Gelap", bg="#dfe6e9", fg="#222")
            self.send_button.configure(bg="#00a8ff", fg="white")
            self.clear_button.configure(bg="#e84118", fg="white")
            self.save_button.configure(bg="#44bd32", fg="white")
            self.load_button.configure(bg="#273c75", fg="white")
            self.copy_button.configure(bg="#fbc531", fg="#222")
            # Kembalikan tag warna area chat ke mode terang
            self.conversation_area.tag_configure('user', foreground='#0097e6', font=("Segoe UI", 11, "bold"))
            self.conversation_area.tag_configure('bot', foreground='#353b48', font=("Segoe UI", 11))
            self.conversation_area.tag_configure('separator', foreground='#b2bec3', font=("Segoe UI", 11, "bold"))
            self.conversation_area.tag_configure('info', foreground='#636e72', font=("Segoe UI", 11, "italic"))
            # Placeholder kontras
            if self.input_entry.get() == "" or self.input_entry.get() == "Ketik pesan di sini...":
                self.input_entry.config(fg="#888")

    def show_about(self):
        messagebox.showinfo("Tentang Pytha Bot", "Pytha Bot v1.0\nChatbot GUI Python\nDikembangkan oleh rahman-wardantz\nhttps://github.com/rahman-wardantz/phyta")

    def show_todo_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("To-Do List")
        popup.geometry("350x350")
        popup.configure(bg="#f5f6fa" if not self.is_dark else "#222f3e")
        # Listbox untuk daftar tugas
        listbox = tk.Listbox(popup, font=("Segoe UI", 11), width=35, height=12)
        listbox.pack(pady=10)
        for t in self.todo_manager.get_list():
            listbox.insert(tk.END, t)
        # Entry tambah tugas
        entry = tk.Entry(popup, font=("Segoe UI", 11), width=25)
        entry.pack(side=tk.LEFT, padx=(10,0), pady=5)
        def add_task():
            task = entry.get().strip()
            ok, msg = self.todo_manager.add_task(task)
            if ok:
                listbox.insert(tk.END, task)
                entry.delete(0, tk.END)
            # Optional: tampilkan pesan jika gagal
        add_btn = tk.Button(popup, text="+", command=add_task, bg="#44bd32", fg="white", font=("Segoe UI", 10, "bold"))
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        def del_task():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                self.todo_manager.todo_list.pop(idx)
                listbox.delete(idx)
        del_btn = tk.Button(popup, text="Hapus", command=del_task, bg="#e84118", fg="white", font=("Segoe UI", 10))
        del_btn.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message(self, event=None):
        """Mengambil input dari pengguna, memproses, dan menampilkan respons."""
        user_input = self.input_entry.get().strip()
        if user_input == "Ketik pesan di sini..." or not user_input:
            return
        # Tampilkan pesan dari pengguna
        self.insert_text("Kamu: " + user_input, sender='user')
        self.input_entry.delete(0, tk.END)
        self.input_entry.config(fg="#222")
        lower_input = user_input.lower()
        # Cek perintah Windows (pindah ke modul terpisah)
        handled, message = handle_windows_command(lower_input, user_input, self.root)
        if handled:
            if message:
                self.insert_text(message, sender='bot')
            return
        # To-Do List praktis
        if lower_input == 'tugas':
            ok, msg = self.todo_manager.list_tasks()
            self.insert_text(f"Pytha: {msg}", sender='bot')
            return
        if lower_input.startswith('+ '):
            task = user_input[2:].strip()
            ok, msg = self.todo_manager.add_task(task)
            self.insert_text(f"Pytha: {msg}", sender='bot')
            return
        if lower_input.startswith('- '):
            param = user_input[2:].strip()
            ok, msg = self.todo_manager.remove_task(param)
            self.insert_text(f"Pytha: {msg}", sender='bot')
            return
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
            if keyword in user_input.lower() and keyword != "default":
                self.insert_text("Pytha: " + reply, sender='bot')
                respon_ditemukan = True
                self.default_count = 0  # Reset jika ada respons valid
        if not respon_ditemukan:
            default_reply = responses.get("default", "Maaf, saya kurang paham. Bisa coba diutarakan dengan kata lain?")
            self.insert_text(f"Pytha: {default_reply}", sender='bot')
            self.default_count += 1
            if self.default_count >= 3:
                self.insert_text("Pytha: Jika kamu butuh bantuan lebih lanjut, silakan cek dokumentasi atau hubungi pengembang.", sender='bot')
                self.default_count = 0

    def quit_chat(self):
        """Menghitung waktu percakapan dan keluar dari program."""
        end_time = time.time()
        elapsed_time = int(end_time - self.start_time)
        self.insert_text(f"Pytha: Total waktu percakapan kamu adalah {elapsed_time} detik.", sender='bot')
        self.insert_text("Pytha: Sampai jumpa!", sender='bot')
        # Tutup jendela setelah 1 detik untuk memberikan waktu membaca pesan
        self.root.after(1000, self.root.destroy)
