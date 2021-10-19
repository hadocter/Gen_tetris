import numpy as np
class t_env:

  def __init__ (self):
    self.board = np.zeros((20,10))
    self.is_dead = 0

    #define tetrominos
    self.t_o = np.array([[1,1],[1,1]])
    self.t_t = np.array([[1,1,1],[0,1,0]])
    self.t_l = np.array([[1,0],[1,0],[1,1]])
    self.t_j = np.array([[0,1],[0,1],[1,1]])
    self.t_i = np.array([[1,1,1,1]])
    self.t_z = np.array([[1,1,0],[0,1,1]])
    self.t_s = np.array([[0,1,1],[1,1,0]])
    self.tm_arr = [self.t_o, self.t_t, self.t_l, self.t_j, self.t_i, self.t_z, self.t_s]

    #if __name__ == '__main__':
     # self.main()

  def clear_board(self):
      self.board = np.zeros((20,10))

  def board_height_pos(self, board_in, row):
    height_pos = 0
    while height_pos < 20:
      if board_in[height_pos, row] == 0:
        height_pos += 1
      elif board_in[height_pos, row]:
        break;
    return height_pos

  def tetromino_height(self, tet):
    row = [0] * tet.shape[1]
    i = tet.shape[1] - 1
    while i >= 0:
      j = tet.shape[0] - 1
      while j >= 0:
          if tet[j, i]:
              row[i] = j + 1
              break
          else:
              j -= 1
      i -= 1
    return row

  def line_clear(self, board_in, line):
    while line >= 0:
        if line == 0:
            board_in[0, ] = np.zeros(10)
        else:
            board_in[line, ] = board_in[line - 1, ]
        line -= 1

  def if_line_full(self, board_in):
      ct = 19
      compare_to = np.array([1,1,1,1,1,1,1,1,1,1])
      while ct >= 0:
          if np.all(board_in[ct, ] == compare_to):
              self.line_clear(board_in, ct)
              print("line full and line cleared")

          ct -= 1


  def line(self, board_in):
      ct = 19
      clearcount = 0
      compare_to = np.array([1,1,1,1,1,1,1,1,1,1])
      while ct >= 0:
          if np.all(board_in[ct, ] == compare_to):
              clearcount += 1
          ct -= 1
      return clearcount

  def holes(self, board_in):
      i = 0
      hole = 0
      while i < 10:
          j = 0
          roof = 0
          while j < 20:
              if board_in[j, i]:
                  roof = 1
              if roof:
                  if board_in[j, i] == 0:
                      hole += 1
              j += 1
          i += 1
      return hole

  def bumpiness(self, board_in):
      i = 0
      height = [0]*10
      while i < 10:
          j = 0
          while j < 20:
              if board_in[j, i]:
                  height[i] = 20 - j
                  break
              else:
                  j += 1
          i += 1

      i = 0
      b_ness = 0
      while i < 9:
          b_ness += abs(height[i] - height[i+1])
          i += 1
      return b_ness

  def sum_height(self, board_in):
      i = 0
      height = [0]*10
      while i < 10:
          j = 0
          while j < 20:
              if board_in[j, i]:
                  height[i] = 20 - j
                  break
              else:
                  j += 1
          i += 1

      i = 0
      return np.sum(height)

  def score(self, board_in, line_cl, weight_in): ###WIP:add weighted sum of scores
      print("cleared_lines = ",line_cl)
      print("holes = ",self.holes(board_in))
      print("bumpiness = ",self.bumpiness(board_in))
      print("sum_height = ",self.sum_height(board_in))
      scr = weight_in[0]*line_cl + weight_in[1]*self.holes(board_in) + weight_in[2]*self.bumpiness(board_in) + weight_in[3]*self.sum_height(board_in)
      return scr


  def predict_board(self, tet, action, weight_in):
      temp_board = self.board.copy()

      #action = [rot, mov] rot->(0~3), mov->(0~9)
      rot = action[0]
      mov = action[1]

      tetromino = np.rot90(tet, rot)

      pos = [0,0] #(y,x)

      #get x_pos according to mov
      if mov+tetromino.shape[1] >= 10:
        pos[1] = 10 - tetromino.shape[1]
      else:
        pos[1] = mov

      #get y_pos according to board state
      x_sel = 0
      max_y_pos = 0
      board_hpos = [0] * tetromino.shape[1]

      while x_sel < tetromino.shape[1]:
        board_hpos[x_sel]=self.board_height_pos(temp_board, x_sel + pos[1]) ### check point hpos = height position
        x_sel += 1

      diff_h = np.subtract(board_hpos, self.tetromino_height(tetromino))
      #print(diff_h, board_hpos, self.tetromino_height(tetromino))
      pos[0] = diff_h[np.argmin(diff_h)]
      #print(diff_h[np.argmin(diff_h)])


      #apply action to temp_board
      j=0
      while j < tetromino.shape[0]:
        i = 0
        while i < tetromino.shape[1]:
          abs_pos_y = j + pos[0]
          abs_pos_x = i + pos[1]
          temp_board[abs_pos_y, abs_pos_x] += tetromino[j,i]
          i+=1
        j+=1
      line_cleared = self.line(temp_board)
      self.if_line_full(temp_board)
      ###Reward calc here
      scr = self.score(temp_board, line_cleared, weight_in)
      print("this is a pridiction")
      print(temp_board)
      return scr

  def apply_board(self, tet, action):
    #action = [rot, mov] rot->(0~3), mov->(0~9)
    rot = action[0]
    mov = action[1]

    tetromino = np.rot90(tet, rot)

    pos = [0,0] #(y,x)

    #get x_pos according to mov
    if mov+tetromino.shape[1] >= 10:
      pos[1] = 10 - tetromino.shape[1]
    else:
      pos[1] = mov

    #get y_pos according to board state
    x_sel = 0
    max_y_pos = 0
    board_hpos = [0] * tetromino.shape[1]

    while x_sel < tetromino.shape[1]:
      board_hpos[x_sel]=self.board_height_pos(self.board, x_sel + pos[1]) ### check point hpos = height position
      x_sel += 1

    diff_h = np.subtract(board_hpos, self.tetromino_height(tetromino))
    print(diff_h, board_hpos, self.tetromino_height(tetromino))
    if np.any(diff_h < 0):
        self.is_dead = 0
    pos[0] = diff_h[np.argmin(diff_h)]
    print(diff_h[np.argmin(diff_h)])


    #apply action to self.board
    j=0
    while j < tetromino.shape[0]:
      i = 0
      while i < tetromino.shape[1]:
        abs_pos_y = j + pos[0]
        abs_pos_x = i + pos[1]
        if abs_pos_y < 0:
            self.is_dead = 1
        self.board[abs_pos_y, abs_pos_x] += tetromino[j,i]
        i+=1
      j+=1

    ###only line scoring must be done before the func(if_line_full) activates
    line_cleared = self.line(self.board)
    self.if_line_full(self.board)
    #self.score(self.board, line_cleared)
    print("this is real")
    print(tetromino)
    print(pos)
    print(self.board)
    print()
    output = [line_cleared, self.is_dead]
    return output

    #self.board = isLinecompleted
    #print(board)
