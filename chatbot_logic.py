from responses import responses
from todo import TodoManager
import time

class ChatBotLogic:
    def __init__(self, todo_manager, insert_text, after_quit):
        self.todo_manager = todo_manager
        self.default_count = 0
        self.insert_text = insert_text
        self.after_quit = after_quit
        self.start_time = time.time()

    def process_message(self, user_input, quit_callback, filedialog, is_dark):
        user_input = user_input.strip()
        if user_input == "Ketik pesan di sini..." or not user_input:
            return
        self.insert_text("Kamu: " + user_input, sender='user')
        lower_input = user_input.lower()
        # To-Do List commands
        if lower_input == 'tugas':
            tasks = self.todo_manager.get_tasks()
            if not tasks:
                self.insert_text("Pytha: Daftar tugas kosong.", sender='bot')
            else:
                daftar = '\n'.join([f"{i+1}. {t}" for i, t in enumerate(tasks)])
                self.insert_text(f"Pytha: Daftar tugas saat ini:\n{daftar}", sender='bot')
            return
        if lower_input.startswith('+ '):
            task = user_input[2:].strip()
            if self.todo_manager.add_task(task):
                self.insert_text(f"Pytha: Tugas '{task}' berhasil ditambahkan ke daftar.", sender='bot')
            else:
                self.insert_text("Pytha: Mohon masukkan deskripsi tugas setelah '+ '", sender='bot')
            return
        if lower_input.startswith('- '):
            param = user_input[2:].strip()
            removed = None
            if param.isdigit():
                removed = self.todo_manager.remove_task(int(param)-1)
            else:
                removed = self.todo_manager.remove_task(param)
            if removed:
                self.insert_text(f"Pytha: Tugas '{removed}' berhasil dihapus.", sender='bot')
            else:
                self.insert_text("Pytha: Tugas tidak ditemukan atau nomor tidak valid.", sender='bot')
            return
        # Exit command
        if user_input.lower() in ['exit', 'quit']:
            self.insert_text("Pytha: Keluar dari program dalam 3 detik...", sender='bot')
            quit_callback(3000)
            return
        # Download command
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
            return url, target_directory
        # Keyword-based response
        respon_ditemukan = False
        for keyword, reply in responses.items():
            if keyword in user_input.lower() and keyword != "default":
                self.insert_text("Pytha: " + reply, sender='bot')
                respon_ditemukan = True
                self.default_count = 0
                break
        if not respon_ditemukan:
            default_reply = responses.get("default", "Maaf, saya kurang paham. Bisa coba diutarakan dengan kata lain?")
            self.insert_text(f"Pytha: {default_reply}", sender='bot')
            self.default_count += 1
            if self.default_count >= 3:
                self.default_count = 0
                fitur = (
                    "\nFitur Pytha Bot:\n"
                    "- To-Do List: tambah tugas: <isi tugas> | lihat tugas | hapus tugas: <nomor/isi>\n"
                    "- Simpan chat: klik tombol Simpan Chat\n"
                    "- Buka chat: klik tombol Buka Chat\n"
                    "- Copy chat: klik tombol Copy Chat\n"
                    "- Export PDF: klik tombol Export PDF\n"
                    "- Download file: download <url>\n"
                    "- Mode gelap/terang: klik tombol 🌙/☀️\n"
                    "- Keluar: exit atau quit\n"
                    "Contoh: tambah tugas: Beli susu\n"
                )
                self.insert_text(f"Pytha: Berikut fitur yang bisa kamu gunakan:{fitur}", sender='bot')
        return None, None

    def quit_chat(self, root):
        end_time = time.time()
        elapsed_time = int(end_time - self.start_time)
        self.insert_text(f"Pytha: Total waktu percakapan kamu adalah {elapsed_time} detik.", sender='bot')
        self.insert_text("Pytha: Sampai jumpa!", sender='bot')
        root.after(1000, root.destroy)
