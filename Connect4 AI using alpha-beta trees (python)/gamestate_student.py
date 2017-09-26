import sys, time, random, copy
from settings import *

class GameState:

    # Initializer for the Connect4 GameState
    # Board is initialized to size width*height
    def __init__(self, rows, cols):
        self.__rows  = rows         # number of rows in the board
        self.__cols = cols          # number of columns in the board
        self.__pieces = [0]*cols    # __pieces[c] = number of pieces in a column c
        self.__player = 0           # the current player to move, 0 = Player One, 1 = Player Two
        self.__board   = [[PLAYER_NONE]*cols for r in range(rows)]

    # performs the given move, putting the piece into the appropriate column and swapping the player
    def do_move(self, move):
        if not self.is_legal(move): 
            print("DOING ILLEGAL MOVE")
            sys.exit()
        self.__board[self.pieces(move)][move] = self.player_to_move()
        self.__pieces[move] += 1
        self.__player = (self.__player + 1) % 2
    def undo_move(self,move):
        self.__board[self.pieces(move) - 1][move] = PLAYER_NONE
        self.__pieces[move] = self.pieces(move)-1
        self.__player = (self.__player + 1) % 2
    # some getter functions that you probably won't need to modify
    def get(self, r, c):        return self.__board[r][c]   # piece type located at (r,c)
    def cols(self):             return self.__cols          # number of columns in board
    def rows(self):             return self.__rows          # number of rows in board
    def pieces(self, col):      return self.__pieces[col]   # number of pieces in a given column
    def total_pieces(self):     return sum(self.__pieces)   # total pieces on the board
    def player_to_move(self):   return self.__player        # the player to move next

    # a move (placing a piece into a given column) is legal if the column isn't full
    def is_legal(self, move):   return move >= 0 and move < self.cols() and self.__pieces[move] < self.rows()

    # returns a list of legal moves at this state (which columns aren't full yet)
    def get_legal_moves(self):  return [i for i in range(self.cols()) if self.is_legal(i)]

    def eval(self, player): #modify all referances to the actual board to referance the copy for the state instead
        other_player = (player + 1) % 2
        player_4s = 0
        other_player_4s = 0
        value = 0
        winning_player = self.winner()
        if winning_player == player: 
            value = 100000 - self.total_pieces()
            return value
        if winning_player == ((player+1)%2): 
            value = -100000 + self.total_pieces()
            return value
        if winning_player == DRAW: 
            value = 0
            return value
            #row check
        for c in range(self.cols()):
            for r in range(self.rows() - 3):
                if self.get(r,c) == player:
                    if (self.get(r+1,c) == player or self.get(r+1,c) == PLAYER_NONE) and  (self.get(r+2,c) == player or self.get(r+2,c) == PLAYER_NONE) and (self.get(r+3,c) == player or self.get(r+3,c) == PLAYER_NONE):
                        player_4s += 1
                elif self.get(r,c) == other_player:
                    if (self.get(r+1,c) == other_player or self.get(r+1,c) == PLAYER_NONE) and  (self.get(r+2,c) == other_player or self.get(r+2,c) == PLAYER_NONE) and (self.get(r+3,c) == other_player or self.get(r+3,c) == PLAYER_NONE):
                        other_player_4s += 1
            #col check
        for r in range(self.rows()):
            for c in range(self.cols() - 3):
                if self.get(r,c) == player:
                    if (self.get(r,c+1) == player or self.get(r,c+1) == PLAYER_NONE) and  (self.get(r,c+2) == player or self.get(r,c+2) == PLAYER_NONE) and (self.get(r,c+3) == player or self.get(r,c+3) == PLAYER_NONE):
                        player_4s += 1
                elif self.get(r,c) == other_player:
                    if (self.get(r,c+1) == other_player or self.get(r,c+1) == PLAYER_NONE) and  (self.get(r,c+2) == other_player or self.get(r,c+2) == PLAYER_NONE) and (self.get(r,c+3) == other_player or self.get(r,c+3) == PLAYER_NONE):
                        other_player_4s += 1
            #diag right
        for c in range(self.cols() - 3):
            for r in range(self.rows() - 3):
                if self.get(r,c) == player:
                    if (self.get(r+1,c+1) == player or self.get(r+1,c+1) == PLAYER_NONE) and  (self.get(r+2,c+2) == player or self.get(r+2,c+2) == PLAYER_NONE) and (self.get(r+3,c+3) == player or self.get(r+3,c+3) == PLAYER_NONE):
                        player_4s += 1
                elif self.get(r,c) == other_player:
                    if (self.get(r+1,c+1) == other_player or self.get(r+1,c+1) == PLAYER_NONE) and  (self.get(r+2,c+2) == other_player or self.get(r+2,c+2) == PLAYER_NONE) and (self.get(r+3,c+3) == other_player or self.get(r+3,c+3) == PLAYER_NONE):
                        other_player_4s += 1

          #diag left
        for c in range(3,self.cols()):
            for r in range(self.rows() - 3):
                if self.get(r,c) == player:
                    if (self.get(r+1,c-1) == player or self.get(r+1,c-1) == PLAYER_NONE) and  (self.get(r+2,c-2) == player or self.get(r+2,c-2) == PLAYER_NONE) and (self.get(r+3,c-3) == player or self.get(r+3,c-3) == PLAYER_NONE):
                        player_4s += 1
                elif self.get(r,c) == other_player:
                    if (self.get(r+1,c-1) == other_player or self.get(r+1,c-1) == PLAYER_NONE) and  (self.get(r+2,c-2) == other_player or self.get(r+2,c-2) == PLAYER_NONE) and (self.get(r+3,c-3) == other_player or self.get(r+3,c-3) == PLAYER_NONE):
                        other_player_4s += 1
        value = player_4s * 100 - other_player_4s*100
        return value

    def winner(self):
        
        # col check
        for r in range(self.rows()):
            for c in range(self.cols() - 3):
                player = self.get(r,c)
                if player == PLAYER_NONE: continue
                if self.get(r,c+1) == player and self.get(r,c+2) == player and self.get(r,c+3) == player:
                    return player
                # row check
        for c in range(self.cols()):
            for r in range(self.rows() - 3):
                player = self.get(r,c)
                if player == PLAYER_NONE: continue
                if self.get(r+1,c) == player and self.get(r+2,c) == player and self.get(r+3,c) == player:
                    return player
        #Check diagonal right
        for c in range(self.cols()-3):
            for r in range(self.rows()-3):
                match = self.get(r,c)
                if match == 2:
                    continue
                elif match != player:
                    player = match
                if self.__board[r][c]== match and self.__board[r+1][c+1]== match and self.__board[r+2][c+2]== match and self.__board[r+3][c+3]==match:
                    return player
        #Check diagonal left
        for c in range(3,self.cols()):
            for r in range(self.rows()-3):
                match = self.get(r,c)
                if match == 2: 
                    continue
                elif match != player:
                    player = match
                if self.__board[r][c]== match and self.__board[r+1][c-1]== match and self.__board[r+2][c-2]== match and self.__board[r+3][c-3]== match:
                      return player
        #Draw condition
        if self.total_pieces() == self.cols() * self.rows():
            return DRAW
       
        return PLAYER_NONE

# Student TODO: Implement this class
class Player_AlphaBeta:
    def __init__(self, max_depth, time_limit):
        self.max_depth = max_depth      # set the max depth of search
        self.max_d = 0
        self.time_limit = time_limit    # set the time limit (in milliseconds)
        self.time_elapsed_ms = 0
        self.reset()
        

    def reset(self):
        self.temp_bestmove = -1
        self.best_move = -1
        self.best_move_val = -100000
        self.val = []

    def get_move(self, state1):
        
        state = copy.deepcopy(state1)
        # store the time that we started calculating this move, so we can tell how much time has passed
        self.time_start = time.clock()
        # store the player that we're deciding a move for and set it as a class variable
        self.player = state.player_to_move()
        #AB_value = self.alpha_beta(state,0, -100000000, 100000000, True)
        self.ID_AB(state)
        return self.best_move

    def alpha_beta(self, state, depth, alpha, beta, max_player):
        self.time_elapsed_ms = (time.clock() - self.time_start)*1000
        if self.terminal(state,depth):
            return state.eval(self.player)
        if self.time_limit > 0 and self.time_elapsed_ms > self.time_limit:raise Timeout()
        for move in state.get_legal_moves():        
            state.do_move(move)
            value = self.alpha_beta(state,depth+1,alpha,beta,not max_player)
            if (depth == 0):self.val.append(value)
            state.undo_move(move)
            if(max_player and value > alpha):
                if(depth == 0):
                    self.temp_best_move = move
                alpha = value
            elif not max_player and (value < beta) :
                beta = value
            if(alpha >= beta): break
        if max_player: return alpha
        else: return beta

    def terminal(self,state,depth):
        if self.max_depth >0 and depth >= self.max_depth: return True
        return state.winner() != PLAYER_NONE

    def ID_AB(self, state):
        if self.max_depth > 0: max_d = self.max_depth
        else: max_d=100
        depth = 0
        alpha = -1000000
        beta = 1000000
        max_player = True
        for d in range(1, max_d+1):
            try:
                self.max_depth = d
                self.best_move_val = self.alpha_beta(state,depth,alpha,beta,max_player)
                self.best_move = self.temp_best_move
            except Timeout as err: 
                break
        return self.best_move

    

class Timeout(Exception):
    def __init__(self):
        Exception.__init__(self,"Time out")
