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

# Load chess pieces images
# Dictonary to hold piece images
pieces = {}
def load_pieces():
    # Array of piece names
    piece_names = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
    for piece in piece_names:
        # Load each piece image from Assets folder
        # and store it in the pieces dictionary
        pieces[piece] = ImageTk.PhotoImage(Image.open(os.path.join("Assets", f"{piece}.png")))
load_pieces()

# Place pieces on the board
def place_pieces():
    # Places white pawns
    for j in range(8):
        pawn = tk.Label(root, image=pieces["wp"])
        pawn.grid(row=6, column=j)
    
    # Places black pawns
    for j in range(8):
        pawn = tk.Label(root, image=pieces["bp"])
        pawn.grid(row=1, column=j)

    # Place white pieces on the first row
    piece_order = ["wr", "wn", "wb", "wq", "wk", "wb", "wk", "wr"]
    for j, piece in enumerate(piece_order):
        piece_label = tk.Label(root, image=pieces[piece])
        piece_label.grid(row=7, column=j)
    
    # Place black pieces on the last row
    piece_order = ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"]
    for j, piece in enumerate(piece_order):
        piece_label = tk.Label(root, image=pieces[piece])
        piece_label.grid(row=0, column=j)
place_pieces()

# Function to handle piece movement
def move_piece(event):
    # Get the clicked square's row and column
    row = event.widget.grid_info()['row']
    column = event.widget.grid_info()['column']

    # Print the clicked square's position
    print(f"Clicked square: ({row}, {column})")
    
    # Check if a piece is clicked
    piece = root.grid_slaves(row=row, column=column)
    
    if piece:
        piece = piece[0]
        piece.grid(row=row+1, column=column) 

# Bind the click event to move_piece function
root.bind("<Button-1>", move_piece)

# Start the main loop
root.mainloop()