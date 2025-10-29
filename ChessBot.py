#will be logic for a chess bot to make moves
import ChessEngine

class ChessBot:
    def __init__(self, gameState):
        self.game_state = gameState

    def randomMove(self, validMoves):
        from random import choice
        if len(validMoves) != 0:
            return choice(validMoves)
        
    def pieceValue(self, piece):
        values = {"wP": 1, "wN": 3, "wB": 3, "wR": 5, "wQ": 9,
                  "bP": -1, "bN": -3, "bB": -3, "bR": -5, "bQ": -9}
        return values.get(piece, 0)
    
    

        