import simulated_environment as se

col1 = ['#00ab99', '#de7e9d', '#184c95', '#f3722a']
col2 = ['g', 'p', 'b', 'o']
col = dict(zip(col2, col1))
pattern_col = {1: [col['o'], col['b'], col['p'], col['p'], col['g']],
               2: [col['g'], col['b'], col['b'], col['g'], col['o']],
               3: [col['b'], col['g'], col['g'], col['o'], col['p']],
               4: [col['b'], col['o'], col['o'], col['p'], col['g']],
               5: [col['p'], col['p'], col['b'], col['g'], col['o']]}

sim_env = se.SHSCPackaging(pattern_col, fast_run=False)


sim_env.canvas.itemconfig(sim_env.compartments_handle[2][1], fill='red')
sim_env.root.mainloop()
