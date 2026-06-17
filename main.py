import tkinter as tk
from cat_engine import CatEngine

root = tk.Tk()

root.overrideredirect(True)
root.attributes("-topmost", True)

root.config(bg="green")

try:
    root.wm_attributes(
        "-transparentcolor",
        "green"
    )
except:
    pass

CatEngine(root)

root.mainloop()