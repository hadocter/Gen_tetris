import tetris_module as tm
import numpy as np
import random
#weight = [*Cleared_lines, *holes, *bumpiness, *sum_height]
class main_process(tm.t_env):
    def select_action(self, tet, weight_in): ###weight_in needeeeeeed
        act_n = 0
        act_score = [0] * 40
        act = [0] * 2
        while act_n < 40:
            act[0] = act_n // 10
            act[1] = act_n % 10
            act_score[act_n] = self.predict_board(tet, act, weight_in)
            act_n += 1
        act_n = argmax(act_score)
        act[0] = act_n // 10
        act[1] = act_n % 10
        return act

    def tetromino_rand(self):
        return self.tm_arr[random.randrange(0,7)]

    def go(self, weight_in):
        dead = 0
        while
        tetm = self.tetromino_rand()
        score += self.apply_board(tetm, self.select_action(tetm, weight_in))[0]





    def new(self):
        print(self.board)
