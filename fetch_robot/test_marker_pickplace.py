import time

import cv2
# import sys
import rospy
# from sensor_msgs.msg import Image
import rgbcamera
import aruco_markers as ar
from math import pi
import pickle
from aruco_utils import ARUCO_DICT
import fetch_utils as fu
from pickplace import PickPlace
import torso_control
import arm_control

if __name__ == '__main__':

    img2, gridboard = ar.gridboard_aruco_create(n_markers_w=7, n_markers_h=5, dict_name="DICT_4X4_100",
                                                image_size=(1754, 1240),
                                                marker_side=0.029, marker_separation=0.01, padding_size=[5, 5, 0, 0])
    cam_calib = pickle.load(open("calibration_output.pickle", "rb"))
    aruco_params = cv2.aruco.DetectorParameters_create()
    aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_100"])

    rospy.init_node("test_pickplace")
    rgb = rgbcamera.RGBCamera()
    pick_place = PickPlace()
    torso = torso_control.TorsoControl()
    arm = arm_control.ArmControl()

    if not arm.is_there(arm.stow_values):
        if not torso.is_there(0.4):
            torso.move_to(0.4, duration=2)
            time.sleep(2)
        arm.stow()
        time.sleep(2)

    if not torso.is_there(0.0):
        torso.move_to(0.0, duration=2)
        time.sleep(6)
    print("phase 1")
    markers_is = [28, 21]
    while markers_is:
        ret, frame = rgb.read()
        if ret:
            detected_markers_image, tvecs, rvecs, ids = ar.aruco_position_estimate(frame=frame, aruco_dict=aruco_dict,
                                                                              aruco_params=aruco_params,
                                                                              board=gridboard, camera_calib=cam_calib,
                                                                              real_marker_size=0.029)
            if tvecs is not None:
                for nn, t in enumerate(tvecs):
                    if ids[nn] in markers_is:
                        r = rvecs[0]
                        # if cv2.waitKey(1) & 0xFF == ord('p'):
                        print('tx: {}, ty: {}, tz: {}'.format(t[0, 0], t[0, 1], t[0, 2]))
                        print(
                            'rx: {}, ry: {}, rz: {}'.format(r[0, 0] * 180 / pi, r[0, 1] * 180 / pi, r[0, 2] * 180 / pi))
                        pos_base = fu.aruco_to_base_link(marker_pos=[t[0, 0], t[0, 1], t[0, 2]], frame_id=rgb.rgb_frame,
                                                         frame_trans=rgb.trans_rgb_base)
                        pos_base[0] += 0.01
                        print(pos_base)
                        # if raw_input('pickup') != 'n':
                        pick_place.pre_pick_h = 0.4
                        pick_place.post_pick_h = 0.4
                        pick_place.pre_pick_pos = [[pos_base[0], pos_base[1], pos_base[2]+0.20 + 0.1], [0, pi/2, 0]]
                        pick_place.pick_pos = [[pos_base[0], pos_base[1], pos_base[2]+0.20 + 0.0], [0, pi/2, 0]]
                        pick_place.post_pick_pos = [[pos_base[0], pos_base[1], pos_base[2]+0.20 + 0.1], [0, pi/2, 0]]
                        pick_place.pick()
                        print('phaaaaasseeee 2')
                        # fetch_pick_place.reset_pos()

                        # if raw_input('place') != 'n':
                        pick_place.pre_place_h = 0.4
                        pick_place.pre_place_pos = [[pos_base[0], pos_base[1], pos_base[2]+0.20 + 0.1], [0, pi/2, 0]]
                        pick_place.place_pos = [[pos_base[0], pos_base[1], pos_base[2]+0.20 + 0.02], [0, pi/2, 0]]
                        pick_place.post_place_pos = [[pos_base[0], pos_base[1], pos_base[2]+0.20 + 0.1], [0, pi/2, 0]]
                        pick_place.post_place_h = 0.0
                        pick_place.place()
                        print('phase 3')
                            # fetch_pick_place.reset_pos()

                        markers_is.remove(ids[nn])

            cv2.imshow("Detected", detected_markers_image)
        else:
            print("waiting for the video")
        if cv2.waitKey(3) == 27:
            break

    cv2.destroyAllWindows()
