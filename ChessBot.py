#will be logic for a chess bot to make moves
import ChessEngine
pieceValue = {"K": 0, "P": 1, "N":3, "B":3, "R":5, "Q":9,"--":0}
checkmate = 10000
stalemate = 0

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

    def evaluateBoard(self, gs):
        # An advanced board evaluation function considering multiple factors
        board = self.gameState.board

        if gs.checkmate:
            if gs.whiteToMove:
                return -checkmate
            else:
                return checkmate
        if gs.stalemate:
            return stalemate
        
        pieceEvaluation = 0
        totalEvaluation = 0
        mobility = len(self.gameState.getValidMoves())
        KingSafety = 0
        CenterControl = 0
        PawnStructure = 0
        pieceActivity = 0
        
        #Early game
        if len(self.gameState.moveLog) <= 15:
            pass
        #mid game
        elif len(self.gameState.moveLog) > 15 and len(self.gameState.moveLog) < 30:
            pass
        #End game
        else:
            pass


        #if board[3][3] in ['bN','bB','bR','bQ'] or board[3][4] in ['bN','bB','bR','bQ'] or board[4][3] in ['bN','bB','bR','bQ'] or board[4][4] in ['bN','bB','bR','bQ']:
            #CenterControl += -0.1
        if board[3][3] in ['bP'] or board[3][4] in ['bP'] or board[4][3] in ['bP'] or board[4][4] in ['bP']:
            CenterControl += -2
        if board[2][2] in ['bN']:
            pieceActivity += -0.1
        if board[2][5] in ['bN']:
            pieceActivity += -0.1
        if board[0][6] == 'bK' or board[0][3] == 'bk':
            KingSafety += -5
        if board[2][5] in ['bQ']:
            pieceActivity += 10

        if self.gameState.moveLog:
            lastMove = self.gameState.moveLog[-1]
            pass

        evaluation = self.simpleBoardEvaluation()
        return evaluation + (mobility * 0.1) + (CenterControl) + (KingSafety) + (PawnStructure * 0.03) + (pieceActivity) + totalEvaluation
    
    # A simpler board evaluation function that focuses solely on material count
    def simpleBoardEvaluation(self):
        board = self.gameState.board
        pieceEvaluation = 0
        for row in board:
            for square in row:
                if square[0] == "w":
                    pieceEvaluation += pieceValue[square[1]]
                if square[0] == "b":
                    pieceEvaluation -= pieceValue[square[1]]
        return pieceEvaluation
        
    def minMax(self, gs, validMoves, depth, whiteToMove):
        if depth == 0:
            return self.evaluateBoard(gs)
        bestMove = None
        
        if whiteToMove:
            maxScore = -checkmate
            for move in validMoves:
                gs.makeMove(move)
                nextMoves = gs.getValidMoves()
                score = self.minMax(gs,nextMoves, depth -1, not whiteToMove)
                gs.undoMove()
                if score > maxScore:
                    maxScore = score
            return maxScore
        else:
            minScore = checkmate
            for move in validMoves:
                gs.makeMove(move)
                nextMoves = gs.getValidMoves()
                score = self.minMax(gs,nextMoves, depth-1, whiteToMove)
                gs.undoMove()
                if score < minScore:
                    minScore = score
            return minScore
    
    # Minimax algorithm with negamax simplification
    def negaMax(self, gs, depth, color):
        if depth == 0:    
            return  color * self.evaluateBoard(gs)
        maxEval = -float('inf')
        for move in self.gameState.getValidMoves():
            self.gameState.makeMove(move)
            eval = -self.negaMax(gs, depth - 1,-color)
            self.gameState.undoMove()
            if eval > maxEval:
                maxEval = eval
        return maxEval
    
    # Alpha-Beta pruning implementation
    def alphaBeta(self, gs, alpha, beta, depth):
        if depth == 0:
            return self.evaluateBoard(gs)
        maxEval = -float('inf')
        if gs.checkmate:
            return -float('inf')
        for move in gs.getValidMoves():
            gs.makeMove(move)
            eval = -self.alphaBeta(gs, -beta, -alpha, depth - 1)
            gs.undoMove()
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
        
    # Choose the best move
    def makeBestMove(self, gs, validMoves, depth):
        bestMove = None
        maxEval = -float('inf')
        for move in validMoves:
            gs.makeMove(move)
            eval = -self.minMax(gs,validMoves,depth -1, True)
            gs.undoMove()
            if eval > maxEval:
                maxEval = eval
                bestMove = move
        return bestMove