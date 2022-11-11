import threading
import server

class Human(threading.Thread):

    def __init__(self, task):
        threading.Thread.__init__(self)
        self.all_box_states = {0: 'Human', 1: 'Assigned_to_Human', 2: 'Assigned_to_Robot', 3: 'Done', 4: 'Return', 5: 'Free'}
        self.gui_color_code = {0: 'g', 1: 'b', 2: 'o', 3: 'p', 4: 'w'}
        self.task_to_do = task.task_to_do
        self.wrong_actions = {"robot": [], "human": [], "return": []}
        self.human_wrong_actions = {}
        self.done_tasks = []
        self.human_actions = []
        self.human_server = server.ServerControl()
        self.human_server.daemon = True
        self.human_server.start()

    def get_human_action(self, action):
        box_state, previous_box_state = self.get_type(action)
        action_number = self.get_action_number(action)
        print(action_number)
        if box_state == 'Human':
            print(box_state, previous_box_state)
        elif box_state == 'Assigned_to_Human':
            print(box_state, previous_box_state)
        elif box_state == 'Assigned_to_Robot':
            print(box_state, previous_box_state)
            self.is_correct(action)
        elif box_state =='Done':
            print(box_state, previous_box_state)
        elif box_state == 'Return':
            print(box_state, previous_box_state)
        elif box_state == 'Free':
            print(box_state, previous_box_state)

        #self.done_tasks.append(action_number)


    def get_type(self, action):
        return self.all_box_states[int(action[1])], self.all_box_states[int(action[0])]

    def is_correct(self, action, action_number):
        col_code = int(action[4])
        col = self.gui_color_code[col_code]
        # col = action[3]
        correct_col = self.task_to_do[action_number][2]
        return col == correct_col

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



