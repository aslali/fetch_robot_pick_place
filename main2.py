import time

import simulated_environment as se
import task_state as ts
import robot
import human_v2
import server
from tasks import Task



import rospy
from fetch_robot.tp_initialize_robot import RobotControl
from fetch_robot.tp_pick_place import pickplace
from fetch_robot.tp_blocks import Blocks

rospy.init_node('test_code')
robot_con = RobotControl()
block_count = Blocks()
time.sleep(10)

# a = pickplace(robot_control=robot_con, pick_col='o', blocks=block_count, pick_loc=1, place_loc=1, place_num=3)
# a = pickplace(robot_control=robot_con, pick_col='o', blocks=block_count, pick_loc=1, place_loc=1, place_num=5)
# a = pickplace(robot_control=robot_con, place_loc=6, place_num=1, blocks=block_count, pick_loc=11, pick_id=86,
#               returning=False)
a = pickplace(robot_control=robot_con, pick_col='green', place_loc=3, place_num=1, blocks=block_count)
a = pickplace(robot_control=robot_con, pick_col='orange', place_loc=3, place_num=2, blocks=block_count)

# a = pickplace(robot_control=robot_con, pick_col='o', pick_loc=1, place_loc=1, place_num=1)
# a = pickplace(robot_control=robot_con, pick_id=80, pick_loc=1, place_loc=1, place_num=4)
# a = pickplace(robot_control=robot_con, pick_id=25, pick_loc=4, place_loc=1, place_num=3)
# a = pickplace(robot_control=robot_con, pick_id=26, pick_loc=4, place_loc=1, place_num=2)
print(a)

# a = pickplace(robot_control=robot_con, pick_id=3, pick_loc=3, place_loc=1, place_num=4)
# a = pickplace(robot_control=robot_con, pick_id=20, pick_loc=3, place_loc=1, place_num=5)