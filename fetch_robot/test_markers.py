import cv2
# import colordetection
import aruco_markers as ar
from math import pi
import pickle

from aruco_utils import ARUCO_DICT

import rospy
from sensor_msgs.msg import Image

######################################## Color Detection ########################################
# a = colordetection.ColorDetection(image_filename='savedImage.jpg', text_filename='all_colors.csv', col_range=20)
# a.take_picture()
# a.define_colors()
# a.detect_color()
######################################################################################################

######################################## Create Aruco and gridboard ########################################
# img1 = ar.single_aruco_create(dict_name="DICT_4X4_50", id=5, side_pixel=100, border_bits=1)
img2, gridboard = ar.gridboard_aruco_create(n_markers_w=5, n_markers_h=4, dict_name="DICT_4X4_100",
                                            image_size=(1754, 1240), first_marker=0,
                                            marker_side=0.06, marker_separation=0.002, padding_size=[0, 0, 0, 0])

# cv2.imshow("single", img1)
# cv2.imshow("board", img2)
# cv2.imwrite("gridboard.jpg", img2)
# detected_markers_image, markers_data = ar.detect_aruco(source=0, dict_name="DICT_4X4_50",
#                                                        image_name="gridboard.jpg")
# cv2.imshow('Detected_Image', detected_markers_image)
######################################################################################################

######################################## create charuco board ########################################
# charuco_image, charuco_board = ar.gridboard_charuco_create(x_squares=11, y_squares=8, image_size=(1754, 1240),
#                                                            dict_name="DICT_5X5_1000", square_length=0.015,
#                                                            marker_length=0.012, padding_size=[0, 0, 0, 0])
# cv2.imshow('charuco', charuco_image)
# cv2.imwrite("charuco_gridboard.jpg", charuco_image)
# if cv2.waitKey() == 27:
#     cv2.destroyAllWindows()
######################################################################################################

######################################### Camera Calibration #########################################
# ar.camera_calibration_charuco(dict_name="DICT_5X5_1000", board=charuco_board, append_prev_calib=False)
######################################################################################################

######################################### Check Calibration Result #########################################
# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# cam_calib = pickle.load(open("calibration_output.pickle", "rb"))
#
# while True:
#     res, frame = vid.read()
#     img_undist = cv2.undistort(src=frame, cameraMatrix=cam_calib['cameraMatrix'],distCoeffs=cam_calib['distCoeffs'])
#     cv2.imshow("Raw image", frame)
#     cv2.imshow("Corrected image", img_undist)
#     if cv2.waitKey(1) == 27:
#         break
# vid.release()
# cv2.destroyAllWindows()
######################################################################################################

######################################### Detect Markers #########################################
# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# fps = vid.get(cv2.CAP_PROP_FPS)
# print(fps)
#
# aruco_params = cv2.aruco.DetectorParameters_create()
# aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_50"])
# while True:
#     res, frame = vid.read()
#     detected_markers_frame, markers_data = ar.detect_aruco(source=1, aruco_params=aruco_params,
#                                                            aruco_dict=aruco_dict, frame=frame,
#                                                            refine=True, board=gridboard)
#     cv2.imshow('Detected_Frame', detected_markers_frame)
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
#
# vid.release()
# cv2.destroyAllWindows()
######################################################################################################

######################################### Pose detection #########################################
# vid = cv2.VideoCapture(0)
# vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
# vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
# vid.set(cv2.CAP_PROP_AUTOFOCUS, 0)
# cam_calib = pickle.load(open("calibration_output.pickle", "rb"))
# aruco_params = cv2.aruco.DetectorParameters_create()
# aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_50"])
#
# while True:
#     res, frame = vid.read()
#     # img_undist = cv2.undistort(src=frame, cameraMatrix=cam_calib['cameraMatrix'], distCoeffs=cam_calib['distCoeffs'])
#     detected_markers_image, tvecs, rvecs = ar.aruco_position_estimate(frame=frame, aruco_dict=aruco_dict, aruco_params=aruco_params,
#                                                        board=gridboard, camera_calib=cam_calib, real_marker_size=0.016)
#     if tvecs is not None:
#         for nn, t in enumerate(tvecs):
#             r = rvecs[0]
#             if cv2.waitKey(1) & 0xFF == ord('p'):
#                 print('tx: {}, ty: {}, tz: {}'.format(t[0, 0], t[0, 1], t[0, 2]))
#                 print('rx: {}, ry: {}, rz: {}'.format(r[0, 0]*180/pi, r[0, 1]*180/pi, r[0, 2]*180/pi))
#
#     cv2.imshow("Detected", detected_markers_image)
#     if cv2.waitKey(1) == 27:
#         break
# vid.release()
# cv2.destroyAllWindows()
######################################################################################################
