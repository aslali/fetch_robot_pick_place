import threading
import server

class Human(threading.Thread):

    def __init__(self, task):
        threading.Thread.__init__(self)
        self.task = task
        self.all_box_states = {0: 'Human', 1: 'Assigned_to_Human', 2: 'Assigned_to_Robot', 3: 'Done', 4: 'Return', 5: 'Free'}
        self.gui_color_code = {0: 'g', 1: 'b', 2: 'o', 3: 'p', 4: 'w'}
        self.task_to_do = task.task_to_do
        self.wrong_actions = {"robot": [], "human": [], "return": []}
        self.human_wrong_actions = {}
        self.done_tasks = []
        # self.human_actions = []
        self.human_actions_from_allocated = []

        self.human_current_action = None
        self.returning_action = None
        self.returned_action = None

        self.human_server = server.ServerControl()
        self.human_server.daemon = True
        self.human_server.start()

    def get_human_action(self, action):
        box_state, previous_box_state, color = self.get_state_color(action)
        action_number = self.get_action_number(action)
        print(action_number)
        if box_state == 'Human':
            self.human_current_action = action_number
            print(box_state, previous_box_state)

        elif box_state == 'Assigned_to_Human':
            if previous_box_state == 'Human':
                self.human_current_action = None
            else:
                print('Unknown case 1')
            print(box_state, previous_box_state)

        elif box_state == 'Assigned_to_Robot':
            print(box_state, previous_box_state)
            iscor = self.is_correct(color=color, action_number=action_number)
            if iscor:
                self.task.tasks_allocated_to_robot.append(action_number)
            elif not iscor:
                self.human_wrong_actions[action_number] = 'assign'
            else:
                print('Unknown case 2')
            self.done_tasks.append(action_number)

        elif box_state == 'Done':
            if previous_box_state == 'Return':
                self.returning_action = None
            elif action_number in self.task.tasks_allocated_to_human:
                self.task.tasks_allocated_to_human.remove(action_number)
                self.human_actions_from_allocated.append(action_number)
                self.done_tasks.append(action_number)
            elif action_number not in self.task.tasks_allocated_to_human:
                if self.is_correct(color=color, action_number=action_number):
                    pass
                else:
                    self.human_wrong_actions[action_number] = 'place'
                self.done_tasks.append(action_number)
            else:
                print('Unknown case 3')

            print(box_state, previous_box_state)

        elif box_state == 'Return':
            self.returning_action = action_number
            print(box_state, previous_box_state)
        elif box_state == 'Free':
            if previous_box_state == 'Assigned_to_Robot':
                if action_number in self.task.tasks_allocated_to_robot:
                    self.task.tasks_allocated_to_robot.remove(action_number)
                else:
                    self.human_wrong_actions.pop(action_number)
            elif previous_box_state == 'Human':
                self.human_current_action = None
            elif previous_box_state == 'Return':
                self.returning_action = None
                self.returned_action = action_number
            else:
                print('Unknown case 10')
            print(box_state, previous_box_state)

        #self.done_tasks.append(action_number)


    def get_state_color(self, action):
        col_code = int(action[4])
        col = self.gui_color_code[col_code]
        return self.all_box_states[int(action[1])], self.all_box_states[int(action[0])], col

    def is_correct(self, color, action_number):
        correct_col = self.task_to_do[action_number][2]
        return color == correct_col

    def get_action_number(self, action):
        ws = int(action[2])
        bn = int(action[3])
        action_number = 5 * (ws - 1) + (bn - 1)
        return action_number

    def run(self):
        # self.human_action('T', 'W4', 4, 10)
        # self.human_action('T', 'W3',2,2)
        first_move = True

        while self.human_server.connected:
            msg_from_human = self.human_server.get_message()
            if msg_from_human is not None:
                self.get_human_action(msg_from_human)
                # self.human_actions.append(msg_from_human)



