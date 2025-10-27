#will be logic for a chess bot to make moves
import ChessEngine

class ChessBot:
    def __init__(self, game_state):
        self.game_state = game_state

    def randomMove(self, valid_moves):
        import random
        return random.choice(valid_moves)