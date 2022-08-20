# rosrun tf static_transform_publisher 0 0 0 0 0 0 map odom 100
# rosrun map_server map_server /home/fetch/map_directory/5427_map.yaml
# roslaunch fetch_moveit_config move_group.launch

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import roslib
import rospy
import rviz
import sys
from math import pi
import geometry_msgs.msg
import moveit_commander
from robot import Robot

from inspect import getmembers, isfunction
from moveit_python import MoveGroupInterface
import cv2
import thread


rospy.init_node('interface_control')
# pub_cmd_vel = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
# moveit_commander.roscpp_initialize(sys.argv)
# robot = moveit_commander.RobotCommander()
# move_group = MoveGroupInterface("arm_with_torso", "base_link", "gripper")

joint_range = { "head_pan": [-90, 90], "head_tilt": [-45, 90], "torso_lift": [0, 400],
                "shoulder_pan": [-92, 92], "shoulder_lift": [-70, 87],
                "upperarm_roll": [-360, 360], "elbow_flex": [-129, 129],
                "forearm_roll": [-360, 360], "wrist_flex": [-125, 125],
                "wrist_roll": [-360, 360], "gripper": [0, 10]}

joint_names = [ "head_pan", "head_tilt", "torso_lift",
                "shoulder_pan", "shoulder_lift",
                "upperarm_roll", "elbow_flex",
                "forearm_roll", "wrist_flex",
                "wrist_roll", "gripper"] #"head_pan_joint", "head_tilt_joint", , "gripper_joint"

# print(dir(move_group))

robot = Robot()

pose = [0.104505419731, 0.0519565418363, 0.1, 1.32, 1.40, -0.2, 1.72, 0.0, 1.66, 0.0, 0.0]

class RVizGui(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.frame = rviz.VisualizationFrame()
        self.frame.initialize()
        reader = rviz.YamlConfigReader()
        config = rviz.Config()
        reader.readFile(config, "/home/fetch/Documents/rviz_interface_gui/fetch.rviz")
        self.frame.load(config)
        # self.frame.setMenuBar(None)
        self.frame.setStatusBar(None)
        self.frame.setHideButtonVisibility(False)

        self.manager = self.frame.getManager()
        print(dir(self.manager))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.frame)
        self.setWindowTitle("Fetch rViz")
        self.setGeometry(100, 100, 600, 900)
        self.setLayout(layout)
        self.show()

    def mousePressEvent(self, e):
        print(self.manager.objectName())

class ControlGui(QtWidgets.QMainWindow):
    def __init__(self):
        super(QtWidgets.QMainWindow, self).__init__()
        self.setWindowTitle("Control Gui")
        self.setGeometry(100, 100, 500, 400)
        buttonF = QtWidgets.QPushButton("Forward", self)
        buttonF.setGeometry(100, 25, 90, 40)
        buttonB = QtWidgets.QPushButton("Backward", self)
        buttonB.setGeometry(100, 75, 90, 40)
        buttonL = QtWidgets.QPushButton("Left", self)
        buttonL.setGeometry(100, 125, 90, 40)
        buttonR = QtWidgets.QPushButton("Right", self)
        buttonR.setGeometry(100, 175, 90, 40)
        buttonF.clicked.connect(lambda: forward())
        buttonB.clicked.connect(lambda: backward())
        buttonL.clicked.connect(lambda: left())
        buttonR.clicked.connect(lambda: right())

        self.cb = QtWidgets.QComboBox(self)
        self.cb.addItems([  "head_pan", "head_tilt", "torso_lift", "shoulder_pan",
                            "shoulder_lift", "upperarm_roll", "elbow_flex",
                            "forearm_roll", "wrist_flex", "wrist_roll", "gripper"])
        self.cb.setGeometry(250, 25, 100, 40)
        self.cb.currentTextChanged.connect(self.selectedJoint)
        self.sld = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.sld.setRange(0, 25)
        self.sld.setFocusPolicy(QtCore.Qt.NoFocus)
        self.sld.setPageStep(2)
        self.sld.setGeometry(250, 75, 100, 40)
        self.sld.valueChanged.connect(self.updateJoint)
        self.label = QtWidgets.QLabel('0', self)
        self.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.label.setMinimumWidth(80)
        self.label.setGeometry(400, 75, 80, 40)
        buttonT = QtWidgets.QPushButton("Tuck", self)
        buttonT.setGeometry(250, 125, 90, 40)
        buttonT.clicked.connect(lambda: tuck())
        buttonT = QtWidgets.QPushButton("Zero", self)
        buttonT.setGeometry(250, 175, 90, 40)
        buttonT.clicked.connect(lambda: zero())
        self.buttonP = QtWidgets.QPushButton("Start perception", self)
        self.buttonP.setGeometry(250, 225, 140, 40)
        self.buttonP.clicked.connect(lambda: perception())

        def forward():
            robot.base.move_forward(1.0)
        def backward():
            robot.base.move_backward(1.0)
        def left():
            robot.base.turn_left(1.0)
        def right():
            robot.base.turn_right(1.0)
        def tuck():
            robot.arm.tuck()
        def zero():
            robot.arm.zero()
            robot.torso.move_to(0.0)
            robot.head.move_home()
            robot.gripper.open()
        def perception():
            if robot.perception.pause[0]:
                rospy.loginfo("Starting perception")
                self.buttonP.setText("Stop perception")
            else:
                rospy.loginfo("Pausing perception")
                self.buttonP.setText("Start perception")
            robot.perception.pause[0] = not robot.perception.pause[0]
        self.show()

    def updateJoint(self, value):
        self.label.setText(str(value))
        joint_name = joint_names[self.cb.currentIndex()]
        pose[self.cb.currentIndex()] = value * 2 * pi / 180.0
        if "head" in joint_name:
       	    robot.head.move_head(pose[0], pose[1])
        elif "fetch_torso" in joint_name:
            robot.torso.move_to(value / 100.)
            pose[self.cb.currentIndex()] = value / 100.0
        elif "gripper" in joint_name:
            robot.gripper.close(value / 100.0)
            pose[self.cb.currentIndex()] = value / 100.0
        else:
       	    robot.arm.move_joint_position(joint_name + "_joint", value * 2 * pi / 180.0)
        # move_group.moveToJointPosition(joint_names, pose, 0.02, wait=False, max_velocity_scaling_factor=0.6)

    def selectedJoint(self, value):
        self.sld.setRange(joint_range[value][0], joint_range[value][1])
        state = robot.getRobotState()[1]
        if value == "torso_lift":
            self.sld.setValue(state[2]*100)
        elif value == "head_pan":
            self.sld.setValue(state[4] * 180 / (2*pi))
        elif value == "head_tilt":
            self.sld.setValue(state[5] * 180 / (2*pi))
        elif value == "gripper":
            self.sld.setValue((state[13] + state[14])*100)
        else:
            self.sld.setValue(state[joint_names.index(value) + 3] * 180 / (2*pi))

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        while True:
            rgbImage = robot.getDetectionImage()
            rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

class ImageGUI(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        objs = robot.perception.get_graspable_objects()
        self.label_objs.setText("Detected objects:\n" + "\n".join(objs))
        self.label_img.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle("RGB camera")
        self.setGeometry(100, 100, 100, 100)
        self.resize(800, 480)
        # create a label
        self.label_img = QtWidgets.QLabel(self)
        self.label_img.move(0, 0)
        self.label_img.resize(640, 480)
        self.label_img.mousePressEvent = self.mousePressEvent

        self.label_objs = QtWidgets.QLabel(self)
        self.label_objs.move(650, 0)
        self.label_objs.setText("Detected objects:\n")
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x, y = event.x(), event.y()
            object_name = robot.yoloDetector.clicked(x, y)
            print("Picking up ", object_name)
            obj = robot.perception.get_object(object_name)
            # robot.pickplace.pick(obj)

if __name__ == "__main__":
    # thread = thread.start_new_thread(display_image, ())

    App = QtWidgets.QApplication(sys.argv)
    App.setCursorFlashTime(100)
    App.setObjectName("rViz")
    # window = RVizGui()
    window2 = ControlGui()
    window3 = ImageGUI()


    sys.exit(App.exec_())
