import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox

class ChatBotUI:
    def __init__(self, root, callbacks, is_dark_callback):
        self.root = root
        self.is_dark_callback = is_dark_callback
        self.callbacks = callbacks
        # Menu bar
        menubar = tk.Menu(root)
        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="Tentang Bot", command=callbacks['show_about'])
        menubar.add_cascade(label="Info", menu=about_menu)
        root.config(menu=menubar)
        # Mode toggle
        self.mode_button = tk.Button(root, text="🌙 Mode Gelap", command=callbacks['toggle_mode'], bg="#dfe6e9", fg="#222", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self.mode_button.grid(row=6, column=0, pady=(0, 5), sticky="e")
        # Responsive root window
        root.rowconfigure(2, weight=1)
        root.columnconfigure(0, weight=1)
        # Title and description
        self.title_label = tk.Label(root, text="Pytha Bot", font=("Segoe UI", 18, "bold"), bg="#f5f6fa", fg="#273c75")
        self.title_label.grid(row=0, column=0, pady=(15, 0), sticky="ew")
        self.desc_label = tk.Label(root, text="Asisten Chat Sederhana Berbasis Python", font=("Segoe UI", 10), bg="#f5f6fa", fg="#353b48")
        self.desc_label.grid(row=1, column=0, pady=(0, 10), sticky="ew")
        # Conversation area
        self.conversation_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', width=60, height=20, font=("Segoe UI", 11))
        self.conversation_area.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.conversation_area.tag_configure('user', foreground='#0097e6', font=("Segoe UI", 11, "bold"))
        self.conversation_area.tag_configure('bot', foreground='#353b48', font=("Segoe UI", 11))
        self.conversation_area.tag_configure('separator', foreground='#b2bec3', font=("Segoe UI", 11, "bold"))
        self.conversation_area.tag_configure('info', foreground='#636e72', font=("Segoe UI", 11, "italic"))
        # Entry frame
        self.entry_frame = tk.Frame(root, bg="#f5f6fa")
        self.entry_frame.grid(row=3, column=0, pady=10, sticky="ew")
        root.rowconfigure(3, weight=0)
        root.grid_columnconfigure(0, weight=1)
        # Input entry
        self.input_entry = tk.Entry(self.entry_frame, width=50, font=("Segoe UI", 11), fg="#888")
        self.input_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.BOTH, expand=True)
        self.input_entry.insert(0, "Ketik pesan di sini...")
        self.input_entry.bind("<FocusIn>", callbacks['clear_placeholder'])
        self.input_entry.bind("<FocusOut>", callbacks['add_placeholder'])
        self.input_entry.bind("<Return>", callbacks['send_message'])
        # Shortcuts
        root.bind('<Control-s>', callbacks['save_chat'])
        root.bind('<Control-l>', callbacks['load_chat'])
        root.bind('<Control-c>', callbacks['copy_chat'])
        root.bind('<Control-k>', callbacks['clear_chat'])
        # Send button
        self.send_button = tk.Button(self.entry_frame, text="Kirim", command=callbacks['send_message'], bg="#00a8ff", fg="white", font=("Segoe UI", 10, "bold"), relief=tk.FLAT)
        self.send_button.pack(side=tk.LEFT)
        # Clear button
        self.clear_button = tk.Button(root, text="Bersihkan Chat", command=callbacks['clear_chat'], bg="#e84118", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.clear_button.grid(row=4, column=0, pady=(0, 10), sticky="ew")
        # Feature frame
        self.feature_frame = tk.Frame(root, bg="#f5f6fa")
        self.feature_frame.grid(row=5, column=0, pady=(0, 10), sticky="ew")
        # Save button
        self.save_button = tk.Button(self.feature_frame, text="Simpan Chat", command=callbacks['save_chat'], bg="#44bd32", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.save_button.pack(side=tk.LEFT, padx=5)
        # Load button
        self.load_button = tk.Button(self.feature_frame, text="Buka Chat", command=callbacks['load_chat'], bg="#273c75", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.load_button.pack(side=tk.LEFT, padx=5)
        # Copy button
        self.copy_button = tk.Button(self.feature_frame, text="Copy Chat", command=callbacks['copy_chat'], bg="#fbc531", fg="#222", font=("Segoe UI", 10), relief=tk.FLAT)
        self.copy_button.pack(side=tk.LEFT, padx=5)
        # Export PDF button
        self.export_pdf_button = tk.Button(self.feature_frame, text="Export PDF", command=callbacks['export_pdf'], bg="#6c5ce7", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.export_pdf_button.pack(side=tk.LEFT, padx=5)
        # To-Do List button
        self.todo_button = tk.Button(self.feature_frame, text="To-Do List", command=callbacks['todo_popup'], bg="#00b894", fg="white", font=("Segoe UI", 10), relief=tk.FLAT)
        self.todo_button.pack(side=tk.LEFT, padx=5)

    # UI update methods
    def insert_text(self, text, sender=None):
        self.conversation_area.configure(state='normal')
        self.conversation_area.insert(tk.END, text + "\n", sender if sender else None)
        self.conversation_area.configure(state='disabled')
        self.conversation_area.yview(tk.END)

    def clear_chat_area(self):
        self.conversation_area.configure(state='normal')
        self.conversation_area.delete(1.0, tk.END)
        self.conversation_area.configure(state='disabled')

    def get_input(self):
        return self.input_entry.get()

    def set_input(self, value, color="#222"):
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, value)
        self.input_entry.config(fg=color)

    def get_chat_content(self):
        return self.conversation_area.get(1.0, tk.END).strip()

    def set_mode(self, dark):
        # ...mode switching code from toggle_mode...
        pass
