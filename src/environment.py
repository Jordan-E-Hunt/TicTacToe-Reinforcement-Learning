import numpy as np

class TicTacToe:
  def __init__(self):
    self.size = 3 #3x3 Board
    self.board = np.zeros((self.size,self.size)) 
    self.players = ["X", "O"]
    self.current = self.players[0]
    self.winner = None
    self.game_over = False
    self.check_winner()

  def reset(self):
    self.__init__()

  def avail_moves(self):
    moves = [] #Will contain list of moves available
    for i in range(self.size):
      for j in range(self.size):
        if self.board[i][j] == 0:
          moves.append((i,j))
    return moves

  def get_state(self):
    #Add Perspective Variation (Bring Accuracy Above 75%)
    p_idx = self.players.index(self.current) + 1 #1 or 2

    #Create a copy where current is 1 and 'other' is -1
    norm_board = np.zeros((self.size,self.size))
    for i in range(self.size):
        for j in range(self.size):
            if self.board[i][j] == 0:
                norm_board[i][j] = 0
            elif self.board[i][j] == p_idx:
                norm_board[i][j] = 1  # Me
            else:
                norm_board[i][j] = -1 # Opponent
    
    canonical = self.canonical_board(norm_board)

    return tuple(norm_board.flatten())

  def make_move(self, move):
    reward = -0.1
    if self.board[move[0]][move[1]] != 0:
      return self.get_state(), -1.0, True, False

    self.board[move[0]][move[1]] = self.players.index(self.current) + 1

    self.check_winner()

    if self.game_over:
      if self.winner == self.current:  #Winner just moved
        reward = 3.0
      elif self.winner == "Draw":  #Draw
        reward = 0.5
      else: #Loss
        reward = -2.0


    self.switch_player()

    return self.get_state(), reward, self.game_over, False

  def switch_player(self):
    if self.current == self.players[0]:
      self.current = self.players[1]
    else:
      self.current = self.players[0]

  def check_winner(self):
    #Row Wins
    for i in range(self.size):
      if self.board[i][0] == self.board[i][1] ==  self.board[i][2] != 0:
        self.winner = self.players[int(self.board[i][1] - 1)]
        self.game_over = True
    #Column Wins
    for j in range(self.size):
      if self.board[0][j] == self.board[1][j] == self.board[2][j] != 0:
        self.winner = self.players[int(self.board[1][j] - 1)]
        self.game_over = True
    #Diagonal Wins
    if (self.board[0][0] == self.board[1][1] == self.board[2][2] != 0 or
        self.board[0][2] == self.board[1][1] == self.board[2][0] != 0):
      self.winner = self.players[int(self.board[1][1] - 1)]
      self.game_over = True

    #Draw
    if np.all(self.board != 0) and self.game_over == False:
      self.winner = "Draw"
      self.game_over = True

  def print_board(self):
    print("--------------")
    for i in range(self.size):
      print("|", end= " ")
      for j in range(self.size):
         print(self.players[int(self.board[i][j] - 1)]
          if self.board[i][j] != 0 else " ", end=" | ")
      print()
      print("--------------")
  
  def canonical_board(self, board):
    "Return the lex-smallest tuple among all 8 symmetries."
    candidates = []
    
    # Original
    candidates.append(tuple(board.flatten()))
    
    # Rotations
    rot90 = np.rot90(board)
    candidates.append(tuple(rot90.flatten()))
    rot180 = np.rot90(rot90)
    candidates.append(tuple(rot180.flatten()))
    rot270 = np.rot90(rot180)
    candidates.append(tuple(rot270.flatten()))
    
    if self.size > 3:# Reflections (Not Needed for 3x3 version or smaller, but for scale)
      candidates.append(tuple(np.fliplr(board).flatten()))  # Horizontal
      candidates.append(tuple(np.flipud(board).flatten()))  # Vertical
      candidates.append(tuple(np.transpose(board).flatten()))  # Main diagonal
      candidates.append(tuple(np.fliplr(np.flipud(board)).flatten()))  # Anti-diagonal
    
    return min(candidates)  # Lex smallest
