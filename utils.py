import os
import requests
import sys
from tkinter import messagebox, filedialog
from fpdf import FPDF
if sys.platform == 'win32':
    import winsound

def play_notification():
    try:
        if sys.platform == 'win32':
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except Exception:
        pass

def download_file(url, target_directory, insert_text):
    try:
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        file_name = os.path.basename(url)
        file_path = os.path.join(target_directory, file_name)
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        insert_text(f"Pytha: File berhasil didownload ke {file_path}", sender='bot')
    except requests.exceptions.RequestException as e:
        insert_text(f"Pytha: Terjadi kesalahan saat mendownload file: {e}", sender='bot')

def export_pdf(chat_content, parent):
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
