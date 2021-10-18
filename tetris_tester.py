import tetris_module as tm
import numpy as np
t = tm.t_env()
act = [2, 0]
t.apply_board(t.t_t, act)
act2 = [1, 3]
t.apply_board(t.t_l, act2)
act3 = [2, 6]
t.apply_board(t.t_t, act3)
act4 = [3, 9]
t.apply_board(t.t_t, act4)



'''import numpy as np
def tetromino_height(tet):
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
    return row'''
