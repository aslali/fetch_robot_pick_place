import numpy as np
import copy
import all_parameters as param
import random


class Task:
    def __init__(self, task_only_human, task_only_robot, task_both, task_to_do, task_precedence_dict, human_speed,
                 t_only_human=None, t_only_robot=None, t_both_human=None, t_both_robot=None):
        self.task_only_human = task_only_human
        self.task_only_robot = task_only_robot
        self.task_both = task_both
        self.tasks_allocated_to_human = []
        self.tasks_allocated_to_robot = []

        self.n_task_human_only = None
        self.n_task_robot_only = None
        self.n_task_both = None
        self.n_task_total = None
        self.n_allocated_task = None
        self.human_error_tasks = set()
        self.human_error_tasks_type1 = set()
        self.human_error_tasks_type2 = set()
        self.n_tasks()

        self.task_to_do = task_to_do
        self.task_precedence_dict = task_precedence_dict

        self.t_task_all = {}
        self.d_task_all = {}
        self.human_speed = human_speed
        self.tasks_required_time()




        self.tasks_all = list(range(self.n_task_total))
        self.finished_tasks = []
        self.remained_tasks = []
        self.remained_task_human_only = []
        self.remained_task_robot_only = []
        self.remained_task_both = []
        self.find_remained_task()

        # self.available_color_table = {'g': [0, 1, 2, 3, 4, 5, 6], 'y': [7, 8, 9, 10, 11, 12, 13],
        #                               'b': [14, 15, 16, 17, 18, 19, 20],
        #                               'r': [21, 22, 23, 24, 25, 26, 27]}
        # self.available_color_human_tray = {1: [], 2: [], 3: [], 4: []}
        # self.available_color_robot_tray = {1: [], 2: [], 3: [], 4: []}

    # def all_time(self):
    #     self.t_hum_all = self.t_both_human + self.t_only_human + [np.NaN] * self.n_task_robot_only
    #     self.t_rob_all = self.t_both_robot + [np.NaN] * self.n_task_human_only + self.t_only_robot
    #     self.t_task_all = [self.t_hum_all, self.t_rob_all]
    def tasks_required_time(self):
        for t in self.task_to_do:
            task_number = t
            task_color = self.task_to_do[t][2]
            if task_color == 'g':
                t_robot = 10
                t_human = param.d_human_close / self.human_speed
            elif task_color == 'b':
                t_robot = 30
                t_human = param.d_human_far / self.human_speed
            elif task_color == 'o':
                t_robot = 30
                t_human = param.d_human_close / self.human_speed
            elif task_color == 'p':
                t_robot = 10
                t_human = param.d_human_far / self.human_speed
            else:
                raise Exception('Unknown color')
            self.t_task_all[t] = (t_human, t_robot)



    def n_tasks(self):
        self.n_task_human_only = len(self.task_only_human)
        self.n_task_robot_only = len(self.task_only_robot)
        self.n_task_both = len(self.task_both)
        self.n_task_total = self.n_task_both + self.n_task_robot_only + self.n_task_human_only
        self.n_allocated_task = len(self.tasks_allocated_to_human)

    def find_remained_task(self):
        self.remained_tasks = list(set(self.tasks_all) - set(self.finished_tasks))
        self.remained_task_human_only = list(set(self.task_only_human) - set(self.finished_tasks))
        self.remained_task_robot_only = list(set(self.task_only_robot) - set(self.finished_tasks))
        self.remained_task_both = list(set(self.task_both) - set(self.finished_tasks))

    def creat_precedence_matrix(self, precedence_dict):
        n_task = len(precedence_dict)
        task_precedence = [[0] * n_task for i in range(n_task)]
        keys = list(precedence_dict)
        for i in range(n_task):
            for j in precedence_dict[keys[i]]:
                task_precedence[i][keys.index(j)] = 1
        return task_precedence

    def remove_finished_task_precedence(self):
        for t in self.finished_tasks:
            if t in list(self.task_precedence_dict):
                del self.task_precedence_dict[t]
        for t in self.task_precedence_dict:
            npred = list(set(self.task_precedence_dict[t]) - set(self.finished_tasks))
            self.task_precedence_dict[t] = npred

    def update_task_human_error(self, human_error, all_human_error, double_error, error_info):
        human_error1 = human_error[:]
        while human_error1:
            lcheck = False
            tray_error = False
            ii = human_error1[0]
            # de = list(set(all_human_error.keys())-set(human_error))
            if ii in double_error:
                for tt in self.task_to_do:
                    if len(self.task_to_do[tt]) > 4 and self.task_to_do[tt][4] == ii:
                        self.task_to_do[tt] = (int(error_info[ii]['workspace'][1]), error_info[ii]['position_num'],
                                                         error_info[ii]['color'], error_info[ii]['object_num'], ii)
                        self.human_error_tasks_type1.add(tt)
                        if tt in self.human_error_tasks_type2:
                            self.human_error_tasks_type2.remove(tt)

                human_error1.pop(0)
                double_error.remove(ii)
            else:
                nt = self.n_task_total % 10
                new_task_num = int('{}{}'.format(3 * (10**nt), ii))
                if error_info[ii]['workspace'] == 'rTray':
                    self.task_to_do[new_task_num] = (error_info[ii]['workspace'], error_info[ii]['position_num'],
                                                     error_info[ii]['color'], error_info[ii]['object_num'], ii)
                    tray_error = True
                    self.human_error_tasks_type2.add(new_task_num)
                else:
                    self.task_to_do[new_task_num] = (int(error_info[ii]['workspace'][1]), error_info[ii]['position_num'],
                                                     error_info[ii]['color'], error_info[ii]['object_num'], ii)
                    self.human_error_tasks_type1.add(new_task_num)

                self.human_error_tasks.add(new_task_num)

                if new_task_num not in self.task_precedence_dict:
                    self.task_precedence_dict[new_task_num] = []
                for i in self.task_precedence_dict[human_error1[0]]:
                    if i in all_human_error:
                        for tt in self.task_to_do:
                            if len(self.task_to_do[tt]) >= 5 and self.task_to_do[tt][4] == i:
                                task_num = tt
                        if task_num not in self.task_precedence_dict:
                            self.task_precedence_dict[task_num] = []
                        self.task_precedence_dict[task_num].append(new_task_num)
                        lcheck = True
                        # human_error1 += [human_error1.pop(0)]

                # if lcheck:
                #     human_error1 += [human_error1.pop(0)]
                # else:
                self.task_precedence_dict[human_error1[0]].append(new_task_num)
                # self.task_precedence_dict[new_task_num]=[]
                self.tasks_all.append(new_task_num)
                self.task_only_robot.append(new_task_num)
                # self.n_tasks()
                if tray_error:
                    self.t_task_all[new_task_num] = (-1, 2)
                else:
                    self.t_task_all[new_task_num] = (-1, self.t_task_all[ii][1])
                self.find_remained_task()
                human_error1.pop(0)
        self.n_tasks()
        return double_error

    def create_new_task(self, new_robot_tasks=[], new_human_tasks=[], human_error=[]):
        # n_new_human = len(new_human_tasks)
        # n_new_robot = len(new_robot_tasks)
        # n_new_tasks = n_new_human + n_new_robot
        # new_tasks = new_human_tasks + new_robot_tasks
        dict_temp = copy.deepcopy(self.task_precedence_dict)
        # new_task_num = self.n_task_total
        dict_temp_type2 = {}
        task_req_times = {}
        for i in self.remained_tasks:
            if i in new_robot_tasks:
                task_req_times[i] = self.t_task_all[i][1]
            elif i in new_human_tasks:
                task_req_times[i] = self.t_task_all[i][0]
            elif i in self.remained_task_robot_only:
                task_req_times[i] = self.t_task_all[i][1]
            elif i in self.remained_task_human_only:
                task_req_times[i] = self.t_task_all[i][0]

        for x in new_human_tasks:
            if x not in self.tasks_allocated_to_human:
                new_task_num = int('{}{}'.format(self.n_task_total, x))
                new_task_pred = dict_temp[x][:]
                dict_temp[x].append(new_task_num)

                dict_temp_type2[new_task_num] = (new_task_pred, 2)
                new_robot_tasks.append(new_task_num)
                task_req_times[new_task_num] = 2
                new_task_num += 1

        # new_precedence_matrix = self.creat_precedence_matrix(dict_temp)

        # new_human_tasks += self.remained_task_human_only
        # new_robot_tasks += self.remained_task_robot_only

        return new_human_tasks, new_robot_tasks, dict_temp, dict_temp_type2, task_req_times
