import pygame
pygame.init()
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Chess Board")

square_size = screen_width // 8
colors = [(255, 255, 255), (0, 0, 139)] # White and a dark grey

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

# Initial board setup (simplified example)
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
    # This is where your chess move validation logic goes
    # For this simple example, we'll just allow any move for demonstration
    return True

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
                if board[row][col] != '--': # Assuming '--' means empty
                    selected_square = (row, col)
            else:
                # Second click: move the selected piece
                start_row, start_col = selected_square
                end_row, end_col = row, col

                if is_valid_move((start_row, start_col), (end_row, end_col), board):
                        # Perform the move
                        board[end_row][end_col] = board[start_row][start_col]
                        board[start_row][start_col] = '--'
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