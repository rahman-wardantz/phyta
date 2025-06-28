class TodoManager:
    def __init__(self, todo_list=None):
        self.todo_list = todo_list if todo_list is not None else []

    def add_task(self, task):
        if task:
            self.todo_list.append(task)
            return True, f"Tugas '{task}' berhasil ditambahkan ke daftar."
        return False, "Mohon masukkan deskripsi tugas setelah '+ '"

    def remove_task(self, param):
        if param.isdigit():
            idx = int(param) - 1
            if 0 <= idx < len(self.todo_list):
                removed = self.todo_list.pop(idx)
                return True, f"Tugas '{removed}' berhasil dihapus dari daftar."
            else:
                return False, "Nomor tugas tidak valid."
        else:
            for i, t in enumerate(self.todo_list):
                if param.lower() in t.lower():
                    removed = self.todo_list.pop(i)
                    return True, f"Tugas '{removed}' berhasil dihapus dari daftar."
            return False, "Tugas tidak ditemukan di daftar."

    def list_tasks(self):
        if not self.todo_list:
            return False, "Daftar tugas kosong."
        daftar = '\n'.join([f"{i+1}. {t}" for i, t in enumerate(self.todo_list)])
        return True, f"Daftar tugas saat ini:\n{daftar}"

    def get_list(self):
        return self.todo_list

    def set_list(self, new_list):
        self.todo_list = new_list
