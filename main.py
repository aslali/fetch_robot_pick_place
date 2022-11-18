import simulated_environment as se
import task_state as ts
import robot
import human_v2
import server
from tasks import Task

human_speed = 10
pattern = [
    ['o', 'b', 'p', 'p', 'g'],
    ['g', 'b', 'b', 'g', 'o'],
    ['b', 'g', 'g', 'o', 'p'],
    ['b', 'o', 'o', 'p', 'g'],
    ['p', 'p', 'b', 'g', 'o']
]

task_precedence_dict = {0: [], 1: [0], 2: [1], 3: [2], 4: [3],
                        5: [], 6: [5], 7: [6], 8: [7], 9: [8],
                        10: [], 11: [10], 12: [11], 13: [12], 14: [13],
                        15: [], 16: [15], 17: [16], 18: [17], 19: [18]}
task_to_do = {}
for j in task_precedence_dict:
    task_to_do[j] = (j // 5 + 1, j % 5 + 1, pattern[j // 5][j % 5])
task_only_human = []
task_only_robot = []
task_both = list(range(20))

sim_env = se.SHSCPackaging(pattern, fast_run=False)
# task_state = ts.TaskState()
task = Task(task_only_human=task_only_human, task_only_robot=task_only_robot, task_both=task_both,
            task_to_do=task_to_do, task_precedence_dict=task_precedence_dict, human_speed=human_speed)

team_server = server.ServerControl()
team_server.daemon = True
team_server.start()

human = human_v2.Human(task=task, team_server=team_server)
robot = robot.Fetch(sim_env=sim_env, task=task, human=human, team_server=team_server)

#robot.start()
human.start()

sim_env.root.mainloop()
