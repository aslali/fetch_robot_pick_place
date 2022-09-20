import threading


class Human(threading.Thread):
    all_action_type = {1: "human", 2: "robot", 3: "human_cancel", 4: "robot_cancel"}
    gui_color_code = {1: 'g', 2: 'b', 3: 'o', 4: 'p'}

    def __init__(self, task_to_do):
        self.all_action_type = {1: "human", 2: "robot", 3: "human_cancel", 4: "robot_cancel"}
        self.gui_color_code = {1: 'g', 2: 'b', 3: 'o', 4: 'p'}
        self.task_to_do = task_to_do

    def get_human_action(self, action):
        action_type = self.get_type(action)
        action_number = self.get_action_number(action)
        if action_type == self.all_action_type[1] or action_type == self.all_action_type[2]:
            is_wrong = self.is_correct(action, action_number)

    def get_type(self, action):
        return self.all_action_type[int(action[0])]

    def is_correct(self, action, action_number):
        col_code = int(action[3])
        col = self.gui_color_code[col_code]
        correct_col = self.task_to_do[action_number][2]
        return col == correct_col

    def get_action_number(self, action):
        ws = int(action[1])
        bn = int(action[2])
        action_number = 5 * (ws - 1) + (bn - 1)
        return action_number
