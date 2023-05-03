import time

import rospy

from arm_control import ArmControl
from camera_modules import *
from torso_control import TorsoControl
from gripper_control import GripperControl, CLOSED_POS, OPENED_POS
from base_control import BaseControl
from fetch_driver_msgs.msg import RobotState
from sensor_msgs.msg import Imu


class PickPlace(object):
    def __init__(self, robot_control=None):
        self.torso = None
        self.gripper = None
        self.arm = None
        self.base = None
        self.robot_control = robot_control

        self.pre_pick_h = None
        self.pre_pick_pos = None
        self.pick_pos = None
        self.post_pick_h = None
        self.post_pick_pos = None
        self.post_pick_x = None

        self.pre_place_pos = None
        self.pre_place_h = None
        self.place_pos = None
        self.post_place_pos = None
        self.post_place_h = None
        self.post_place_x = None

        self.joint_effort = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
                     "upperarm_roll_joint": [], "elbow_flex_joint": [],
                     "forearm_roll_joint": [], "wrist_flex_joint": [],
                     "wrist_roll_joint": []}
        # self.joint_velocity = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
        #              "upperarm_roll_joint": [], "elbow_flex_joint": [],
        #              "forearm_roll_joint": [], "wrist_flex_joint": [],
        #              "wrist_roll_joint": []}
        #
        # self.joint_position = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
        #              "upperarm_roll_joint": [], "elbow_flex_joint": [],
        #              "forearm_roll_joint": [], "wrist_flex_joint": [],
        #              "wrist_roll_joint": []}
        #
        #
        # self.desired_effort = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
        #              "upperarm_roll_joint": [], "elbow_flex_joint": [],
        #              "forearm_roll_joint": [], "wrist_flex_joint": [],
        #              "wrist_roll_joint": []}
        # self.desired_velocity = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
        #              "upperarm_roll_joint": [], "elbow_flex_joint": [],
        #              "forearm_roll_joint": [], "wrist_flex_joint": [],
        #              "wrist_roll_joint": []}
        # self.desired_position = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
        #              "upperarm_roll_joint": [], "elbow_flex_joint": [],
        #              "forearm_roll_joint": [], "wrist_flex_joint": [],
        #              "wrist_roll_joint": []}
        #
        #
        # self.joint_dv = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
        #              "upperarm_roll_joint": [], "elbow_flex_joint": [],
        #              "forearm_roll_joint": [], "wrist_flex_joint": [],
        #              "wrist_roll_joint": []}
        # self.imu_vel_val = {"x": [], "y": [], "z": []}

        self.init_controllers()

    def init_controllers(self):
        if self.robot_control is None:
            self.arm = ArmControl()
            self.gripper = GripperControl()
            self.torso = TorsoControl()
            self.base = BaseControl()
        else:
            self.arm = self.robot_control.fetch_arm
            self.gripper = self.robot_control.fetch_gripper
            self.torso = self.robot_control.fetch_torso
            self.base = self.robot_control.fetch_base

    def cb(self, data):
        a = data.joints
        self.curtime.append(time.time() - self.init_time)
        for ii in range(7):
            self.joint_effort[a[ii + 5].name].append(a[ii + 5].effort)
            # if len(self.curtime) > 1:
                # dv = a[ii + 5].velocity - self.joint_velocity[a[ii + 5].name][-1]
                # dt = self.curtime[-1] - self.curtime[-2]
                # self.joint_dv[a[ii + 5].name].append(dv/dt)
            # self.joint_velocity[a[ii + 5].name].append(a[ii + 5].velocity)
            # self.joint_position[a[ii + 5].name].append(a[ii + 5].position)
            # self.desired_velocity[a[ii + 5].name].append(a[ii + 5].desired_velocity)
            # self.desired_position[a[ii + 5].name].append(a[ii + 5].desired_position)
            # self.desired_effort[a[ii + 5].name].append(a[ii + 5].effort)

            # print(a[ii + 5].name)



    def pick(self, do_stow=True):
        if not self.torso.is_there(self.pre_pick_h):
            self.torso.move_to(self.pre_pick_h, duration=6)
            while not self.torso.is_there(self.pre_pick_h):
                time.sleep(0.5)
        # print(self.pre_pick_pos[0])
        self.arm.move_cartesian_position(self.pre_pick_pos[0], self.pre_pick_pos[1])
        # time.sleep(0.5)
        self.gripper.open()
        self.arm.move_cartesian_position(self.pick_pos[0], self.pick_pos[1])
        self.gripper.close(pos=CLOSED_POS, max_effort=100)
        time.sleep(0.5)
        self.arm.move_cartesian_position(self.post_pick_pos[0], self.post_pick_pos[1])
        # time.sleep(0.5)
        if do_stow:
            self.arm.stow(wait=False)
            # time.sleep(0.5)
        if self.post_pick_x:
            self.base.move_backward(distance=self.post_pick_x)
        if not self.torso.is_there(self.post_pick_h):
            self.torso.move_to(self.post_pick_h, duration=2)
            # time.sleep(3)

    def place(self, release=False, do_stow=True):
        if not self.torso.is_there(self.pre_place_h):
            self.torso.move_to(self.pre_place_h, duration=6)
            while not self.torso.is_there(self.pre_place_h):
                time.sleep(0.5)
        self.arm.move_cartesian_position(self.pre_place_pos[0], self.pre_place_pos[1])
        # time.sleep(0.5)
        self.curtime = []
        self.init_time = time.time()

        self._sub = rospy.Subscriber("/robot_state", RobotState, self.cb)
        time.sleep(1)
        self.arm.move_cartesian_position(self.place_pos[0], self.place_pos[1], wait=False, a_scale=0.5, v_scale=0.4)
        # time.sleep(2)

        ctime =time.time()
        self.curtime = []
        self.init_time = time.time()

        if release:
            self.gripper.open(pos=OPENED_POS)
        else:
            while time.time() - ctime < 5:
                # print(self.joint_effort['shoulder_lift_joint'])
                if self.joint_effort["shoulder_lift_joint"][-1] > 4:
                    self.arm.arm_group.stop()
                    self.gripper.open(pos=OPENED_POS)
                    # self.fetch_arm.arm_group.stop()
                    break

        # # self.fetch_arm.arm_group.stop()
        # # time.sleep(0.5)

        self._sub.unregister()
        # self._sub2.unregister()
        self.gripper.open(pos=OPENED_POS)
        self.arm.move_cartesian_position(self.post_place_pos[0], self.post_place_pos[1])
        # time.sleep(0.5)
        if do_stow:
            self.arm.stow(wait=False)
            # time.sleep(0.5)
        if self.post_place_x:
            self.base.move_backward(distance=self.post_place_x)
        if not self.torso.is_there(self.post_place_h):
            self.torso.move_to(self.post_place_h, duration=2.0)
            # time.sleep(1)

    def reset_pos(self):
        self.gripper.open(pos=OPENED_POS)
        time.sleep(2.0)
        self.torso.move_to(0.4)
        time.sleep(2.0)
        # self.fetch_arm.tuck()
        # time.sleep(2.0)
        # self.fetch_torso.lower()
