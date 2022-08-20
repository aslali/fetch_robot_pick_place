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

from groceryreminder import printing_func, get_breakfast,get_creative_breakfast
from pick_place import picking_func
import numpy as np

poses = pd.read_csv("robot_poses.csv")

rospy.init_node('Learning_GUI')

robot = Robot()
current_image_rgb, current_image_yolo = None, None

class ContextGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setWindowTitle("Learning Breakfast")
        self.setGeometry(100, 100, 300, 130)
        button_save = QtWidgets.QPushButton("Save", self)
        button_save.setGeometry(170, 60, 90, 40)
        button_save.clicked.connect(lambda: self.save())

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(25, 25, 180, 40)
        self.label.setText("Breakfast name:\n")

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(25, 60, 120, 40)

    @pyqtSlot()
    def save(self):
        # path = 'contexts/'
        # textboxValue = self.textbox.text()
        # cv2.imwrite(path + textboxValue + "_rgb.png", cv2.cvtColor(current_image_rgb, cv2.COLOR_RGB2BGR)) #robot.getRGBImage()
        # cv2.imwrite(path + textboxValue + "_yolo.png", current_image_yolo)
        # f = open(path + textboxValue + "_bounding_boxes.txt", "w")
        # for k, box in enumerate(robot.yoloDetector.boxes):
        #    obj, _ = robot.perception.get_object(robot.yoloDetector.class_names[k])
        #    if obj:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n", obj.object.primitive_poses[0].position.x, obj.object.primitive_poses[0].position.y, obj.object.primitive_poses[0].position.z)
        #    else:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n")
        #
        QtWidgets.QMessageBox.question(self, 'Message - pythonspot.com', 'Breakfast successfully saved', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        self.close()


class BreakfastGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setWindowTitle("Bring Breakfast")
        self.setGeometry(100, 100, 300, 130)
        button_save = QtWidgets.QPushButton("Bring it", self)
        button_save.setGeometry(170, 60, 90, 40)
        button_save.clicked.connect(lambda: self.save())

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(25, 25, 180, 40)
        self.label.setText("Breakfast name:\n")

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(25, 60, 120, 40)

    @pyqtSlot()
    def save(self):
        textboxValue = self.textbox.text()
        get_breakfast(textboxValue)
        # path = 'contexts/'
        # textboxValue = self.textbox.text()
        # cv2.imwrite(path + textboxValue + "_rgb.png", cv2.cvtColor(current_image_rgb, cv2.COLOR_RGB2BGR)) #robot.getRGBImage()
        # cv2.imwrite(path + textboxValue + "_yolo.png", current_image_yolo)
        # f = open(path + textboxValue + "_bounding_boxes.txt", "w")
        # for k, box in enumerate(robot.yoloDetector.boxes):
        #    obj, _ = robot.perception.get_object(robot.yoloDetector.class_names[k])
        #    if obj:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n", obj.object.primitive_poses[0].position.x, obj.object.primitive_poses[0].position.y, obj.object.primitive_poses[0].position.z)
        #    else:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n")
        #
        QtWidgets.QMessageBox.question(self, 'Message - pythonspot.com', 'Breakfast successfully saved', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        self.close()

"""
class TaskGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setWindowTitle("Learning Task")
        self.setGeometry(100, 100, 300, 130)
        button_save = QtWidgets.QPushButton("Save", self)
        button_save.setGeometry(170, 60, 90, 40)
        button_save.clicked.connect(lambda: self.save())

        self.label = QtWidgets.QLabel(self)
        self.label.move(25, 25)
        self.label.setText("Task name:\n")

        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setGeometry(25, 60, 120, 40)

    @pyqtSlot()
    def save(self):
        # path = "tasks/"
        # textboxValue = self.textbox.text()
        # cv2.imwrite(path + textboxValue + "_rgb.png", cv2.cvtColor(current_image_rgb, cv2.COLOR_RGB2BGR)) #robot.getRGBImage()
        # cv2.imwrite(path + textboxValue + "_yolo.png", current_image_yolo)
        # f = open(path + textboxValue + "_bounding_boxes.txt", "w")
        # for k, box in enumerate(robot.yoloDetector.boxes):
        #    obj, _ = robot.perception.get_object(robot.yoloDetector.class_names[k])
        #    if obj:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n", obj.object.primitive_poses[0].position.x, obj.object.primitive_poses[0].position.y, obj.object.primitive_poses[0].position.z)
        #    else:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n")
        #
        QtWidgets.QMessageBox.question(self, 'Message - pythonspot.com', 'Task successfully saved', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        self.close()
"""
"""
class ObjectGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setWindowTitle("Learning Object")
        self.setGeometry(100, 100, 500, 300)

        # self.label_robot = QtWidgets.QLabel(self)
        # self.label_robot.move(25, 25)
        # self.label_robot.setGeometry(25, 25, 200, 30)
        # self.label_robot.setText("Number of robot positions:\n")
        # self.textbox_robot = QtWidgets.QLineEdit(self)
        # self.textbox_robot.setGeometry(25, 55, 120, 40)
        #
        # self.label_pic = QtWidgets.QLabel(self)
        # self.label_pic.move(210, 25)
        # self.label_pic.setGeometry(210, 25, 200, 30)
        # self.label_pic.setText("Number of pictures to be taken:\n")
        # self.textbox_pic = QtWidgets.QLineEdit(self)
        # self.textbox_pic.setGeometry(210, 55, 120, 40)
        #
        # self.button_apply = QtWidgets.QPushButton("Apply", self)
        # self.button_apply.setGeometry(390, 55, 90, 40)
        # self.button_apply.clicked.connect(lambda: self.apply())
        self.nb_robot_pose = 0
        # self.nb_pictures = 0
        self.it_robot_pose = 0
        self.it_pictures = 0
        self.incr = 0

        self.label_iter = QtWidgets.QLabel(self)
        self.label_iter.setGeometry(25, 30, 180, 30)
        self.label_iter.setText("Robot pose: 0 out of " + str(self.nb_robot_pose) + "\nPictures taken: 0")
#        self.label_iter.setVisible(False)

        self.label_label = QtWidgets.QLabel(self)
        self.label_label.setGeometry(210, 25, 180, 30)
        self.label_label.setText("Object name:")
        self.textbox_label = QtWidgets.QLineEdit(self)
        self.textbox_label.setGeometry(210, 55, 120, 40)

        self.button_save = QtWidgets.QPushButton("Save", self)
        self.button_save.setGeometry(25, 150, 80, 40)
        self.button_save.clicked.connect(lambda: self.save())
#        self.button_save.setVisible(False)

        self.button_next = QtWidgets.QPushButton("Go to next pose", self)
        self.button_next.setGeometry(210, 150, 130, 40)
        self.button_next.clicked.connect(lambda: self.next())
#        self.button_next.setVisible(False)

        self.button_end = QtWidgets.QPushButton("End", self)
        self.button_end.setGeometry(25, 250, 90, 40)
        self.button_end.clicked.connect(lambda: self.end())
        robot.perception.pause[0] = False
        robot.fetch_torso.move_to(poses["torso_lift"][self.it_robot_pose])
        robot.head.move_head(0.0, poses["head_tilt"][self.it_robot_pose])

    @pyqtSlot()
    def next(self):
        self.it_robot_pose += 1
        self.it_pictures = 0
        self.label_iter.setText("Robot pose: " + str(self.it_robot_pose) + " out of 10" + "\nPictures taken: " + str(self.it_pictures))
        #Robot goes to pose i
        robot.fetch_torso.move_to(poses["torso_lift"][self.it_robot_pose])
        robot.head.move_head(0.0, poses["head_tilt"][self.it_robot_pose])
        if self.it_robot_pose == 10:
            self.button_next.setDisabled(True)

    @pyqtSlot()
    def save(self):
        # path = "data/"
        # textboxValue = self.textbox_label.text()
        # if not os.path.isdir(path + textboxValue):
        #     os.mkdir(path + textboxValue)
        # filename = textboxValue + "_" + str(self.it_robot_pose) +  "_" + str(self.it_pictures)
        # cv2.imwrite(path + textboxValue + "/" + filename + "_rgb.png", cv2.cvtColor(current_image_rgb, cv2.COLOR_RGB2BGR)) #robot.getRGBImage()
        # cv2.imwrite(path + textboxValue + "/" + filename + "_yolo.png", cv2.cvtColor(current_image_yolo, cv2.COLOR_RGB2BGR))
        # f = open(path + textboxValue + "/" + filename + "_bounding_boxes.txt", "w")
        # for k, box in enumerate(robot.yoloDetector.boxes):
        #    obj, _ = robot.perception.get_object(robot.yoloDetector.class_names[k])
        #    if obj:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "," + str(obj.primitive_poses[0].position.x) + "," + str(obj.primitive_poses[0].position.y) + "," + str(obj.primitive_poses[0].position.z) + "\n")
        #    else:
        #        f.write(robot.yoloDetector.class_names[k] + "," + ",".join([str(b) for b in box]) + "\n")

        self.it_pictures += 1
        self.label_iter.setText("Robot pose: " + str(self.it_robot_pose) + " out of 10" + "\nPictures taken: " + str(self.it_pictures))
        #save current image + label

    @pyqtSlot()
    def end(self):
        robot.perception.pause[0] = True
        self.close()
"""
class MainGui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.setWindowTitle("Learning Gui")
        self.setGeometry(100, 100, 700, 1000)
        button_context = QtWidgets.QPushButton("Learn Special Context", self)
        button_context.setGeometry(20, 25, 180, 40)
        button_task = QtWidgets.QPushButton("Learn Task", self)
        button_task.setGeometry(20, 75, 180, 40)
        button_object = QtWidgets.QPushButton("Learn Object", self)
        button_object.setGeometry(20, 125, 180, 40)
        button_context.clicked.connect(lambda: learn_context())
        button_task.clicked.connect(lambda: learn_task())
        button_object.clicked.connect(lambda: learn_object())

        def learn_context():
            ContextGUI(self).show()
        def learn_task():
            TaskGUI(self).show()
        def learn_object():
            ObjectGUI(self).show()
        self.show()

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)
    cap = cv2.VideoCapture(0)

    def run(self):
        while True:
            global current_image_rgb, current_image_yolo
            current_image_rgb = robot.getRGBImage()
            current_image_yolo = robot.getDetectionImage()
            # current_image_rgb = cv2.cvtColor(current_image_rgb, cv2.COLOR_BGR2RGB)
            current_image_yolo = cv2.cvtColor(current_image_yolo, cv2.COLOR_BGR2RGB)
            h, w, ch = current_image_rgb.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(current_image_yolo.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

class ImageGUI(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget, self).__init__()
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        objs = robot.perception.get_graspable_objects()
        # self.label_objs.setText("Grocery List:\n" + "\n".join(objs))
        self.label_img.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot()
    def save(self):
        my_creative_breakfast = get_creative_breakfast()
        print (my_creative_breakfast)
        #for i in range(0,len(my_creative_breakfast)):
        #    picking_func(my_creative_breakfast[i])

        #textboxValue = self.textbox.text()
        #get_breakfast(textboxValue)
        #QtWidgets.QMessageBox.question(self, 'Message - pythonspot.com', 'Breakfast successfully saved', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        #self.close()

    def initUI(self):
        self.setWindowTitle("RGB camera")
        self.setGeometry(100, 100, 900, 700)
        # self.resize(1200, 480)
        # create a label
        self.label_img = QtWidgets.QLabel(self)
        self.label_img.setGeometry(220, 0, 640, 480)
        self.label_img.mousePressEvent = self.mousePressEvent

        button_context = QtWidgets.QPushButton("Learn Breakfast", self)
        button_context.setGeometry(20, 25, 180, 40)
        button_get = QtWidgets.QPushButton("Get Breakfast", self)
        button_get.setGeometry(20, 75, 180, 40)
        button_upload = QtWidgets.QPushButton("Surprise Me!", self)
        button_upload.setGeometry(20, 125, 180, 40)
        button_up = QtWidgets.QPushButton("Forward", self)
        button_up.setGeometry(435, 500, 180, 40)
        button_down = QtWidgets.QPushButton("Backward", self)
        button_down.setGeometry(435, 600, 180, 40)
        button_left = QtWidgets.QPushButton("Left", self)
        button_left.setGeometry(310, 550, 180, 40)
        button_right = QtWidgets.QPushButton("Right", self)
        button_right.setGeometry(555, 550, 180, 40)
        button_context.clicked.connect(lambda: learn_context())
        button_get.clicked.connect(lambda: get_list())
        #button_upload.clicked.connect(lambda: upload_list())
        button_upload.clicked.connect(lambda: self.save())
        button_up.clicked.connect(lambda: robot.base.move_forward())
        button_down.clicked.connect(lambda: robot.base.move_backward())
        button_left.clicked.connect(lambda: robot.base.turn_left())
        button_right.clicked.connect(lambda: robot.base.turn_right())

        def learn_context():
            ContextGUI(self).show()
        def get_list():
            BreakfastGUI(self).show()
        def upload_list():
            pass
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

    App = QtWidgets.QApplication(sys.argv)
    App.setCursorFlashTime(100)
    App.setObjectName("rViz")
#    window2 = MainGui()
    window3 = ImageGUI()

    sys.exit(App.exec_())
