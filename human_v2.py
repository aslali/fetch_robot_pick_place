import threading
from all_parameters import gui_color_code


class Human(threading.Thread):

    def __init__(self, task, team_server, measure):
        threading.Thread.__init__(self)
        self.task = task
        self.team_server = team_server
        self.all_box_states = {0: 'Human', 1: 'Assigned_to_Human', 2: 'Assigned_to_Robot', 3: 'Done', 4: 'Return',
                               5: 'Free'}
        self.task_to_do = task.task_to_do
        self.wrong_actions = {"Robot": [], "Human": [], "Return": []}
        self.human_wrong_actions = {}
        self.done_tasks = []
        self.wrong_action_info = {}
        # self.human_actions = []
        self.human_actions_from_allocated = []
        self.action_right_choose = {}

        self.human_current_action = None
        self.returning_action = None
        self.returned_action = None
        self.last_action_number = -1
        self.measure = measure
        self.save_action = None
        self.wait_human = True

        # self.team_server = server.ServerControl()
        # self.team_server.daemon = True
        # self.team_server.start()

    def get_human_action(self, action):
        box_state, previous_box_state, color = self.get_state_color(action)
        action_number, workspace, box = self.get_action_number(action)
        self.last_action_number = action_number
        self.returned_action = None
        if box_state == 'Human':
            self.human_current_action = action_number
            # if action_number > 19:
            #     self.task.task_precedence_dict[action_number] = []
            #     self.task.task_both.append(action_number)
            #     self.task.tasks_all.append(action_number)
            #     self.task.n_tasks()
            #     self.task_to_do[action_number] = {'workspace': workspace, 'box': box, 'color': color}
            #     self.task.tasks_required_time(task_num=action_number)
            #     self.done_tasks.append(action_number)
            self.wait_human = False

        elif box_state == 'Assigned_to_Human':
            if previous_box_state == 'Human':
                self.human_current_action = None
            else:
                print('Unknown case 1')

        elif box_state == 'Assigned_to_Robot':
            # if action_number > 19:
            #     self.task.tasks_allocated_to_robot.append(action_number)
            #     self.task.task_precedence_dict[action_number] = []
            #     self.task.task_both.append(action_number)
            #     self.task.tasks_all.append(action_number)
            #     self.task.n_tasks()
            #     self.task_to_do[action_number] = {'workspace': workspace, 'box': box, 'color': color}
            #     self.task.tasks_required_time(task_num=action_number)
            #     self.action_right_choose[action_number] = 1
            # else:
            iscor = self.is_correct(color=color, action_number=action_number)
            if iscor:
                self.task.tasks_allocated_to_robot.append(action_number)
                self.save_action = 'Assigned_to_Robot'
            elif not iscor:
                self.human_wrong_actions[action_number] = 'Reject'
                self.wrong_action_info[action_number] = {'type': 'Reject', 'color': color,
                                                         'workspace': workspace,
                                                         'box': box}
                self.save_action = 'Reject'
            else:
                print('Unknown case 2')
            self.done_tasks.append(action_number)
            self.action_right_choose[action_number] = 1

        elif box_state == 'Done':
            if previous_box_state == 'Return':
                self.returning_action = None
            elif action_number in self.task.tasks_allocated_to_human:
                self.task.tasks_allocated_to_human.remove(action_number)
                self.human_actions_from_allocated.append(action_number)
                self.done_tasks.append(action_number)
                self.task.finished_tasks.append(action_number)
                self.action_right_choose[action_number] = 1  # check this
                self.human_current_action = None
                self.save_action = 'Assigned_to_Human'
            elif action_number not in self.task.tasks_allocated_to_human:
                # if action_number < 20:
                if self.is_correct(color=color, action_number=action_number):
                    self.task.finished_tasks.append(action_number)
                    self.save_action = 'Human'
                else:
                    self.human_wrong_actions[action_number] = 'Return'
                    self.wrong_action_info[action_number] = {'type': 'Return', 'color': color,
                                                             'workspace': workspace,
                                                             'box': box, 'id': self.marker_id}
                    self.save_action = 'Return'
                # else:
                #     self.task.finished_tasks.append(action_number)
                self.human_current_action = None
                self.done_tasks.append(action_number)
                self.action_right_choose[action_number] = 1
            else:
                print('Unknown case 3')


        elif box_state == 'Return':
            self.returning_action = action_number
        elif box_state == 'Free':
            if previous_box_state == 'Assigned_to_Robot':
                if action_number in self.task.tasks_allocated_to_robot:
                    self.task.tasks_allocated_to_robot.remove(action_number)
                    self.save_action = "Cancel_Assign"
                else:
                    self.human_wrong_actions.pop(action_number) #todo: how to consider this case?
                    self.save_action = "Cancel_Wrong_Assign"
            elif previous_box_state == 'Human':
                self.human_current_action = None
            elif previous_box_state == 'Return':
                self.returning_action = None
                self.returned_action = action_number
                if action_number in self.human_wrong_actions:
                    self.human_wrong_actions.pop(action_number)
                # elif action_number > 19:
                #     pass
                    self.save_action = 'Correct_Return'
                else:
                    self.human_wrong_actions[action_number] = 'Human_Return'
                    self.wrong_action_info[action_number] = {'type': 'Human_Return', 'color': color,
                                                             'workspace': workspace,
                                                             'box': box}
                    self.task.task_precedence_dict[action_number] = []
                    self.task.finished_tasks.remove(action_number)
                    for i in range(box + 1, 6):
                        task_num = (workspace - 1) * 5 + (i - 1)
                        if task_num not in self.task.finished_tasks:
                            self.task.task_precedence_dict[task_num].append(action_number)
                            break

                    for i in range(box - 1, 0):
                        task_num = (workspace - 1) * 5 + (i - 1)
                        if task_num not in self.task.finished_tasks:
                            self.task.task_precedence_dict[action_number].append(task_num)
                            break

                    self.save_action = 'Wrong_Return'

                self.action_right_choose[action_number] = 1
                self.done_tasks.append(action_number)
            else:
                print('Unknown case 10')

        # self.done_tasks.append(action_number)

    def get_state_color(self, action):
        col_code = int(action[4])
        color = gui_color_code[col_code]
        return self.all_box_states[int(action[1])], self.all_box_states[int(action[0])], color

    def is_correct(self, color, action_number):
        correct_col = self.task_to_do[action_number]['color']
        return color == correct_col

    def get_action_number(self, action):
        ws = int(action[2])
        bn = int(action[3])
        action_number = 5 * (ws - 1) + (bn - 1)
        return action_number, ws, bn

    def get_marker_number(self, msg):
        self.marker_id = int(msg[0:])

    def run(self):
        # self.human_action('T', 'W4', 4, 10)
        # self.human_action('T', 'W3',2,2)
        first_move = True

        while self.team_server.connected:
            msg_from_human = self.team_server.get_message()
            if msg_from_human is not None:
                start_time = self.measure.start_time()
                if len(msg_from_human) > 3:
                    self.get_human_action(msg_from_human)
                    self.task.temp_unavailable_task = self.human_current_action
                else:
                    self.get_marker_number(msg_from_human)
                if self.save_action is not None:
                    self.measure.action_end(start_time_total=0, agent='human',
                                            travel_distance=0, action_type=self.save_action,
                                            action_number=1)
                self.save_action = None

                print('wrong actions: ', self.human_wrong_actions)
                print('done tasks: ', self.done_tasks)
                print('from allocated: ', self.human_actions_from_allocated)
                print('right: ', self.action_right_choose)

                print('current: ', self.human_current_action)
                print('returning: ', self.returning_action)
                print('returned: ', self.returned_action)
