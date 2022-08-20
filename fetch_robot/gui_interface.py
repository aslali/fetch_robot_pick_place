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

import os

from inspect import getmembers, isfunction
from moveit_python import MoveGroupInterface
import cv2

import pandas as pd

poses = pd.read_csv("robot_poses.csv")

# rospy.init_node('Performing_GUI')
import glob

task_list = glob.glob("tasks/*.txt")
for k, task in enumerate(task_list):
    task = task.split("/")[1].split(".")[0]
    task = "_".join(task.split("_")[:-2])
    task_list[k] = task

print(task_list)

# robot = Robot()

class MainGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setWindowTitle("Performing Gui")
        self.setGeometry(100, 100, 680, 800)

        # button_task = QtWidgets.QPushButton("Learn Task", self)
        # button_task.setGeometry(20, 75, 180, 40)
        # button_object = QtWidgets.QPushButton("Learn Object", self)
        # button_object.setGeometry(20, 125, 180, 40)
        # button_context.clicked.connect(lambda: learn_context())
        # button_task.clicked.connect(lambda: learn_task())
        # button_object.clicked.connect(lambda: learn_object())

        self.label_img_task = QtWidgets.QLabel(self)
        self.label_img_task.move(25, 25)
        self.label_img_task.resize(640, 480)

        self.cb = QtWidgets.QComboBox(self)
        self.cb.addItems(["--"] + task_list)
        self.cb.setGeometry(25, 520, 200, 40)
        self.cb.currentTextChanged.connect(self.cb_text_changed)

        button_perform = QtWidgets.QPushButton("Perform task", self)
        button_perform.setGeometry(300, 520, 180, 40)
        button_perform.clicked.connect(lambda: perform())

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(25, 600, 200, 40)

        button_bring = QtWidgets.QPushButton("Bring object", self)
        button_bring.setGeometry(300, 600, 180, 40)
        button_bring.clicked.connect(lambda: bring())

        button_clean = QtWidgets.QPushButton("Clean", self)
        button_clean.setGeometry(140, 680, 180, 40)
        button_clean.clicked.connect(lambda: clean())

        self.show()

        def perform():
            pass

        def bring():
            textboxValue = self.textbox.text()
            #robot.goto(x,y)

        def clean():
            pass


    def cb_text_changed(self, value):
        current_image_rgb = cv2.imread("tasks/" + value + "_rgb.png")#, cv2.IMREAD_RGB)
        current_image_rgb = cv2.cvtColor(current_image_rgb, cv2.COLOR_BGR2RGB)
        h, w, ch = current_image_rgb.shape
        bytesPerLine = ch * w
        convertToQtFormat = QImage(current_image_rgb.data, w, h, bytesPerLine, QImage.Format_RGB888)
        p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
        self.label_img_task.setPixmap(QPixmap.fromImage(p))


if __name__ == "__main__":

    App = QtWidgets.QApplication(sys.argv)
    App.setCursorFlashTime(100)
    App.setObjectName("tasks_gui")
    window2 = MainGui()

    sys.exit(App.exec_())
