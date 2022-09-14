# from fetch_robot.tp_pick_place import pickplace
# from fetch_robot.tp_initialize_robot import RobotControl
# from fetch_robot import tp_blocks
import planner
import threading



class Fetch(threading.Thread):
    def __init__(self, sim_env, task, human):
        # self.robot_con = RobotControl()
        # self.blocks = tp_blocks.Blocks()
        threading.Thread.__init__(self)
        self.p_human_allocation = 0.8
        self.p_human_error = 0.1
        self.allocation_time_interval = 0
        self.planner = planner.Planner(self.p_human_allocation, self.p_human_error, self.allocation_time_interval)
        # self.time_step = time_step
        self.task = task
        self.human = human
        self.sim_env = sim_env

        # self.speed = speed
        # self.rob_slopdist = {}
        # self.hum_slopdist = {}

        self.all_allocated_tasks = []
        self.cur_allocated_tasks = []
        self.interaction_history = []
        self.pre_human_tasks_done = []
        self.pre_human_wrong_actions = []
        self.human_accuracy_history = []

        self.save_init_sol = False
        self.safe_dist_hr = 180
        # self.measure = measure
        # self.update_sim = not fast_run
        # self.rfast = rfast

    def action(self, block_col, pick_loc, place_loc, place_num):
        pass
        # pickplace(robot_control=self.robot_con, pick_col=block_col, blocks=self.blocks, pick_loc=pick_loc,
        #           place_loc=place_loc, place_num=place_num)


    def run(self):
        # self.measure.human_measures(self.measure.init_time, self.p_human_allocation, self.p_human_error)
        # self.measure.human_dist_error(self.measure.init_time, self.planner.pbeta, self.planner.beta_set)
        # self.measure.human_dist_follow(start_time=self.measure.init_time, pf=self.planner.palpha,
        #                                sf=self.planner.alpha_set)
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
        isfinished = len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) == 0
        while not isfinished:
            # start_time_total = self.measure.start_time()
            self.task.find_remained_task()
            self.task.remove_finished_task_precedence()

            hum_new_actions = []
            pre_tasks = self.pre_human_tasks_done[:]
            for i in self.human.done_tasks:
                if i in pre_tasks:
                    pre_tasks.remove(i)
                else:
                    hum_new_actions.append(i)
            # hum_new_actions = list(set(self.human.done_tasks) - set(self.pre_human_tasks_done))
            if hum_new_actions:
                if self.cur_allocated_tasks or self.task.tasks_allocated_to_robot:  # Todo: check why I added self.cur_allocated_task
                    for ts in hum_new_actions:
                        if self.human.action_right2choose[ts] == 1:
                            if ts in self.cur_allocated_tasks:
                                haction = 1
                            elif ts in self.task.tasks_allocated_to_robot:
                                haction = -1  # Todo: this reduces p_conform significantly
                            else:
                                haction = 0

                            self.planner.adaptability_update(human_action=haction,
                                                             action_history=self.interaction_history)
                            self.interaction_history.append(haction)
                            # self.measure.human_dist_follow(start_time=start_time_total, pf=self.planner.palpha,
                            #                                sf=self.planner.alpha_set)
                self.cur_allocated_tasks = self.task.tasks_allocated_to_human[:]

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

                        self.measure.human_dist_error(start_time=start_time_total, pe=self.planner.pbeta,
                                                      se=self.planner.beta_set)

                if human_wrong_actions:
                    seen = set()
                    dubl = []
                    for x in human_wrong_actions:
                        if x in seen:
                            dubl.append(x)
                        else:
                            seen.add(x)
                    self.human.double_error = list(set(self.human.double_error) - set(dubl))
                    human_wrong_actions = list(set(human_wrong_actions))
                    de = self.task.update_task_human_error(human_error=human_wrong_actions,
                                                           double_error=self.human.double_error,
                                                           all_human_error=self.human.human_wrong_actions,
                                                           error_info=self.human.wrong_action_info)
                    # self.human.double_error = de[:]
            # self.measure.human_measures(start_time=start_time_total, p_error=self.planner.p_human_error,
            #                             p_following=self.planner.p_human_allocation)
            isfinished = len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) == 0
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

                # if fselec:
                #     new_human_task, new_robot_task = self.planner.task_selection(task=self.task, hpenalty=punish_h,
                #                                                                  rpenalty=punish_r,
                #                                                                  error_penalty=punish_error)
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
                        rtiming, htiming, precedence, is_solution = self.planner.task_scheduler(task_time=ttasks,
                                                                                                human_tasks=htasks,
                                                                                                robot_tasks=rtasks,
                                                                                                precedence=new_pr,
                                                                                                precedence_type2=new_pr_type2,
                                                                                                remaining_tasks=self.task.remained_tasks,
                                                                                                tasks_human_error=self.task.human_error_tasks,
                                                                                                tasks_human_error_type1=self.task.human_error_tasks_type1,
                                                                                                tasks_human_error_type2=self.task.human_error_tasks_type2,
                                                                                                )
                    cur_step_actions = [i for i in rtiming if rtiming[i] == 0]
                    t_tray = [i for i in cur_step_actions if i in new_pr_type2]
                    tray_t = [i for i in cur_step_actions if i in self.task.human_error_tasks_type2]
                    w_tray = list(set(cur_step_actions) - set(tray_t) - set(t_tray))
                    available_actions = tray_t + t_tray + w_tray
                    if not available_actions:
                        ccccccccccccc = 1
                    counter = 0
                else:
                    counter += 1

                next_action, next_robot_turn, available_actions = self.action_from_schedule(timerob=rtiming,
                                                                                            available_actions=available_actions,
                                                                                            precedence=precedence,
                                                                                            count=counter)
                self.pre_human_tasks_done = self.human.done_tasks[:]
                self.pre_human_wrong_actions = list(self.human.human_wrong_actions.keys())
                # start_time_action = self.measure.start_time()
                # travel_dist = self.robot_action(next_action)
                # self.measure.action_end(start_time_total=start_time_total, start_time_action=start_time_action,
                #                         agent='robot', travel_distance=travel_dist, action_type=next_action['type'],
                #                         action_number=next_action['action_number'])
                #
                # aaaaaaa = 1
                # isfinished = len(self.task.remained_task_both) + len(self.task.remained_task_robot_only) == 0

        # self.measure.run_all()
