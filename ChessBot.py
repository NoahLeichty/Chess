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
        pawnEvalutaion = [[2, 2, 2, 2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2, 2, 2],
                          [1.75, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.75],
                          [1.5, 1.25, 1.75, 1.75, 1, 1, 1.25, 1.5],
                          [1.25, 1, 1, 1.5, 1.5, 1, 1, 1.25],
                          [1.25, 1.1, 1.1, 0.95, 0.95, 1.1, 1.1, 1.25],
                          [.95, .95, .95, .95, .95, .95, .95, .95],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          ]
        return pawnEvalutaion

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

        if ChessEngine.GameState().whiteToMove:
            sideToMove = 1
        else:
            sideToMove = -1

        Eval  = (materialScore + mobilityScore) * sideToMove

        # Another way to do board evaluation
        pieceEvaluation = 0
        totalEvaluation = 0
        mobility = len(self.gameState.getValidMoves())
        KingSafety = 0
        CenterControl = 0
        
        if board[3][3] in ['bN','bB','bR','bQ'] or board[3][4] in ['bN','bB','bR','bQ'] or board[4][3] in ['bN','bB','bR','bQ'] or board[4][4] in ['bN','bB','bR','bQ']:
            CenterControl += 3
        if board[3][3] in ['bP'] or board[3][4] in ['bP'] or board[4][3] in ['bP'] or board[4][4] in ['bP']:
            CenterControl += 100
        if board[0][6] == 'bK' or board[0][3] == 'bk':
            KingSafety += 10
        PawnStructure = 0
        pieceActivity = 0
        evaluation = self.simpleBoardEvaluation()
        return evaluation + (mobility * 0.1) + (CenterControl) + (KingSafety) + (PawnStructure * 0.03) + (pieceActivity * 0.02)
    
    # A simpler board evaluation function that focuses solely on material count
    def simpleBoardEvaluation(self):
        board = self.gameState.board
        pieceEvaluation = 0
        for row in board:
            for square in row:
                if square == 'wP':
                    pieceEvaluation += 1
                elif square == 'bP':
                    pieceEvaluation -= 1
                elif square == 'wN':
                    pieceEvaluation += 3
                elif square == 'bN':
                    pieceEvaluation -= 3
                elif square == 'wB':
                    pieceEvaluation += 3
                elif square == 'bB':
                    pieceEvaluation -= 3
                elif square == 'wR':
                    pieceEvaluation += 5
                elif square == 'bR':
                    pieceEvaluation -= 5
                elif square == 'wQ':
                    pieceEvaluation += 9
                elif square == 'bQ':
                    pieceEvaluation -= 9
                elif square == 'wK':
                    pieceEvaluation += 1000
                elif square == 'bK':
                    pieceEvaluation -= 1000
        return pieceEvaluation
        
    def minMax(self, node, depth, maximizingPlayer):
        if depth == 0:
            return node
    
    # Minimax algorithm with negamax simplification
    def negaMax(self, depth,color):
        if depth == 0:    
            return  color * self.evaluateBoard()
        maxEval = -float('inf')
        for move in self.gameState.getValidMoves():
            self.gameState.makeMove(move)
            eval = -self.negaMax(depth - 1,-color)
            self.gameState.undoMove()
            if eval > maxEval:
                maxEval = eval
        return maxEval
    
    # Alpha-Beta pruning implementation
    def alphaBeta(self, alpha, beta, depth):
        if depth == 0:
            return self.evaluateBoard()
        maxEval = -float('inf')
        if self.gameState.checkmate:
            return -float('inf')
        for move in self.gameState.getValidMoves():
            self.gameState.makeMove(move)
            eval = -self.alphaBeta(-beta, -alpha, depth - 1)
            self.gameState.undoMove()
            if eval > maxEval:
                maxEval = eval
                if eval > alpha:
                    alpha = eval
            if eval >= beta:
                return beta
        return maxEval
    
    # Quiescence Search that extends the search for "quiet" positions
    def quiescenceSearch(self, alpha, beta, depth, color,):
        stand_pat = color * self.evaluateBoard()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat
        for move in self.gameState.getValidMoves():
            if move.pieceCaptured != '--':  # Only consider captures
                self.gameState.makeMove(move)
                score = -self.quiescenceSearch(-beta, -alpha, depth -1, -color)
                self.gameState.undoMove()
                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score
        return alpha
    
    def moveOrdering(self):
        # Simple move ordering based on captures
        moveScore = 0
        for move in self.gameState.getValidMoves():
           if move.pieceCaptured != '--':
               moveScore += 10  # Prioritize captures
        return moveScore
        
    # Choose the best move using negamax
    def makeBestMove(self, validMoves, depth):
        bestMove = None
        maxEval = -float('inf')
        for move in validMoves:
            self.gameState.makeMove(move)
            eval = -self.alphaBeta(-float('inf'), float('inf'), depth - 1)
            self.gameState.undoMove()
            if eval > maxEval:
                maxEval = eval
                bestMove = move
        return bestMove