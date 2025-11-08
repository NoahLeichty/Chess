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
    
    def pawnEvaluation(self):
        pass
    def evaluateBoard(self):
        #simple evaluation function that counts material
        board = self.gameState.board
        
        # One way to do board evaluation
        kingWt = 1000
        queenWt = 9
        rookWt = 5
        knightWt = 3
        bishopWt = 3
        pawnWt = 1
        mobilityWt = 0.1
        
        wK = wQ = wR = wN = wB = wP = 0
        bK = bQ = bR = bN = bB = bP = 0
        wMobility = bMobility = 0
        materialScore = kingWt  * (wK-bK) + queenWt * (wQ-bQ) + rookWt  * (wR-bR) + knightWt* (wN-bN) + bishopWt* (wB-bB) + pawnWt  * (wP-bP)

        mobilityScore = mobilityWt * (wMobility-bMobility)

        if self.gameState.whiteToMove:
            sideToMove = 1
        else:
            sideToMove = -1

        Eval  = (materialScore + mobilityScore) * sideToMove

        # Another way to do board evaluation
        evaluation = 0
        material = 0
        mobility = len(ChessEngine.GameState().getValidMoves())
        KingSafety = 0 
        CenterControl = 0
        PawnStructure = 0
        pieceActivity = 0
        pieceValues = {
            'wP': 1, 'wN': 3, 'wB': 3, 'wR': 5, 'wQ': 9, 'wK': 100,
            'bP': -1, 'bN': -3, 'bB': -3, 'bR': -5, 'bQ': -9, 'bK':100
        }
        for i in range (len(pieceValues)):
            material += pieceValues[i]
        evaluation = material
        return evaluation
    
    # A simpler board evaluation function that focuses solely on material count
    def simpleBoardEvaluation(self):
        board = self.gameState.board
        pieceValues = {
            'wP': 1, 'wN': 3, 'wB': 3, 'wR': 5, 'wQ': 9, 'wK': 100,
            'bP': -1, 'bN': -3, 'bB': -3, 'bR': -5, 'bQ': -9, 'bK':100
        }
        evaluation = 0
        for row in board:
            for piece in row:
                if piece in pieceValues:
                    evaluation += pieceValues[piece]
        return evaluation
        
    
    def minMax(self, node, depth, maximizingPlayer):
        if depth == 0:
            return node
    
    def negaMax(self, depth):
        if depth == 0:
            return self.simpleBoardEvaluation()
        maxEval = -float('inf')
        for move in ChessEngine.GameState().getValidMoves():
            ChessEngine.GameState().makeMove(move)
            eval = -self.negaMax(depth - 1)
            if eval > maxEval:
                maxEval = eval
            ChessEngine.GameState().undoMove()
        return maxEval
    
    def alphaBeta(self, alpha, beta, depth):
        if depth == 0:
            return self.simpleBoardEvaluation()
        maxEval = -float('inf')
        for move in ChessEngine.GameState().getValidMoves():
            ChessEngine.GameState()(move)
            eval = -self.alphaBeta(-beta, -alpha, depth - 1)
            ChessEngine.GameState().undoMove()
            if eval > maxEval:
                maxEval = eval
            if maxEval > alpha:
                alpha = maxEval
            if beta <= alpha:
                return maxEval
        return maxEval

    def makeBestMove(self, validMoves, depth):
        bestMove = None
        maxEval = -float('inf')
        for move in validMoves:
            ChessEngine.GameState().makeMove(move)
            eval = -self.negaMax(depth - 1)
            ChessEngine.GameState().undoMove()
            if eval > maxEval:
                maxEval = eval
                bestMove = move
        return bestMove