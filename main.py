# main.py
import tkinter as tk
from database import init_db
from gui import WashingGUI

if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = WashingGUI(root)
    root.mainloop()
