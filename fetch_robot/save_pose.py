import rospy
from torso_control import TorsoControl
from head_control import HeadControl

file = open("robot_poses.csv", "w")
file.write("torso_lift,head_tilt\n")
rospy.init_node("test")
torso = TorsoControl()
head = HeadControl()

for i in range(10):
    torso.move_to(0.4/10.0 * i)
    raw_input('Adjust the head and press any key to continue')
    file.write(str(0.4/10.0 * i) + "," + str(head.get_pose()[1]) + "\n")

file.close()
