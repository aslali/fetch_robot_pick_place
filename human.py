import threading
class Human(threading.Thread):
    def __init__(self, task, sim_env, speed):
        threading.Thread.__init__(self)
        self.task = task
        self.sim_env = sim_env
        self.done_tasks = []
        self.human_wrong_actions = {}
        self.wrong_color_object = {}
        self.hpoints = sim_env.hpoints
        self.speed = speed
        self.wrong_action_info = {}
        self.slopdist = {}
        self.double_error = []
        self.human_actions_from_allocated = []
        self.close_tasks = [0, 1, 2, 3, 4, 15, 16, 17, 18, 19]
        self.far_tasks = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.slop_distance()
        # self.measure = measure
        self.action_right_choose = {}
        # self.update_sim = not fast_run
        # self.rfast = rfast