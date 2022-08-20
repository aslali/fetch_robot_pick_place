import copy

import rospy
from base_control import BaseControl
from head_control import HeadControl
from pickplace import PickPlace
from arm_control import ArmControl
from torso_control import TorsoControl
import numpy as np
import time
import aruco_markers as ar
import pickle
import cv2
from aruco_utils import ARUCO_DICT
import rgbcamera
import fetch_utils as fu
from fetch_detect_markers import Fetch_markers

pi = np.pi


def head_slow_sweep(max_turn):
    max_turn = abs(max_turn)
    actual_pos = fetch_head.get_pose()
    cur_pan = fetch_head.actual_positions[0]
    trn_right = np.abs(-max_turn - cur_pan)
    trn_left = np.abs(max_turn - cur_pan)
    turn_dir = np.argmin([trn_right, trn_left])
    if turn_dir == 0:
        rights = np.arange(cur_pan, -max_turn - 0.2, -0.2).tolist()
        lefts = np.arange(-max_turn, max_turn + 0.2, 0.2).tolist()
        turns = rights + lefts
    else:
        lefts = np.arange(cur_pan, max_turn, 0.2).tolist()
        rights = np.arange(max_turn, -max_turn, -0.2).tolist()
        turns = lefts + rights
    return turns, actual_pos


def is_marker_detected(detected, wanted):
    detected_ids = []
    is_detected = False
    if type(wanted) is list:
        for i in wanted:
            if i in detected:
                detected_ids.append(i)
        if detected_ids:
            is_detected = True
    else:
        if wanted in detected:
            detected_ids = wanted
            is_detected = True
    prev_detected = copy.copy(detected)
    return is_detected, detected_ids, prev_detected


if __name__ == '__main__':
    rospy.init_node("test_base")
    fetch_base = BaseControl()
    fetch_head = HeadControl()
    pick_place = PickPlace()
    torso = TorsoControl()
    arm = ArmControl()
    markers = Fetch_markers()
    markers.start()
    pick_ids = [2]




    if not torso.is_there(0.0):
        torso.move_to(0.0, duration=2)
        time.sleep(6)

    for pick_id in pick_ids:
        ## robot goes toward the pick-up table
        fetch_base.goto(x=-0.29, y=0.533, theta=pi/6)
        print(fetch_base.get_pose())
        time.sleep(2)
        ## robot sweep its head to find the objects
        turns, actual_pose = head_slow_sweep(pi / 4)
        for i in turns:
            ctime = time.time()
            while time.time() - ctime < 0.2:
                imd, ids, minfo = is_marker_detected(markers.all_markers, pick_id)
            print(imd)
            if imd:
                break
            else:
                fetch_head.move_head(i, 0.4)
                time.sleep(0.1)
        ## robot moves toward the object
        print(minfo[pick_id][1][0])
        print(minfo[pick_id][0])
        print('before: ', fetch_base.get_pose())
        fetch_base.goto(minfo[pick_id][1][0], y=3.55, theta=pi/6)
        print('after: ', fetch_base.get_pose())
        time.sleep(2)
        ## robot keep looking at the object
        fetch_head.look_at(minfo[pick_id][0][0] - 0.65, 0.05, minfo[pick_id][0][2] - 0.05)
        time.sleep(8)

        ## robot detects the object position
        ctime = time.time()
        while time.time() - ctime < 0.5:
            imd, ids, minfo = is_marker_detected(markers.all_markers, pick_id)
            if imd:
                break

        # if raw_input('Good to go?') == 'y':
        #     fetch_base.move_backward(second=3)
        #     print(imd)



