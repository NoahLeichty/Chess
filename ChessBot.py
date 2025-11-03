#will be logic for a chess bot to make moves
import ChessEngine
import my_module

class ChessBot:
    def __init__(self, gameState):
        self.gameState = gameState

    def randomMove(self, validMoves):
        from random import choice
        if len(validMoves) != 0:
            return choice(validMoves)
    
    def pieceValue(self, piece):
        values = {"wP": 1, "wN": 3, "wB": 3, "wR": 5, "wQ": 9, "wK": 0,
                  "bP": -1, "bN": -3, "bB": -3, "bR": -5, "bQ": -9, "bK": 0, "--": 0}
        return values.get(piece, 0)
    
    def evaluateBoard(self):
        evaluation = 0
        
    
    def minMax(self, node, depth, maximizingPlayer):
        if depth == 0:
            return node
    

        