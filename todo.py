import tkinter as tk

class TodoManager:
    def __init__(self, root, is_dark_callback):
        self.root = root
        self.todo_list = []
        self.is_dark_callback = is_dark_callback  # function to check dark mode

    def add_task(self, task):
        if task:
            self.todo_list.append(task)
            return True
        return False

    def remove_task(self, idx_or_text):
        if isinstance(idx_or_text, int):
            if 0 <= idx_or_text < len(self.todo_list):
                return self.todo_list.pop(idx_or_text)
        else:
            for i, t in enumerate(self.todo_list):
                if idx_or_text.lower() in t.lower():
                    return self.todo_list.pop(i)
        return None

    def get_tasks(self):
        return self.todo_list

    def show_todo_popup(self):
        popup = tk.Toplevel(self.root)
        popup.title("To-Do List")
        popup.geometry("350x350")
        popup.configure(bg="#f5f6fa" if not self.is_dark_callback() else "#222f3e")
        listbox = tk.Listbox(popup, font=("Segoe UI", 11), width=35, height=12)
        listbox.pack(pady=10)
        for t in self.todo_list:
            listbox.insert(tk.END, t)
        entry = tk.Entry(popup, font=("Segoe UI", 11), width=25)
        entry.pack(side=tk.LEFT, padx=(10,0), pady=5)
        def add_task_popup():
            task = entry.get().strip()
            if self.add_task(task):
                listbox.insert(tk.END, task)
                entry.delete(0, tk.END)
        add_btn = tk.Button(popup, text="+", command=add_task_popup, bg="#44bd32", fg="white", font=("Segoe UI", 10, "bold"))
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        def del_task_popup():
            sel = listbox.curselection()
            if sel:
                idx = sel[0]
                self.remove_task(idx)
                listbox.delete(idx)
        del_btn = tk.Button(popup, text="Hapus", command=del_task_popup, bg="#e84118", fg="white", font=("Segoe UI", 10))
        del_btn.pack(side=tk.LEFT, padx=5, pady=5)
