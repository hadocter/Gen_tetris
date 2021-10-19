import tetris_module as tm
t = tm.t_env()
act = [1,1]
t.apply_board(t.t_t, act)
weight = [1,1,1,1]
a = t.predict_board(t.t_t, act, weight)
print(a)
