import simulated_environment as se
import task_state as ts
from all_parameters import colors



pattern_col = {1: [colors['o'], colors['b'], colors['p'], colors['p'], colors['g']],
               2: [colors['g'], colors['b'], colors['b'], colors['g'], colors['o']],
               3: [colors['b'], colors['g'], colors['g'], colors['o'], colors['p']],
               4: [colors['b'], colors['o'], colors['o'], colors['p'], colors['g']],
               5: [colors['p'], colors['p'], colors['b'], colors['g'], colors['o']]}

sim_env = se.SHSCPackaging(pattern_col, fast_run=False)
task_state = ts.TaskState()
robot = 

sim_env.canvas.itemconfig(sim_env.compartments_handle[2][1], fill='red')
sim_env.root.mainloop()
