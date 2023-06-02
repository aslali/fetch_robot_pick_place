from fetch_robot.tp_pick_place import pickplace
from fetch_robot.tp_initialize_robot import RobotControl
from fetch_robot import tp_blocks
import planner
import threading
import all_parameters as param
import time
import rospy
import server
import sys


class Fetch(threading.Thread):
    def __init__(self, sim_env, task, team_server, human, measure, robot_connected=False):
        self.robot_connected = robot_connected
        if self.robot_connected:
            rospy.init_node('test_code')
            self.robot_con = RobotControl()
            self.blocks = tp_blocks.Blocks()
        threading.Thread.__init__(self)
        self.p_human_allocation = 0.7
        self.p_human_error = 0.1
        self.allocation_time_interval = 0
        self.planner = planner.Planner(self.p_human_allocation, self.p_human_error, self.allocation_time_interval)
        self.task = task
        self.human = human
        self.sim_env = sim_env
        self.team_server = team_server

        self.action_list = {'Robot': 0, 'Done': 1, 'Assigned_to_Human': 2, 'Assigned_to_Robot': 3, 'Reject': 4,
                            'Return': 5, 'Human_by_Robot': 6}

        self.all_allocated_tasks = []
        self.cur_allocated_tasks = []
        self.interaction_history = []
        self.pre_human_tasks_done = []
        self.pre_human_wrong_actions = []
        self.human_accuracy_history = []

        self.save_init_sol = False
        self.safe_dist_hr = 180
        self.measure = measure

        if self.robot_connected:
            self.conveyor_server = server.ServerControl(port_num=5078)
            self.conveyor_server.daemon = True
            self.conveyor_server.start()

    def action(self, place_loc, place_num, pick_loc=None, block_col=None, block_id=None):

        if block_id:
            pickplace(robot_control=self.robot_con, place_loc=place_loc, place_num=place_num, blocks=self.blocks,
                      pick_loc=pick_loc, pick_id=block_id, returning=True, d_thrd_place=0.5)
            self.conveyor_server.send_message('1')
            time.sleep(9)
            self.conveyor_server.send_message('0')
        else:
            pickplace(robot_control=self.robot_con, place_loc=place_loc, place_num=place_num, blocks=self.blocks,
                      pick_loc=pick_loc, pick_col=block_col)

    def action_from_schedule(self, timerob, available_actions, precedence, count):
        act_info = None
        if available_actions:
            ac = available_actions[0]
            in_table_zone = False

            if ac in self.task.remained_tasks:
                workspace = self.task.task_to_do[ac]['workspace']
                box = self.task.task_to_do[ac]['box']
                color = self.task.task_to_do[ac]['color']
                if ac in self.task.human_error_tasks:
                    if self.task.task_to_do[ac]['type'] == 'Reject':
                        self.task.human_error_tasks_reject.remove(ac)
                        in_table_zone = True
                        etype = 'Reject'
                        act_info = {'type': etype, 'workspace': workspace, 'box': box,
                                    'color': color, 'action_number': ac,
                                    'correcting_action': self.task.task_to_do[ac]['wrong_task']}
                    else:
                        self.task.human_error_tasks_return.remove(ac)
                        etype = 'Return'
                        act_info = {'type': etype, 'workspace': workspace, 'box': box,
                                    'color': color, 'action_number': ac,
                                    'correcting_action': self.task.task_to_do[ac]['wrong_task'],
                                    'id': self.task.task_to_do[ac]['id']}

                    self.task.finished_tasks.append(ac)
                    self.task.human_error_tasks.remove(ac)
                else:
                    if ac in self.task.tasks_allocated_to_robot:
                        self.task.tasks_allocated_to_robot.remove(ac)
                        act_info = {'type': 'Assigned_to_Robot', 'workspace': workspace, 'box': box,
                                    'action_number': ac,
                                    'color': color}
                    elif ac in self.task.tasks_allocated_to_human:
                        self.task.tasks_allocated_to_human.remove(ac)
                        act_info = {'type': 'Human_by_Robot', 'workspace': workspace, 'box': box,
                                    'action_number': ac,
                                    'color': color}
                    else:
                        act_info = {'type': 'Robot', 'workspace': workspace,
                                    'box': box,
                                    'color': color,
                                    'action_number': ac}
                    self.task.finished_tasks.append(ac)
            else:
                for i in precedence:
                    if ac in precedence[i]:
                        self.task.tasks_allocated_to_human.append(i)
                        self.all_allocated_tasks.append(i)
                        self.cur_allocated_tasks = self.task.tasks_allocated_to_human[:]
                        break
                workspace = self.task.task_to_do[i]['workspace']
                box = self.task.task_to_do[i]['box']
                color = self.task.task_to_do[i]['color']
                act_info = {'type': 'Assigned_to_Human', 'workspace': workspace, 'box': box,
                            'color': color, 'action_number': ac, 'assigning_action': i}
                in_table_zone = True

            # self.task.finished_tasks.append(i)
            available_actions.pop(0)
        else:
            cccccccccccccccccc = 1
        return act_info, in_table_zone, available_actions

    def robot_action(self, next_action):
        ws = next_action['workspace']
        box = next_action['box']
        color = next_action['color']
        travel_distance = 0

        if next_action['type'] == 'Return':
            self.human.human_wrong_actions.pop(next_action['correcting_action'])
            action_type = self.action_list['Return']
            travel_distance = self.get_travel_distance(task_color=color, action='Return')
        elif next_action['type'] == 'Reject':
            self.human.human_wrong_actions.pop(next_action['correcting_action'])
            action_type = self.action_list['Reject']
        elif next_action['type'] == 'Assigned_to_Human':
            if next_action['assigning_action'] in self.human.human_wrong_actions:
                self.human.human_wrong_actions.pop(next_action['assigning_action'])
            action_type = self.action_list['Assigned_to_Human']
        elif next_action['type'] == 'Human_by_Robot':
            action_type = self.action_list['Human_by_Robot']
            travel_distance = self.get_travel_distance(color)

        elif next_action['type'] == 'Robot':
            action_type = self.action_list['Robot']
            if next_action['action_number'] in self.human.human_wrong_actions:
                self.human.human_wrong_actions.pop(next_action['action_number'])
            travel_distance = self.get_travel_distance(color)
        elif next_action['type'] == 'Assigned_to_Robot':
            if next_action['action_number'] in self.human.human_wrong_actions:
                self.human.human_wrong_actions.pop(next_action['action_number'])
            action_type = self.action_list['Assigned_to_Robot']
            travel_distance = self.get_travel_distance(color)

        msg = str(action_type) + str(ws) + str(box) + str(param.gui_color_code[color])
        self.team_server.send_message(msg)
        return travel_distance

    def get_travel_distance(self, task_color, action=None):
        if action == "Return":
            td = param.d_robot_return
        else:
            if task_color == 'green':
                td = param.d_robot_close
            elif task_color == 'blue':
                td = param.d_robot_far
            elif task_color == 'orange':
                td = param.d_robot_far
            elif task_color == 'pink':
                td = param.d_robot_close
            else:
                raise Exception('Unknown color')
        return td

    def run(self):
        # try:
        self.measure.human_measures(self.measure.init_time, self.p_human_allocation, self.p_human_error)
        self.measure.human_dist_error(self.measure.init_time, self.planner.pbeta, self.planner.beta_set)
        self.measure.human_dist_follow(start_time=self.measure.init_time, pf=self.planner.palpha,
                                       sf=self.planner.alpha_set)
        htmax = max(v[0] for v in list(self.task.t_task_all.values()))
        rtmax = max(v[1] for v in list(self.task.t_task_all.values()))
        punish_h = 1.5 * (rtmax + htmax)
        punish_r = punish_h
        punish_error = 2 * punish_h

        # if self.save_init_sol:
        #     new_human_task, new_robot_task = self.planner.task_selection(task=self.task, hpenalty=punish_h,
        #                                                                  rpenalty=punish_r, error_penalty=punish_error,
        #                                                                  save=self.save_init_sol)
        #     htasks, rtasks, new_pr, new_pr_type2, ttasks = self.task.create_new_task(new_robot_tasks=new_robot_task,
        #                                                                              new_human_tasks=new_human_task)
        #     self.planner.task_scheduler(ttasks, htasks, rtasks, new_pr, new_pr_type2, self.task.remained_tasks,
        #                                 save=self.save_init_sol)

        counter = 0
        new_robot_task = None
        new_human_task = None
        next_robot_turn = False
        isfinished = (len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) == 0)
        if self.robot_connected:
            while self.conveyor_server.conn is None:
                print('waiting for conveyor')
            self.conveyor_server.send_message('1')
            time.sleep(3)
            self.conveyor_server.send_message('0')
        while self.team_server.conn is None:
            print('waiting')
        self.measure.experiment_start_time = self.measure.start_time()
        while self.human.wait_human:
            time.sleep(1)
            print ('waiting for the human')
        while not isfinished:
            start_time_total = self.measure.start_time()
            if len(set(self.task.remained_task_both) - set([self.human.human_current_action])) + len(self.task.remained_task_robot_only) > 0:
                self.team_server.send_message('8000')
                gui_deactivated = True
            self.task.find_remained_task()
            self.task.remove_finished_task_precedence()

            hum_new_actions = []
            pre_tasks = self.pre_human_tasks_done[:]
            for i in self.human.done_tasks:
                if i in pre_tasks:
                    pre_tasks.remove(i)
                else:
                    hum_new_actions.append(i)

            if hum_new_actions:
                human_wrong_actions = []
                for ts in hum_new_actions:
                    if ts in self.human.human_wrong_actions:
                        heaction = 0
                        human_wrong_actions.append(ts)
                    elif ts not in self.human.human_actions_from_allocated:
                        heaction = 1

                    if ts not in self.human.human_actions_from_allocated:
                        self.planner.human_error_update(human_action=heaction,
                                                        action_history=self.human_accuracy_history)
                        self.human_accuracy_history.append(heaction)

                        # self.measure.human_dist_error(start_time=start_time_total, pe=self.planner.pbeta,
                        #                               se=self.planner.beta_set)

                if human_wrong_actions:
                    # seen = set()
                    # dubl = []
                    # for x in human_wrong_actions:
                    #     if x in seen:
                    #         dubl.append(x)
                    #     else:
                    #         seen.add(x)
                    # self.human.double_error = list(set(self.human.double_error) - set(dubl))
                    human_wrong_actions = list(set(human_wrong_actions))
                    de = self.task.update_task_human_error(human_error=human_wrong_actions,
                                                           all_human_error=self.human.human_wrong_actions,
                                                           error_info=self.human.wrong_action_info)

                wrong_assign = [ii for ii in self.human.human_wrong_actions if
                                self.human.human_wrong_actions[ii] == 'Reject']
                tasks_allocated_to_robot = [ii for ii in self.task.tasks_allocated_to_robot]

                for ts in hum_new_actions:
                    if self.cur_allocated_tasks or tasks_allocated_to_robot or wrong_assign:
                        if self.human.action_right_choose[ts] == 1:
                            if ts in self.cur_allocated_tasks:
                                haction = 1
                                self.cur_allocated_tasks.remove(ts)
                            elif (ts in tasks_allocated_to_robot) or (ts in wrong_assign):
                                haction = -1  # Todo: this reduces p_conform significantly
                                try:
                                    tasks_allocated_to_robot.remove(ts)
                                except:
                                    try:
                                        wrong_assign.remove(ts)
                                    except:
                                        pass
                            else:
                                haction = 0

                            self.planner.adaptability_update(human_action=haction,
                                                             action_history=self.interaction_history)
                            self.interaction_history.append(haction)
                            self.measure.human_dist_follow(start_time=start_time_total, pf=self.planner.palpha,
                                                           sf=self.planner.alpha_set)
                self.cur_allocated_tasks = self.task.tasks_allocated_to_human[:]

            self.measure.human_measures(start_time=start_time_total, p_error=self.planner.p_human_error,
                                        p_following=self.planner.p_human_allocation)
            isfinished = (len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) == 0)
            if not isfinished:
                if next_robot_turn:
                    fselec = False
                    fschedule = False
                else:
                    # fselec = self.is_task_selection(new_robot_task, new_human_task)
                    fselec = True
                    if fselec:
                        fschedule = True
                    else:
                        fschedule = self.is_scheduling()

                if fschedule and not isfinished:
                    is_solution = False
                    while not is_solution:
                        if fselec:
                            new_human_task, new_robot_task = self.planner.task_selection(task=self.task,
                                                                                         hpenalty=punish_h,
                                                                                         rpenalty=punish_r,
                                                                                         error_penalty=punish_error,
                                                                                         prev_sol={})

                        htasks, rtasks, new_pr, new_pr_type2, ttasks = self.task.create_new_task(
                            new_robot_tasks=new_robot_task,
                            new_human_tasks=new_human_task)
                        if not rtasks:
                            break
                        rtiming, htiming, precedence, is_solution = self.planner.task_scheduler(task_time=ttasks,
                                                                                                human_tasks=htasks,
                                                                                                robot_tasks=rtasks,
                                                                                                precedence=new_pr,
                                                                                                precedence_type2=new_pr_type2,
                                                                                                remaining_tasks=self.task.remained_tasks,
                                                                                                tasks_human_error=self.task.human_error_tasks,
                                                                                                tasks_human_error_type1=self.task.human_error_tasks_return,
                                                                                                tasks_human_error_type2=self.task.human_error_tasks_reject
                                                                                                )
                    if rtasks:
                        cur_step_actions = [i for i in rtiming if rtiming[i] == 0]
                        t_tray = [i for i in cur_step_actions if i in new_pr_type2]
                        tray_t = [i for i in cur_step_actions if i in self.task.human_error_tasks_reject]
                        w_tray = list(set(cur_step_actions) - set(tray_t) - set(t_tray))
                        available_actions = tray_t + t_tray + w_tray
                        if not available_actions:
                            ccccccccccccc = 1
                        counter = 0
                else:
                    counter += 1

                if rtasks:
                    next_action, next_robot_turn, available_actions = self.action_from_schedule(timerob=rtiming,
                                                                                            available_actions=available_actions,
                                                                                            precedence=precedence,
                                                                                            count=counter)
                    travel_dist = self.robot_action(next_action)

                self.pre_human_tasks_done = self.human.done_tasks[:]
                self.pre_human_wrong_actions = list(self.human.human_wrong_actions.keys())
                if gui_deactivated:
                    self.team_server.send_message('9000')
                    gui_deactivated = False


                if rtasks:
                    start_time_action = self.measure.start_time()
                    send_done_message = False
                    if next_action['type'] == 'Robot':
                        if self.robot_connected:
                            self.action(block_col=next_action['color'], place_num=next_action['box'],
                                        place_loc=next_action['workspace'])
                        else:
                            time.sleep(60)
                        send_done_message = True
                    elif next_action['type'] == 'Assigned_to_Robot':
                        if self.robot_connected:
                            self.action(block_col=next_action['color'], place_num=next_action['box'],
                                        place_loc=next_action['workspace'])
                        else:
                            time.sleep(60)
                        send_done_message = True
                    elif next_action['type'] == 'Return':
                        if self.robot_connected:
                            self.action(pick_loc=next_action['workspace'] * 10 + next_action['workspace'], place_loc=6,
                                        place_num=1, block_id=next_action['id'])
                        else:
                            time.sleep(60)
                        send_done_message = True
                    elif next_action['type'] == 'Human_by_Robot':
                        if self.robot_connected:
                            self.action(block_col=next_action['color'], place_num=next_action['box'],
                                        place_loc=next_action['workspace'])
                        else:
                            time.sleep(30)
                        send_done_message = True

                    if send_done_message:
                        msg = str(self.action_list['Done']) + str(next_action['workspace']) + str(next_action['box']) \
                              + str(param.gui_color_code[next_action['color']])
                        self.team_server.send_message(msg)
                    self.measure.action_end(start_time_total=start_time_total, start_time_action=start_time_action,
                                            agent='robot', travel_distance=travel_dist, action_type=next_action['type'],
                                            action_number=next_action['action_number'])
            #
            # aaaaaaa = 1
            isfinished = (len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) == 0)

        self.measure.experiment_end_time = self.measure.start_time()
        self.measure.run_all()

        # except Exception as ex:
        #     print(ex)
        # self.team_server.server_disconnect()
