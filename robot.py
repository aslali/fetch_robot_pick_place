from fetch_robot.tp_pick_place import pickplace
from fetch_robot.tp_initialize_robot import RobotControl
from fetch_robot import tp_blocks
import planner


class Fetch():
    def __init__(self, sim_env, task, human):
        self.robot_con = RobotControl()
        self.blocks = tp_blocks.Blocks()

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

        self.slop_distance()
        self.tasks_required_time()

        self.save_init_sol = False
        self.safe_dist_hr = 180
        # self.measure = measure
        # self.update_sim = not fast_run
        # self.rfast = rfast

    def tasks_required_time(self):
        for i in range(5):
            self.task.t_task_all[i] = (self.hum_slopdist['TW1'][0] * 2 / self.human.speed,
                                       self.rob_slopdist['TW1'][0] * 2 / self.speed + 2)
            self.task.d_task_all[i] = self.hum_slopdist['TW1'][0] * 2
        for i in range(5, 10):
            self.task.t_task_all[i] = (self.hum_slopdist['TW2'][0] * 2 / self.human.speed,
                                       self.rob_slopdist['TW2'][0] * 2 / self.speed + 2)
            self.task.d_task_all[i] = self.hum_slopdist['TW2'][0] * 2
        for i in range(10, 15):
            self.task.t_task_all[i] = (self.hum_slopdist['TW3'][0] * 2 / self.human.speed,
                                       self.rob_slopdist['TW3'][0] * 2 / self.speed + 2)
            self.task.d_task_all[i] = self.hum_slopdist['TW3'][0] * 2
        for i in range(15, 20):
            self.task.t_task_all[i] = (self.hum_slopdist['TW4'][0] * 2 / self.human.speed,
                                       self.rob_slopdist['TW4'][0] * 2 / self.speed + 2)
            self.task.d_task_all[i] = self.hum_slopdist['TW4'][0] * 2
            
    def action(self, block_col, pick_loc, place_loc, place_num):
        pickplace(robot_control=self.robot_con, pick_col=block_col, blocks=self.blocks, pick_loc=pick_loc,
                  place_loc=place_loc, place_num=place_num)

