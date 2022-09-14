import numpy as np
import time
import threading
import random


class Human(threading.Thread):
    speed = 1.0

    def __init__(self, task, speed, sim_env, time_step, measure, p_conformity=1, p_error=0, fast_run=False, rfast=1):
        threading.Thread.__init__(self)
        self.time_step = time_step
        self.task = task
        self.sim_env = sim_env
        self.done_tasks = []
        self.human_wrong_actions = {}
        self.wrong_color_object = {}
        self.p_conformity = p_conformity
        self.p_error = p_error
        self.hpoints = sim_env.hpoints
        self.speed = speed
        self.wrong_action_info = {}
        self.slopdist = {}
        self.double_error = []
        self.human_actions_from_allocated = []
        self.close_tasks = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19]
        self.far_tasks = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.slop_distance()
        self.measure = measure
        self.action_right2choose = {}
        self.update_sim = not fast_run
        self.rfast = rfast



    def get_available_tasks(self):
        human_available_task = []
        human_available_task_error = []
        human_available_wrong_tasks = []
        type1_error = [i for i in self.human_wrong_actions if self.human_wrong_actions[i] == 'type1']
        # type2_error = [i for i in self.human_wrong_actions if self.human_wrong_actions[i] == 'type2']
        cor_wrong_actions = list(set(self.task.remained_tasks) - set(type1_error))
        for i in self.task.remained_tasks:
            robtas = i in self.task.remained_task_robot_only
            preced_check_with_error = any(j in cor_wrong_actions for j in self.task.task_precedence_dict[i])
            preced_check_no_error = any(j in self.task.remained_tasks for j in self.task.task_precedence_dict[i])
            rob_alloc = i in self.task.tasks_allocated_to_robot
            wrong_act = i in self.human_wrong_actions

            if (not robtas) and (not preced_check_with_error) and (not rob_alloc) and (not wrong_act):
                human_available_task_error.append(i)
                if not preced_check_no_error:
                    human_available_task.append(i)
                else:
                    human_available_wrong_tasks.append(i)

        not_allocated_tasks = list(set(human_available_task) - set(self.task.tasks_allocated_to_human))
        not_allocated_tasks_error = list(set(human_available_task_error) - set(self.task.tasks_allocated_to_human))
        tasks_to_allocate = list(set(not_allocated_tasks) - set(self.task.tasks_allocated_to_robot))

        return not_allocated_tasks, tasks_to_allocate, human_available_wrong_tasks, not_allocated_tasks_error

    def is_action_wrong(self):
        pass
    def action_selection(self):
        not_allocated_tasks, tasks_to_allocate, human_available_wrong_tasks, not_allocated_tasks_error = self.get_available_tasks()

        # pf = random.random()
        wrong_action_type1 = False
        wrong_action_type2 = False
        # alloc_robot = False
        # act_info = {}
        # next_action = None
        # is_error = random.random() < self.p_error  # random.random()
        last_action = 0
        if self.is_action_wrong(last_action):
            pass
        if last_action in self.task.tasks_allocated_to_human:
            self.human_actions_from_allocated.append(last_action)
            self.action_right2choose[last_action] = 1
            self.task.tasks_allocated_to_human.remove(last_action)

        if last_action


        # if self.task.tasks_allocated_to_human and pf < self.p_conformity:
            # next_action = random.choice(self.task.tasks_allocated_to_human)
            # self.task.tasks_allocated_to_human.remove(next_action)
            # ds = self.task.task_to_do[next_action][1]
            # ws = self.task.task_to_do[next_action][0]
            act_info = {'type': 'tray1', 'start': 'T', 'destination': 'W{}'.format(ws),
                        'destination_num': ds,
                        'object': self.task.available_color_human_tray[ws], 'action_number': next_action}
            # self.task.available_color_human_tray[ws] = []
            # self.human_actions_from_allocated.append(next_action)
            # self.action_right2choose[next_action] = 1
        #
        elif not_allocated_tasks or (is_error and human_available_wrong_tasks):
            # if is_error:
            #     next_action = random.choice(not_allocated_tasks + human_available_wrong_tasks)
            # else:
            #     next_action = random.choice(not_allocated_tasks)
            # col = self.task.task_to_do[next_action][2]
            # cond1 = (next_action in tasks_to_allocate) and (random.random() < 0.3636 * self.p_conformity ** 2 -
            #                                                 1.356 * self.p_conformity + 0.9982)
            cond1 = (random.random() < 0.3636 * self.p_conformity ** 2 -
                     1.356 * self.p_conformity + 0.9982)
            cond2 = len(not_allocated_tasks) > 1 or bool(self.task.tasks_allocated_to_human)

            if cond1 and cond2:
                s2 = not_allocated_tasks_error + [nn for nn in self.far_tasks if nn in not_allocated_tasks_error]
                s1 = not_allocated_tasks + [nn for nn in self.far_tasks if nn in not_allocated_tasks]
                if is_error:
                    next_action = random.choice(s2)
                else:
                    next_action = random.choice(s1)
                col = self.task.task_to_do[next_action][2]
                ws = self.task.task_to_do[next_action][0]
                if is_error:
                    if next_action in human_available_wrong_tasks:
                        colp = ['r', 'g', 'b', 'y']
                    else:
                        colp = list(set(['r', 'g', 'b', 'y']) - set(list(col)))

                    wrong_col = random.choice(colp)
                    col = wrong_col
                    wrong_action_type2 = True
                    atype = 'error2'
                else:
                    self.task.tasks_allocated_to_robot.append(next_action)
                    alloc_robot = True
                    atype = 'allocate'

                act_info = {'type': atype, 'start': 'T', 'destination': 'rTray',
                            'destination_num': ws,
                            'object': self.task.available_color_table[col][-1], 'action_number': next_action}
                self.task.available_color_robot_tray[ws] = self.task.available_color_table[col][-1]
                self.task.available_color_table[col].pop()
                ll = self.sim_env.table_blocks[col]['status']
                ito = len(ll) - 1 - ll[::-1].index(1)
                self.sim_env.table_blocks[col]['status'][ito] = 0
                self.action_right2choose[next_action] = 1
            else:
                s2 = not_allocated_tasks_error + [nn for nn in self.close_tasks if nn in not_allocated_tasks_error]
                s1 = not_allocated_tasks + [nn for nn in self.close_tasks if nn in not_allocated_tasks]
                if is_error:
                    next_action = random.choice(s2)
                else:
                    next_action = random.choice(s1)
                col = self.task.task_to_do[next_action][2]
                if is_error:
                    if next_action in human_available_wrong_tasks:
                        colp = ['r', 'g', 'b', 'y']
                    else:
                        colp = list(set(['r', 'g', 'b', 'y']) - set(list(col)))
                    wrong_col = random.choice(colp)
                    col = wrong_col
                    wrong_action_type1 = True
                    atype = 'error1'
                else:
                    atype = 'normal'

                act_info = {'type': atype, 'start': 'T',
                            'destination': 'W{}'.format(self.task.task_to_do[next_action][0]),
                            'destination_num': self.task.task_to_do[next_action][1],
                            'object': self.task.available_color_table[col][-1], 'action_number': next_action}
                self.task.available_color_table[col].pop()
                ll = self.sim_env.table_blocks[col]['status']
                ito = len(ll) - 1 - ll[::-1].index(1)
                self.sim_env.table_blocks[col]['status'][ito] = 0
                if len(not_allocated_tasks + human_available_wrong_tasks) > 1:
                    self.action_right2choose[next_action] = 1
                else:
                    self.action_right2choose[next_action] = 0

        elif self.task.tasks_allocated_to_human:
            s1 = self.task.tasks_allocated_to_human + [nn for nn in self.close_tasks if
                                                       nn in self.task.tasks_allocated_to_human]
            next_action = random.choice(s1)
            # ac = random.randint(0, len(self.task.tasks_allocated_to_human) - 1)
            # next_action = self.task.tasks_allocated_to_human[ac]
            self.task.tasks_allocated_to_human.remove(next_action)
            col = self.task.task_to_do[next_action][2]
            ds = self.task.task_to_do[next_action][1]
            ws = self.task.task_to_do[next_action][0]
            act_info = {'type': 'tray1', 'start': 'T', 'destination': 'W{}'.format(ws),
                        'destination_num': ds,
                        'object': self.task.available_color_human_tray[ws], 'action_number': next_action}
            self.task.available_color_human_tray[ws] = []
            self.human_actions_from_allocated.append(next_action)
            self.action_right2choose[next_action] = 0
        elif not not_allocated_tasks:
            pa = [i for i in self.human_wrong_actions if self.human_wrong_actions[i] == 'type2']
            pa += self.task.tasks_allocated_to_robot
            pa += [nn for nn in pa if nn in pa]
            if pa:
                next_action = random.choice(pa)
                if next_action in self.human_wrong_actions:
                    ds = self.task.task_to_do[next_action][1]
                    ws = self.task.task_to_do[next_action][0]
                    act_info = {'type': 'error1', 'start': 'T', 'destination': 'W{}'.format(ws),
                                'destination_num': ds,
                                'object': self.task.available_color_robot_tray[ws], 'action_number': next_action}
                    col = self.wrong_action_info[next_action]['color']
                    wrong_action_type1 = True
                    self.double_error.append(next_action)
                else:
                    self.task.tasks_allocated_to_robot.remove(next_action)
                    # col = self.task.task_to_do[next_action][2]
                    ds = self.task.task_to_do[next_action][1]
                    ws = self.task.task_to_do[next_action][0]
                    act_info = {'type': 'tray2', 'start': 'T', 'destination': 'W{}'.format(ws),
                                'destination_num': ds,
                                'object': self.task.available_color_robot_tray[ws], 'action_number': next_action}
            self.action_right2choose[next_action] = 0
        else:
            raise ValueError('Unconsidered Case')

        if wrong_action_type1 or wrong_action_type2:
            self.human_wrong_actions[next_action] = 'type1' if wrong_action_type1 else 'type2'
            self.wrong_action_info[next_action] = {'color': col, 'object_num': act_info['object'],
                                                   'workspace': act_info['destination'],
                                                   'position_num': act_info['destination_num']}
        elif alloc_robot:
            pass
        else:
            self.task.finished_tasks.append(next_action)
        if next_action is not None:
            self.done_tasks.append(next_action)

        return act_info, next_action

    # def run(self):
    #     # self.human_action('T', 'W4', 4, 10)
    #     # self.human_action('T', 'W3',2,2)
    #     first_move = True
    #
    #     while len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) > 0:
    #         idle_time = 0
    #         travel_dist = 0
    #         start_time = self.measure.start_time()
    #         if first_move:
    #             idle_time, travel_dist = self.human_move_by_position(self.sim_env.human_pos,
    #                                                                  self.sim_env.human_pos_table)
    #             first_move = False
    #             action = None
    #             self.measure.action_end(start_time_total=start_time, agent='human', idle_time=idle_time,
    #                                     travel_distance=travel_dist, action_type= 'idle',
    #                                     action_number= -1)
    #         else:
    #             self.task.find_remained_task()
    #             self.task.remove_finished_task_precedence()
    #             action, action_num = self.action_selection()
    #             if action:
    #                 idle_time, travel_dist = self.human_action(action)
    #                 self.measure.action_end(start_time_total=start_time, agent='human', idle_time=idle_time,
    #                                         travel_distance=travel_dist, action_type=action['type'],
    #                                         action_number=action['action_number'])
