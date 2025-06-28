import os
import sys
from tkinter import messagebox

def handle_windows_command(lower_input, user_input, parent=None):
    """
    Menangani perintah Windows. Kembalikan (handled, message) jika perintah dikenali,
    handled: True jika perintah dijalankan, False jika tidak.
    message: pesan untuk ditampilkan di chat.
    """
    # Perintah dengan konfirmasi
    if lower_input == 'shutdown':
        if parent and messagebox.askyesno('Konfirmasi', 'Yakin ingin mematikan komputer?'):
            os.system('shutdown /s /t 1')
            return True, 'Pytha: Komputer dimatikan.'
        return True, 'Pytha: Perintah shutdown dibatalkan.'
    if lower_input == 'restart':
        if parent and messagebox.askyesno('Konfirmasi', 'Yakin ingin restart komputer?'):
            os.system('shutdown /r /t 1')
            return True, 'Pytha: Komputer direstart.'
        return True, 'Pytha: Perintah restart dibatalkan.'
    if lower_input == 'sleep':
        if parent and messagebox.askyesno('Konfirmasi', 'Yakin ingin sleep komputer?'):
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return True, 'Pytha: Komputer sleep.'
        return True, 'Pytha: Perintah sleep dibatalkan.'
    if lower_input == 'logoff':
        if parent and messagebox.askyesno('Konfirmasi', 'Yakin ingin logout user?'):
            os.system('shutdown /l')
            return True, 'Pytha: User logout.'
        return True, 'Pytha: Perintah logoff dibatalkan.'
    # Perintah tanpa konfirmasi
    commands = {
        'buka explorer': lambda: os.startfile(r'C:\\'),
        'buka notepad': lambda: os.system('start notepad'),
        'buka kalkulator': lambda: os.system('start calc'),
        'buka calculator': lambda: os.system('start calc'),
        'buka cmd': lambda: os.system('start cmd'),
        'buka powershell': lambda: os.system('start powershell'),
        'buka paint': lambda: os.system('start mspaint'),
        'buka device manager': lambda: os.system('devmgmt.msc'),
        'buka control panel': lambda: os.system('control'),
        'buka task manager': lambda: os.system('taskmgr'),
        'buka settings': lambda: os.system('start ms-settings:'),
        'buka bluetooth': lambda: os.system('start ms-settings:bluetooth'),
        'buka network': lambda: os.system('start ms-settings:network'),
        'buka windows update': lambda: os.system('start ms-settings:windowsupdate'),
        'buka run': lambda: os.system('explorer shell:::{2559a1f3-21d7-11d4-bdaf-00c04f60b9f0}'),
        'buka event viewer': lambda: os.system('eventvwr'),
        'buka services': lambda: os.system('services.msc'),
        'buka disk management': lambda: os.system('diskmgmt.msc'),
        'buka registry editor': lambda: os.system('regedit'),
        'buka snipping tool': lambda: os.system('start snippingtool'),
        'buka edge': lambda: os.system('start msedge'),
        'lock': lambda: os.system('rundll32.exe user32.dll,LockWorkStation'),
    }
    if lower_input in commands:
        try:
            commands[lower_input]()
            return True, f'Pytha: {lower_input.replace("buka ", "").capitalize()} dibuka.'
        except Exception as e:
            return True, f'Pytha: Gagal menjalankan perintah: {e}'
    if lower_input.startswith('buka explorer '):
        folder = user_input[14:].strip()
        if folder:
            try:
                os.startfile(folder)
                return True, f'Pytha: File Explorer dibuka di {folder}.'
            except Exception as e:
                return True, f'Pytha: Gagal membuka folder: {e}'
        else:
            return True, 'Pytha: Mohon masukkan path folder setelah "buka explorer".'
    return False, None
