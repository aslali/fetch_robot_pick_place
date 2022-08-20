
import rospy
import moveit_commander
from fetch_driver_msgs.msg import RobotState, JointState, MotorState
import arm_control
import matplotlib.pyplot as plt


def cb(data):
    global joint_val
    # print(data)
    # print(data.joints)
    a = data.joints
    joint_val.append(a[5].effort)
    # for i in range(5, 12):
    #     print(a[i].name, ': ', a[i].effort)


    # print(data.motors)
    # print(data.boards)

def cb2(data):
    print(data)

def cb3(data):
    print(data)


joint_val = []
rospy.init_node("force_test")
_sub = rospy.Subscriber("/robot_state", RobotState, cb)
# _sub = rospy.Subscriber("/robot_state", MotorState, cb3)
# _sub = rospy.Subscriber("/joint_states", JointState, cb2)
# robot = moveit_commander.RobotCommander()
# print(robot.get_current_state())

arm = arm_control.ArmControl()
arm.stow()

rospy.spin()
plt.plot(range(len(joint_val)), joint_val)
plt.show()

