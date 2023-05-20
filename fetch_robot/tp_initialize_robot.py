from .base_control import BaseControl
from .head_control import HeadControl
from .arm_control import ArmControl
from .torso_control import TorsoControl
from .gripper_control import GripperControl
from .fetch_detect_markers import Fetch_markers
from .pickplace import PickPlace
from speech_control import SpeechControl
import time



class RobotControl:
    def __init__(self):
        self.fetch_base = BaseControl()
        self.fetch_head = HeadControl()
        self.fetch_torso = TorsoControl()
        self.fetch_arm = ArmControl()
        self.fetch_voice = SpeechControl()
        self.fetch_gripper = GripperControl()
        self.fetch_pick_place = PickPlace()
        self.pick_place_ready()
        self.markers = Fetch_markers()
        self.markers.daemon = True
        self.markers.start()

    def pick_place_ready(self):
        if not self.fetch_arm.is_there(self.fetch_arm.stow_values):
            if not self.fetch_torso.is_there(0.4):
                self.fetch_torso.move_to(0.4, duration=2)
                time.sleep(2)
            self.fetch_arm.stow()
            time.sleep(2)

        if not self.fetch_torso.is_there(0.0):
            self.fetch_torso.move_to(0.0, duration=2)
            time.sleep(6)

    def reset_robot(self):
        if not self.fetch_arm.is_there(self.fetch_arm.stow_values):
            if not self.fetch_torso.is_there(0.4):
                self.fetch_torso.move_to(0.4, duration=2)
                time.sleep(2)
            self.fetch_arm.stow()
            time.sleep(2)

        if not self.fetch_torso.is_there(0.0):
            self.fetch_torso.move_to(0.0, duration=2)
            time.sleep(6)


if __name__ == '__main__':
    import rospy

    rospy.init_node("test_robot")
    robot_control = RobotControl()
    rospy.spin()
