import cv2
# import sys
import rospy
# from sensor_msgs.msg import Image
import rgbcamera
import aruco_markers as ar
from math import pi
import pickle
from aruco_utils import ARUCO_DICT
# import numpy as np
#
# from geometry_msgs.msg import PointStamped
#
# import tf2_py as tf2
# import tf2_ros
# from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud, transform_to_kdl


if __name__ == '__main__':

    ######################################## create charuco board ########################################
    # (1754, 1240)
    charuco_image, charuco_board = ar.gridboard_charuco_create(x_squares=7, y_squares=5, image_size=(3508, 2480),
                                                               dict_name="DICT_4X4_1000", square_length=0.0375,
                                                               marker_length=0.0325, padding_size=[5]*4)
    # 0.015,0.012
    # cv2.imshow('charuco', charuco_image)
    # cv2.imwrite("charuco_gridboard.jpg", charuco_image)
    # if cv2.waitKey() == 27:
    #     cv2.destroyAllWindows()
    ######################################################################################################


    ######################################### Camera Calibration #########################################
    rospy.init_node("test_cameras")
    rgb = rgbcamera.RGBCamera()
    # while True:
    #     isimage, image = rgb.read()
    #     if isimage:
    #         cv2.imshow("test", image)
    #         if cv2.waitKey(5) == 27:
    #             break
    #     else:
    #         print("waiting for the video")
    ar.camera_calibration_charuco(video=rgb, dict_name="DICT_4X4_1000", board=charuco_board, append_prev_calib=False)
    cv2.destroyAllWindows()
    ######################################################################################################
