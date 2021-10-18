import numpy as np
class t_env:

  def __init__ (self):
    self.board = np.zeros((20,10))

    #define tetrominos
    self.t_o = np.array([[1,1],[1,1]])
    self.t_t = np.array([[1,1,1],[0,1,0]])
    self.t_l = np.array([[1,0],[1,0],[1,1]])
    self.t_j = np.array([[0,1],[0,1],[1,1]])
    self.t_i = np.array([[1,1,1,1]])
    self.t_z = np.array([[1,1,0],[0,1,1]])
    self.t_s = np.array([[0,1,1],[1,1,0]])

    #if __name__ == '__main__':
     # self.main()

  def board_height_pos(self, row):
    height_pos = 0
    while height_pos < 20:
      if self.board[height_pos, row] == 0:
        height_pos += 1
      elif self.board[height_pos, row]:
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

  def line_clear(self, line):
    while line >= 0:
        if line == 0:
            self.board[0, ] = np.zeros(10)
        else:
            self.board[line, ] = self.board[line - 1, ]
        line -= 1

  def if_line_full(self):
      ct = 19
      compare_to = np.array([1,1,1,1,1,1,1,1,1,1])
      while ct >= 0:
          if np.all(self.board[ct, ] == compare_to):
              self.line_clear(ct)
              print("line full and line cleared")
          ct -= 1

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
      board_hpos[x_sel]=self.board_height_pos(x_sel + pos[1]) ### check point hpos = height position
      x_sel += 1

    diff_h = np.subtract(board_hpos, self.tetromino_height(tetromino))
    print(diff_h, board_hpos, self.tetromino_height(tetromino))
    pos[0] = diff_h[np.argmin(diff_h)]
    print(diff_h[np.argmin(diff_h)])


    #apply action to self.board
    j=0
    while j < tetromino.shape[0]:
      i = 0
      while i < tetromino.shape[1]:
        abs_pos_y = j + pos[0]
        abs_pos_x = i + pos[1]
        self.board[abs_pos_y, abs_pos_x] += tetromino[j,i]
        i+=1
      j+=1

    self.if_line_full()

    print(tetromino)
    print(pos)
    print(self.board)

    #self.board = isLinecompleted
    #print(board)
