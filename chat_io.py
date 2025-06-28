from tkinter import filedialog, messagebox
from fpdf import FPDF

def export_pdf(conversation_area):
    chat_content = conversation_area.get(1.0, 'end').strip()
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

def save_chat(conversation_area):
    chat_content = conversation_area.get(1.0, 'end').strip()
    if not chat_content:
        messagebox.showinfo("Info", "Tidak ada chat untuk disimpan.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")], title="Simpan Riwayat Chat")
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(chat_content)
        messagebox.showinfo("Sukses", f"Chat berhasil disimpan di {file_path}")

def load_chat(conversation_area):
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], title="Buka Riwayat Chat")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as f:
            chat_content = f.read()
        conversation_area.configure(state='normal')
        conversation_area.delete(1.0, 'end')
        conversation_area.insert('end', chat_content)
        conversation_area.configure(state='disabled')
        return True
    return False

def copy_chat(conversation_area, root):
    chat_content = conversation_area.get(1.0, 'end').strip()
    if chat_content:
        root.clipboard_clear()
        root.clipboard_append(chat_content)
        messagebox.showinfo("Disalin", "Seluruh chat telah disalin ke clipboard.")
    else:
        messagebox.showinfo("Info", "Tidak ada chat untuk disalin.")

def show_help(root=None):
    help_text = (
        "Panduan Penggunaan Pytha Bot:\n"
        "- Ketik pesan apapun untuk mendapatkan respons.\n"
        "- To-Do List: \n"
        "    - 'tugas' untuk melihat daftar tugas\n"
        "    - '+ <tugas>' untuk menambah tugas\n"
        "    - '- <nomor/teks>' untuk menghapus tugas\n"
        "- Fitur Windows: \n"
        "    - 'buka notepad', 'buka kalkulator', 'buka explorer', dll\n"
        "- Download file: \n"
        "    - 'download <url>'\n"
        "- Fitur chat: \n"
        "    - Simpan, buka, copy, export PDF chat dari menu fitur\n"
        "- Mode gelap/terang: klik tombol di pojok kanan atas\n"
        "- Ketik 'help' untuk menampilkan panduan ini\n"
        "- Ketik 'exit' atau 'quit' untuk keluar\n"
    )
    if root:
        from tkinter import messagebox
        messagebox.showinfo("Panduan Pytha Bot", help_text)
    return help_text
