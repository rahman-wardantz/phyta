import tkinter as tk
from tkinter import scrolledtext
import time
from responses import responses

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        root.title("Phyta Bot")
        
        # Catat waktu mulai percakapan
        self.start_time = time.time()

        # Area percakapan dengan scrollbar
        self.conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20)
        self.conversation_area.pack(padx=10, pady=10)

        # Frame untuk masukan teks dan tombol kirim
        self.entry_frame = tk.Frame(root)
        self.entry_frame.pack(pady=10)

        # Entry untuk input pengguna
        self.input_entry = tk.Entry(self.entry_frame, width=50)
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.input_entry.bind("<Return>", self.send_message)  # kirim ketika tekan Enter

        # Tombol untuk mengirim pesan
        self.send_button = tk.Button(self.entry_frame, text="Kirim", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        # Tampilkan pesan sambutan
        self.insert_text("Phyta: Selamat datang di Phyta bot!")

    def insert_text(self, text):
        """Menambahkan teks ke area percakapan."""
        self.conversation_area.configure(state='normal')
        self.conversation_area.insert(tk.END, text + "\n")
        self.conversation_area.configure(state='disabled')
        self.conversation_area.yview(tk.END)

    def send_message(self, event=None):
        """Mengambil input dari pengguna, memproses, dan menampilkan respons."""
        user_input = self.input_entry.get().strip().lower()
        if not user_input:
            return

        # Tampilkan pesan dari pengguna
        self.insert_text("Kamu: " + user_input)
        self.input_entry.delete(0, tk.END)

        # Jika input adalah perintah untuk keluar
        if user_input in ['exit', 'quit']:
            self.insert_text("Phyta: Keluar dari program dalam 3 detik...")
            self.root.after(3000, self.quit_chat)
            return

        # Cari respons berdasarkan kata kunci
        respon_ditemukan = False
        for keyword, reply in responses.items():
            if keyword in user_input:
                self.insert_text("Phyta: " + reply)
                respon_ditemukan = True
                break

        # Jika tidak ada kecocokan respons
        if not respon_ditemukan:
            self.insert_text(f"Phyta: Kamu mengatakan '{user_input}'")

    def quit_chat(self):
        """Menghitung waktu percakapan dan keluar dari program."""
        end_time = time.time()
        elapsed_time = int(end_time - self.start_time)
        self.insert_text(f"Phyta: Total waktu percakapan kamu adalah {elapsed_time} detik.")
        self.insert_text("Phyta: Sampai jumpa!")
        # Tutup jendela setelah 1 detik untuk memberikan waktu membaca pesan
        self.root.after(1000, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()