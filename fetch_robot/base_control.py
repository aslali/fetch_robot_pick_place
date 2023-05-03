import copy

import rospy
import geometry_msgs.msg
import tf
import trajectory_msgs.msg
import control_msgs.msg
import yaml
import time
import actionlib
import moveit_commander
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import sin, cos, pi
from socket import *


class BaseControl(object):
    """ Move base and navigation """

    def __init__(self):
        ## Create publisher to move the base
        self._pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
        self.tf_listener = tf.TransformListener()

        ##action client for navigation
        self.client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("Waiting for move_base...")
        if not self.client.wait_for_server():
            rospy.logerr(
                "Could not connect to move_base... Did you roslaunch fetch_navigation fetch_nav.launch map_file:=/home/fetch_admin/map_directory/5427_updated.yaml?")
        else:
            rospy.loginfo("Got move_base")

        self.actual_positions = None
        self.actual_vel = (0, 0, 0)

        ## subscribe to odom to get the robot current position
        # def callback(msg):
        #     p = msg.pose.pose.position
        #     self.actual_positions = (p.x, p.y, p.z)

        # self._sub = rospy.Subscriber("/odom", Odometry, callback)
        # self.actual_positions = (0, 0, 0)

        while self._pub.get_num_connections() == 0:
            rospy.sleep(0.1)

    def move_forward(self, second=None, distance=None, speed=0.2):
        tw = geometry_msgs.msg.Twist()
        if (second is None) and (distance is None):
            tw.linear.x = abs(speed)
            self._pub.publish(tw)
        elif (second is not None) and (distance is None):
            cur_time = time.time()
            while time.time() - cur_time < second:
                tw.linear.x = abs(speed)
                self._pub.publish(tw)
            # self.get_pose()

        elif (second is None) and (distance is not None):
            cur_time = time.time()
            while time.time() - cur_time < 1:
                tw.linear.x = abs(0)
                self._pub.publish(tw)
            init_pos = self.get_pose()
            dx = 0
            dy = 0
            while max(dx, dy) < distance:
                tw.linear.x = abs(speed)
                self._pub.publish(tw)
                cur_pos = self.get_pose()
                dx = abs(cur_pos[0] - init_pos[0])
                dy = abs(cur_pos[1] - init_pos[1])
                # old_pos = copy.copy(cur_pos)
        elif (second is not None) and (distance is not None):
            print("only one of second or distance!")

    def move_backward(self, second=None, distance=None, speed=-0.2):
        tw = geometry_msgs.msg.Twist()
        if (second is None) and (distance is None):
            tw.linear.x = -abs(speed)
            self._pub.publish(tw)
        elif (second is not None) and (distance is None):
            cur_time = time.time()
            while time.time() - cur_time < second:
                tw.linear.x = -abs(speed)
                self._pub.publish(tw)
            # self.get_pose()

        elif (second is None) and (distance is not None):
            cur_time = time.time()
            while time.time() - cur_time < 1:
                tw.linear.x = -abs(0)
                self._pub.publish(tw)
            init_pos = self.get_pose()
            dx = 0
            dy = 0
            while max(dx, dy) < distance:
                tw.linear.x = -abs(speed)
                self._pub.publish(tw)
                cur_pos = self.get_pose()
                dx = abs(cur_pos[0] - init_pos[0])
                dy = abs(cur_pos[1] - init_pos[1])
                # old_pos = copy.copy(cur_pos)
        elif (second is not None) and (distance is not None):
            print("only one of second or distance!")

    def turn_left(self, angle=0.2):
        tw = geometry_msgs.msg.Twist()
        tw.angular.z = abs(angle)
        self._pub.publish(tw)
        # if s:
        #     s.send(",".join([str(d) for d in list(self.get_pose())]))

    def turn_right(self, angle=-0.2):
        tw = geometry_msgs.msg.Twist()
        tw.angular.z = -abs(angle)
        self._pub.publish(tw)
        # if s:
        #     s.send(",".join([str(d) for d in list(self.get_pose())]))

    ## get 3D position of the robot
    def get_pose(self):
        # self.move_forward(speed=0.01)
        # self.tf_listener.waitForTransform('/map', '/base_link', rospy.Time.now(), rospy.Duration(4.0))
        (trans, rot) = self.tf_listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        new_rot = tf.transformations.euler_from_quaternion(rot)
        # print(trans, new_rot)
        self.actual_positions = [trans[0], trans[1], new_rot[2]]
        return self.actual_positions

    # def __del__(self):
    #     print(1)
    #     self._pub.publish(geometry_msgs.msg.Twist())
    #     print(22)
    #     move_goal = MoveBaseGoal()
    #     print(3)
    #     self.client.send_goal(move_goal)
    #     print(4)
    #     self.client.wait_for_result()
    #     print(5)

    ##### Navigation
    def goto(self, x, y, theta, frame="map"):
        move_goal = MoveBaseGoal()
        move_goal.target_pose.pose.position.x = x
        move_goal.target_pose.pose.position.y = y
        move_goal.target_pose.pose.orientation.z = sin(theta / 2.0)
        move_goal.target_pose.pose.orientation.w = cos(theta / 2.0)
        move_goal.target_pose.header.frame_id = frame
        move_goal.target_pose.header.stamp = rospy.Time.now()
        self.client.send_goal(move_goal)
        self.client.wait_for_result()
        # if s:
        #     s.send(",".join([str(d) for d in list(self.get_pose())]))

    def goto_relative(self, dx, dy, dtheta, frame="map"):
        move_goal = MoveBaseGoal()
        move_goal.target_pose.pose.position.x = self.actual_positions[0] + dx
        move_goal.target_pose.pose.position.y = self.actual_positions[1] + dy
        move_goal.target_pose.pose.orientation.z = self.actual_positions[2] + sin(dtheta / 2.0)
        move_goal.target_pose.pose.orientation.w = self.actual_positions[2] + cos(dtheta / 2.0)

        # move_goal.target_pose.pose.orientation.z = dtheta
        # move_goal.target_pose.pose.orientation.w = 1

        move_goal.target_pose.header.frame_id = frame
        move_goal.target_pose.header.stamp = rospy.Time.now()
        self.client.send_goal(move_goal)
        self.client.wait_for_result()
        if s:
            s.send(",".join([str(d) for d in list(self.get_pose())]))


if __name__ == '__main__':
    rospy.init_node("test_base")
    base_control = BaseControl()

    # print ([-5.32,-1.55,0])
    # base_control.goto(-5.32, -1.55, pi/2)
    # time.sleep(2)
    # for i in range(0, 2):
    #     base_control.move_forward()
    # print(base_control.get_pose())

    # base_control.move_right(angle=2*pi)
    # time.sleep(2)

    # init_time = time.time()
    # while time.time() - init_time < 2:
    #     # for i in range(100):
    #     base_control.turn_right(angle=pi / 2)
    #     # time.sleep(0.01)

    base_control.move_forward(distance=0.5)
    while True:
        print(base_control.get_pose())

    # print(base_control.get_pose())
    # base_control.move_right(45)
    # base_control.move_forward(1.0)
    # time.sleep(2)
    # base_control.move_forward()
    # base_control.move_right()
