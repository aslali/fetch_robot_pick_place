from fetch_robot.tp_pick_place import pickplace
from fetch_robot.tp_initialize_robot import RobotControl
from fetch_robot import tp_blocks


class Fetch:
    def __init__(self):
        self.robot_con = RobotControl()
        self.blocks = tp_blocks.Blocks()

    def action(self, block_col, pick_loc, place_loc, place_num):
        pickplace(robot_control=self.robot_con, pick_col=block_col, blocks=self.blocks, pick_loc=pick_loc,
                  place_loc=place_loc, place_num=place_num)
