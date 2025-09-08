import pygame
pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Board")

square_size = screen_width // 8
colors = [(255, 255, 255), (0, 0, 139)] # White and a dark blue

# Load piece images
piece_images = {
    "wP": pygame.image.load("Assets/wp.png"),
    "wR": pygame.image.load("Assets/wr.png"),
    "wN": pygame.image.load("Assets/wn.png"),
    "wB": pygame.image.load("Assets/wb.png"),
    "wQ": pygame.image.load("Assets/wq.png"),
    "wK": pygame.image.load("Assets/wk.png"),
    "bP": pygame.image.load("Assets/bp.png"),
    "bR": pygame.image.load("Assets/br.png"),
    "bN": pygame.image.load("Assets/bn.png"),
    "bB": pygame.image.load("Assets/bb.png"),
    "bQ": pygame.image.load("Assets/bq.png"),
    "bK": pygame.image.load("Assets/bk.png"),
}

# Scale images to fit squares
for piece_type, image in piece_images.items():
    piece_images[piece_type] = pygame.transform.scale(image, (square_size, square_size))

# Initial board setup
board = [
    ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
    ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None],
    ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
    ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
]

selected_square = None # Stores (row, col) of selected piece

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Chess")

def is_valid_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]
    target = board[end_row][end_col]
    current_piece = board[start_row][start_col]

    # Basic validation: ensure the piece exists and the move is within bounds
    if not (0 <= start_row < 8 and 0 <= start_col < 8 and 0 <= end_row < 8 and 0 <= end_col < 8):
        return False
    
    if piece is None:
        return False
    
    global white_turn
    white_turn = True


    # Only white can move
    if white_turn == True and piece.startswith('b'):
        return False
    elif white_turn == False and piece.startswith('w'):
        return False

    # White pawn movement
    if piece == 'wP':
        if start_col == end_col and target is None:
            if start_row - end_row == 1:
                return True
            if start_row == 6 and start_row - end_row == 2 and board[start_row - 1][start_col] is None:
                return True
        elif abs(start_col - end_col) == 1 and start_row - end_row == 1 and target is not None and target.startswith('b'):
            return True
        elif abs(start_col - end_col) == 1 and start_row - end_row == 1 and target is None:
            # En passant (simplified)
            if start_row == 3 and board[start_row][end_col] == 'bP':
                return True
        return False
    # Black pawn movement
    elif piece == 'bP':
        if start_col == end_col and target is None:
            if end_row - start_row == 1:
                return True
            if start_row == 1 and end_row - start_row == 2 and board[start_row + 1][start_col] is None:
                return True
        elif abs(start_col - end_col) == 1 and end_row - start_row == 1 and target is not None and target.startswith('w'):
            return True 
        elif abs(start_col - end_col) == 1 and end_row - start_row == 1 and target is None:
            # En passant (simplified)
            if start_row == 4 and board[start_row][end_col] == 'wP':
                return True
        return False
    # Rook movement
    elif piece in ['wR', 'bR']:
        if start_row != end_row and start_col != end_col:
            return False
        step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        r, c = start_row + step_row, start_col + step_col
        while (r, c) != (end_row, end_col):
            if board[r][c] is not None:
                return False
            r += step_row
            c += step_col
        if target is None or (piece.startswith('w') and target.startswith('b')) or (piece.startswith('b') and target.startswith('w')):
            return True
        return False
    # Knight movement
    elif piece in ['wN', 'bN']:
        if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
            if target is None or (piece.startswith('w') and target.startswith('b')) or (piece.startswith('b') and target.startswith('w')):
                return True
        return False
    elif piece in ['wB', 'bB']:
        if abs(start_row - end_row) != abs(start_col - end_col):
            return False
        step_row = 1 if end_row > start_row else -1
        step_col = 1 if end_col > start_col else -1
        r, c = start_row + step_row, start_col + step_col
        while (r, c) != (end_row, end_col):
            if board[r][c] is not None:
                return False
            r += step_row
            c += step_col
        if target is None or (piece.startswith('w') and target.startswith('b')) or (piece.startswith('b') and target.startswith('w')):
            return True
        return False
    # Queen movement
    elif piece in ['wQ', 'bQ']:
        if start_row == end_row or start_col == end_col:
            step_row = 0 if start_row == end_row else (1 if end_row > start_row else -1)
            step_col = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        elif abs(start_row - end_row) == abs(start_col - end_col):
            step_row = 1 if end_row > start_row else -1
            step_col = 1 if end_col > start_col else -1
        else:
            return False
        r, c = start_row + step_row, start_col + step_col
        while (r, c) != (end_row, end_col):
            if board[r][c] is not None:
                return False
            r += step_row
            c += step_col
        if target is None or (piece.startswith('w') and target.startswith('b')) or (piece.startswith('b') and target.startswith('w')):
            return True
        return False
    # King movement
    elif piece in ['wK', 'bK']:
        if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
            if target is None or (piece.startswith('w') and target.startswith('b')) or (piece.startswith('b') and target.startswith('w')):
                return True
        return False
    else:
        False

    if piece is None:
        return False
    return True

def make_move(start_pos, end_pos, board):
    start_row, start_col = start_pos
    end_row, end_col = end_pos
    piece = board[start_row][start_col]
    board[end_row][end_col] = piece
    board[start_row][start_col] = None

# Game loop flag
running = True

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user clicks the close button
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // square_size
            row = y // square_size
            print(f"Clicked on row: {row}, col: {col}")

            if selected_square is None:
                # First click: select a piece
                if board[row][col] != None:
                    selected_square = (row, col)
            else:
                # Second click: move the selected piece
                start_row, start_col = selected_square
                end_row, end_col = row, col
                print(f"Moving from {selected_square} to {(end_row, end_col)}")
                
                
                if is_valid_move((start_row, start_col), (end_row, end_col), board):
                    make_move((start_row, start_col), (end_row, end_col), board)
                    selected_square = None # Deselect

                    # Pawn promotion to queen
                    if board[end_row][end_col] == 'wP' and end_row == 0:
                        board[end_row][end_col] = 'wQ'

                    if board[end_row][end_col] == 'bP' and end_row == 7:
                        board[end_row][end_col] = 'bQ'
                    
                    # Castling (simplified, no checks for check conditions)
                    if board[end_row][end_col] == 'wK' and start_row == 7 and start_col == 4:
                        if board[end_row] == 7 and board[end_col] == 6:
                            board[7][5] = 'wR'
                            board[7][6] = 'wK'
                            board[7][7] = None
                        elif end_row == 7 and end_col == 2:
                            board[7][3] = 'wR'
                            board[7][0] = None
                    if board[end_row][end_col] == 'bK' and start_row == 0 and start_col == 4:
                        if end_row == 0 and end_col == 6:
                            board[0][5] = 'bR'
                            board[0][7] = None
                        elif end_row == 0 and end_col == 2:
                            board[0][3] = 'bR'
                            board[0][0] = None

                else:
                    print("Invalid move")
                    selected_square = None # Deselect

    for row in range(8):
        for col in range(8):
            color_index = (row + col) % 2
            color = colors[color_index]
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))

            # Drawing the pieces
            piece = board[row][col]
            if piece:
                screen.blit(piece_images[piece], (col * square_size, row * square_size))
                pygame.display.flip()

# Quit Pygame
pygame.quit()