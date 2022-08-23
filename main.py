"""
Entry of this project.
"""
import tkinter as tk
from core.gui import MainApp

root = tk.Tk()
app = MainApp(root)
root.attributes("-alpha", 0.8)
root.mainloop()
