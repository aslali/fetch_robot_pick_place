import simulated_environment as se
import task_state as ts
import robot
import human_v2
import server
from tasks import Task
import measure


human_speed = 1
pattern_number = 2


# pattern = [
#     ['blue', 'blue', 'blue', 'blue', 'green'],
#     ['green', 'green', 'green', 'green', 'pink'],
#     ['pink', 'pink', 'pink', 'pink', 'orange'],
#     ['orange', 'orange', 'orange', 'orange', 'blue'],
#     ['pink', 'pink', 'blue', 'green', 'orange']
# ]

if pattern_number == 1:
    pattern = [
        ['blue', 'green', 'orange', 'orange', 'blue'],
        ['pink', 'blue', 'green', 'green', 'pink'],
        ['orange', 'pink', 'blue', 'blue', 'orange'],
        ['green', 'orange', 'pink', 'pink', 'green'],
        ['pink', 'pink', 'blue', 'green', 'orange']
    ]
elif pattern_number == 2:
    pattern = [
        ['orange', 'orange', 'green', 'green', 'pink'],
        ['pink', 'orange', 'orange', 'pink', 'blue'],
        ['pink', 'pink', 'blue', 'blue', 'green'],
        ['blue', 'green', 'green', 'blue', 'orange'],
        ['pink', 'pink', 'blue', 'green', 'orange']
    ]
    # pattern = [
    #     ['orange', 'orange', 'blue', 'blue', 'orange'],
    #     ['orange', 'orange', 'orange', 'orange', 'blue'],
    #     ['pink', 'orange', 'blue', 'green', 'green'],
    #     ['blue', 'green', 'green', 'green', 'pink'],
    #     ['blue', 'blue', 'blue', 'green', 'pink']
    # ]
elif pattern_number == 3:
    pattern = [
        ['pink', 'orange', 'green', 'orange', 'pink'],
        ['green', 'pink', 'blue', 'pink', 'green'],
        ['blue', 'green', 'orange', 'green', 'blue'],
        ['orange', 'blue', 'pink', 'blue', 'orange'],
        ['pink', 'pink', 'blue', 'green', 'orange']
    ]
elif pattern_number == 4:
    pattern = [
        ['orange', 'orange', 'blue', 'blue', 'pink'],
        ['blue', 'blue', 'pink', 'pink', 'green'],
        ['pink', 'pink', 'green', 'green', 'orange'],
        ['green', 'green', 'orange', 'orange', 'blue'],
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

team_server = server.ServerControl(port_num=5077)
team_server.daemon = True
team_server.start()



measure = measure.Measure(directory='16268', case_name='task4.pickle')
print('phase1')
human = human_v2.Human(task=task, team_server=team_server, measure=measure)
# human.daemon = True
print('phase2')
robot = robot.Fetch(sim_env=sim_env, task=task, human=human, team_server=team_server, measure=measure, robot_connected=True)
# robot.daemon = True
print('phase3')

measure.init_time = measure.start_time()
robot.start()
print('phase4')

human.start()

sim_env.root.mainloop()

