#will be logic for a chess bot to make moves
import ChessEngine

class ChessBot:
    def __init__(self, gameState):
        self.game_state = gameState

    def randomMove(self, validMoves):
        import random
        if len(validMoves) != 0:
            return random.choice(validMoves)
        