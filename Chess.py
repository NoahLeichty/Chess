# will be like chess and eventually have AI and engine
import tkinter as tk
from PIL import Image, ImageTk
import os

# opens frame for chess game
root = tk.Tk()
root.title("Chess")
root.geometry("600x600")

# Create a chessboard layout
# 8x8 grid of squares
for i in range(8):
    for j in range(8):
        if (i + j) % 2 == 0:
            color = "white"
        else:
            color = "dark blue"
        square = tk.Frame(root, width=75, height=75, bg=color)
        square.grid(row=i, column=j)

root.mainloop()