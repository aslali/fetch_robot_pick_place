import simulated_environment as se
import task_state as ts
import robot
import human_v2
import server
from tasks import Task


human_speed = 1
pattern = [
    ['blue', 'blue', 'blue', 'blue', 'green'],
    ['green', 'green', 'green', 'green', 'pink'],
    ['pink', 'pink', 'pink', 'pink', 'orange'],
    ['orange', 'orange', 'orange', 'orange', 'blue'],
    ['pink', 'pink', 'blue', 'green', 'orange']
]

task_precedence_dict = {0: [], 1: [0], 2: [1], 3: [2], 4: [3],
                        5: [], 6: [5], 7: [6], 8: [7], 9: [8],
                        10: [], 11: [10], 12: [11], 13: [12], 14: [13],
                        15: [], 16: [15], 17: [16], 18: [17], 19: [18]}
task_to_do = {}
for j in task_precedence_dict:
    task_to_do[j] = {'workspace': j // 5 + 1, 'box': j % 5 + 1, 'color': pattern[j // 5][j % 5]}
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
print('phase1')
human = human_v2.Human(task=task, team_server=team_server)
# human.daemon = True
print('phase2')
robot = robot.Fetch(sim_env=sim_env, task=task, human=human, team_server=team_server, robot_connected=False)
# robot.daemon = True
print('phase3')

robot.start()
print('phase4')

human.start()

sim_env.root.mainloop()
