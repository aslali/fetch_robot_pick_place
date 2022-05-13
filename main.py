
import simulated_environment as se
task_to_do = {0: (1, 1, 'y'), 1: (1, 2, 'y'), 2: (1, 3, 'y'), 3: (1, 4, 'y'), 4: (1, 5, 'r'),
              5: (2, 1, 'r'), 6: (2, 2, 'r'), 7: (2, 3, 'r'), 8: (2, 4, 'r'), 9: (2, 5, 'g'),
              10: (3, 1, 'g'), 11: (3, 2, 'g'), 12: (3, 3, 'g'), 13: (3, 4, 'g'), 14: (3, 5, 'b'),
              15: (4, 1, 'b'), 16: (4, 2, 'b'), 17: (4, 3, 'b'), 18: (4, 4, 'b'), 19: (4, 5, 'y')}
pattern_col = {}
col1 = ['#00a933', '#ffff00', '#2a6099', '#ff0000']
col2 = ['g', 'y', 'b', 'r']
col = dict(zip(col2, col1))
for i in task_to_do.values():
    pattern_col[(i[0], i[1])] = col[i[2]]
sim_env = se.SHSCPackaging(pattern_col, fast_run=False)

sim_env.root.mainloop()