import tkinter as tk
from tkinter import filedialog, messagebox
import time
from todo import TodoManager
from chatbot_ui import ChatBotUI
from chatbot_logic import ChatBotLogic
from utils import play_notification, download_file, export_pdf

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.is_dark = False
        self.todo_manager = TodoManager(root, lambda: self.is_dark)
        # Callbacks for UI actions
        callbacks = {
            'show_about': self.show_about,
            'toggle_mode': self.toggle_mode,
            'clear_placeholder': self.clear_placeholder,
            'add_placeholder': self.add_placeholder,
            'send_message': self.send_message,
            'save_chat': self.save_chat,
            'load_chat': self.load_chat,
            'copy_chat': self.copy_chat,
            'clear_chat': self.clear_chat,
            'export_pdf': self.export_pdf,
            'todo_popup': self.show_todo_popup
        }
        self.ui = ChatBotUI(root, callbacks, lambda: self.is_dark)
        self.logic = ChatBotLogic(self.todo_manager, self.insert_text, self.quit_chat)
        self.ui.insert_text("Pytha: Selamat datang di Pytha bot!", sender='bot')
        self.default_count = 0
        self.start_time = time.time()

    def clear_placeholder(self, event):
        if self.ui.get_input() == "Ketik pesan di sini...":
            self.ui.set_input('', color="#222")

    def add_placeholder(self, event):
        if not self.ui.get_input():
            self.ui.set_input("Ketik pesan di sini...", color="#888")

    def clear_chat(self, event=None):
        self.ui.clear_chat_area()
        self.ui.insert_text("\n", sender=None)
        self.ui.insert_text("••••••••••••••••••••••••••••••••••••••••", sender='separator')
        self.ui.insert_text("\nChat telah dibersihkan. Mulai percakapan baru!\n", sender='info')

    def export_pdf(self):
        chat_content = self.ui.get_chat_content()
        export_pdf(chat_content, self.root)

    def insert_text(self, text, sender=None):
        timestamp = time.strftime("[%H:%M:%S] ")
        if sender in ['user', 'bot']:
            self.ui.insert_text(timestamp + text, sender=sender)
            if sender == 'bot':
                play_notification()
        else:
            self.ui.insert_text(text, sender=sender)

    def save_chat(self, event=None):
        chat_content = self.ui.get_chat_content()
        if not chat_content:
            messagebox.showinfo("Info", "Tidak ada chat untuk disimpan.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Simpan Riwayat Chat")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(chat_content)
            messagebox.showinfo("Sukses", f"Chat berhasil disimpan di {file_path}")

    def load_chat(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], title="Buka Riwayat Chat")
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                chat_content = f.read()
            self.ui.clear_chat_area()
            self.ui.insert_text(chat_content)
            self.ui.insert_text("\n[Riwayat chat dimuat]", sender='info')

    def copy_chat(self, event=None):
        chat_content = self.ui.get_chat_content()
        if chat_content:
            self.root.clipboard_clear()
            self.root.clipboard_append(chat_content)
            messagebox.showinfo("Disalin", "Seluruh chat telah disalin ke clipboard.")
        else:
            messagebox.showinfo("Info", "Tidak ada chat untuk disalin.")

    def toggle_mode(self):
        self.is_dark = not self.is_dark
        # TODO: Implement mode switching in UI
        # self.ui.set_mode(self.is_dark)

    def show_about(self):
        messagebox.showinfo("Tentang Pytha Bot", "Pytha Bot v1.0\nChatbot GUI Python\nDikembangkan oleh rahman-wardantz\nhttps://github.com/rahman-wardantz/phyta")

    def send_message(self, event=None):
        user_input = self.ui.get_input()
        self.ui.set_input('', color="#222")
        result = self.logic.process_message(user_input, self.delayed_quit, filedialog, self.is_dark)
        if isinstance(result, tuple) and result[0] and result[1]:
            # Download command
            url, target_directory = result
            download_file(url, target_directory, self.insert_text)

    def delayed_quit(self, delay):
        self.root.after(delay, lambda: self.logic.quit_chat(self.root))

    def show_todo_popup(self):
        self.todo_manager.show_todo_popup()

    def quit_chat(self):
        self.logic.quit_chat(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatBotGUI(root)
    root.mainloop()
