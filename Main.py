"""
Main entry point for Pytha Bot GUI application.
"""

import tkinter as tk
from chatbot_gui import ChatBotGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatBotGUI(root)
    root.mainloop()