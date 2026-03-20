#will be logic for a chess bot to make moves
import ChessEngine
import random
pieceValue = {"K": 0, "P": 1, "N":3, "B":3, "R":5, "Q":9}
checkmate = 10000
stalemate = 0

class ChessBot:
    def __init__(self, gameState):
        self.gameState = gameState
        self.piecePositionScores = {"N":self.knightEvaluation(), "wP": self.WhitePawnEvaluation(),"bP":self.blackPawnEvaluation(),"B":self.bishopEvalutation(),
                                    "R":self.rookEvalutation(),"Q":self.queenEvalutation(), "K":self.kingEvalutation()}

    def randomMove(self, validMoves):
        from random import choice
        if len(validMoves) != 0:
            return choice(validMoves)
    
    def WhitePawnEvaluation(self):
        return [[8,8,8,8,8,8,8,8],
                [7,7,7,7,7,7,7,7],
                [6,6,6,6,6,6,6,6],
                [4,2,3,7,7,3,2,4],
                [4,2,3,7,7,3,2,4],
                [3,2,0,2,2,0,2,3],
                [1,1,1,0,0,1,1,1],
                [0,0,0,0,0,0,0,0]]
    
    def blackPawnEvaluation(self):
        return [[0,0,0,0,0,0,0,0],
                [1,1,1,0,0,1,1,1],
                [3,2,0,2,2,0,2,2],
                [4,2,3,7,7,3,2,2],
                [4,2,3,7,7,3,2,2],
                [6,6,6,6,6,6,6,6],
                [7,7,7,7,7,7,7,7],
                [8,8,8,8,8,8,8,8]]
    
    def knightEvaluation(self):
        return [[1,1,1,1,1,1,1,1],
                [1,2,2,2,2,2,2,1],
                [1,2,3,3,3,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [1,2,3,3,3,3,3,1],
                [1,2,2,2,2,2,2,1],
                [1,1,1,1,1,1,1,1]]
    
    def bishopEvalutation(self):
        return [[4,3,2,1,1,2,3,4],
                [3,4,2,2,2,2,4,3],
                [2,3,4,3,3,4,3,2],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [2,3,4,3,3,4,3,2],
                [3,4,3,2,2,3,4,3],
                [4,3,2,1,1,2,3,4]]
    
    def rookEvalutation(self):
        return [[4,3,4,4,4,4,3,4],
                [4,4,4,4,4,4,4,4],
                [3,3,3,3,3,3,3,3],
                [1,2,3,4,4,3,2,1],
                [1,2,3,4,4,3,2,1],
                [3,3,3,3,3,3,3,3],
                [4,4,4,4,4,4,4,4],
                [4,3,4,4,4,4,3,4]]
    
    def kingEvalutation(self):
        return [[1,3,4,1,1,3,4,3],
                [2,2,2,1,1,2,2,2],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [2,2,2,2,2,2,2,2],
                [3,4,4,1,1,1,4,3]]
    
    def queenEvalutation(self):
        return [[1,1,1,3,1,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,2,2,1,1,1],
                [1,1,3,3,3,3,1,1],
                [1,1,3,3,3,2,1,1],
                [1,1,2,2,2,1,1,1],
                [1,1,1,1,1,1,1,1],
                [1,1,1,3,1,1,1,1]]

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

        if self.gameState.moveLog:
            lastMove = self.gameState.moveLog[-1]
            pass

        evaluation = self.simpleBoardEvaluation()
        return evaluation + (mobility * 0.1) + (CenterControl) + (KingSafety) + (PawnStructure * 0.03) + (pieceActivity) + totalEvaluation
    
    # A simpler board evaluation function that focuses solely on material count
    def simpleBoardEvaluation(self):
        board = self.gameState.board
        pieceEvaluation = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                square = board[row][col]
                if square != "--":
                    #score it positionally
                    piecePositionScore = 0
                    if square[1] != "P":
                        piece = square[1]
                    else:
                        piece = square
                    piecePositionScore = self.piecePositionScores[piece][row][col]
                if square[0] == "w":
                    pieceEvaluation += pieceValue[square[1]] + piecePositionScore * 0.1
                if square[0] == "b":
                    pieceEvaluation -= pieceValue[square[1]] + piecePositionScore * 0.1
        return pieceEvaluation
        
    def minMax(self, gs, depth, whiteToMove):
        if depth == 0:
            return self.evaluateBoard(gs)
        bestMove = None
        
        if whiteToMove:
            maxScore = -checkmate
            for move in gs.getValidMoves():
                gs.makeMove(move)
                score = self.minMax(gs, depth -1, not whiteToMove)
                gs.undoMove()
                if score > maxScore:
                    maxScore = score
            return maxScore
        else:
            minScore = checkmate
            for move in gs.getValidMoves():
                gs.makeMove(move)
                score = self.minMax(gs, depth-1, whiteToMove)
                gs.undoMove()
                if score < minScore:
                    minScore = score
            return minScore
    
    # Minimax algorithm with negamax simplification
    def negaMax(self, gs, depth, color):
        if depth == 0:    
            return  color * self.evaluateBoard(gs)
        maxEval = -checkmate
        for move in gs.getValidMoves():
            gs.makeMove(move)
            eval = -self.negaMax(gs, depth - 1, -color)
            gs.undoMove()
            if eval > maxEval:
                maxEval = eval
        return maxEval
    
    # Alpha-Beta pruning implementation
    def alphaBeta(self, gs, alpha, beta, depth):
        if depth == 0:
            return self.simpleBoardEvaluation()
        maxEval = -float('inf')
        validMoves = gs.getValidMoves().random.shuffle
        if gs.stalemate:
            return stalemate
        for move in validMoves:
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
    
    def negaMaxAlphaBeta(self, gs, depth, alpha, beta, color):
        if depth == 0:    
            return  color * self.evaluateBoard(gs)
        maxEval = -checkmate
        #impliment move ordering later
        for move in gs.getValidMoves():
            gs.makeMove(move)
            # if move.pieceCaptured != "--": potential for move ordering
            eval = -self.negaMaxAlphaBeta(gs, depth - 1, -beta, -alpha, -color)
            gs.undoMove()
            if eval > maxEval:
                maxEval = eval
            if maxEval > alpha:
                alpha = maxEval
            if alpha >= beta:
                break
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
            eval = -self.negaMaxAlphaBeta(gs, depth -1, -checkmate, checkmate, 1 if gs.whiteToMove else -1)
            gs.undoMove()
            if eval > maxEval:
                maxEval = eval
                bestMove = move
        return bestMove