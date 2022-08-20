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
    pick_ids = [1, 2]
    place_ids = {1: 3, 2: 0}

    if not arm.is_there(arm.stow_values):
        if not torso.is_there(0.4):
            torso.move_to(0.4, duration=2)
            time.sleep(2)
        arm.stow()
        time.sleep(2)

    if not torso.is_there(0.0):
        torso.move_to(0.0, duration=2)
        time.sleep(6)

    for pick_id in pick_ids:
        ## robot goes toward the pick-up table
        fetch_base.goto(x=-4.9, y=-0.56, theta=-pi / 2)
        time.sleep(2)
        ## robot sweep its head to find the objects
        turns, actual_pose = head_slow_sweep(pi / 5)
        for i in turns:
            ctime = time.time()
            while time.time() - ctime < 1:
                imd, ids, minfo = is_marker_detected(markers.get_markers_info(), pick_id)
                if imd:
                    break
            print(imd)
            if not imd:
                fetch_head.move_head(i, 0.4)
                time.sleep(0.1)
        ## robot moves toward the object
        print('heeey', minfo[pick_id][1][0])
        fetch_base.goto(minfo[pick_id][1][0], y=-1.2, theta=-pi / 2)
        dro = abs(minfo[pick_id][1][1] - fetch_base.get_pose()[1])
        if dro > 0.7:
            fetch_base.move_forward(distance=dro - 0.7)

        time.sleep(2)
        ## robot keep looking at the object
        # fetch_head.look_at(minfo[pick_id][0][0] - 0.74, 0.0, minfo[pick_id][0][2] - 0.12)
        fetch_head.look_at(0.7, 0.0, minfo[pick_id][0][2] - 0.3)
        time.sleep(1)

        ## robot detects the object position
        ctime = time.time()
        head_move_cnt = 0
        while time.time() - ctime < 6:
            cctime = time.time()
            while time.time() - cctime < 0.5:
                imd, ids, minfo = is_marker_detected(markers.get_markers_info(dtime=3), pick_id)
                if imd:
                    break
            if not imd:
                if head_move_cnt % 4 == 0 or head_move_cnt % 4 == 1:
                    fetch_head.move_down(offset=0.15)
                elif head_move_cnt % 4 == 2 or head_move_cnt % 4 == 3:
                    fetch_head.move_up(offset=0.15)
                head_move_cnt += 1
            else:
                break


        if imd:
            # robot picks up the object
            pos_base = minfo[pick_id][0]
            pos_base[0] += 0.0
            pick_place.pre_pick_h = 0.4
            pick_place.post_pick_h = 0.0
            pick_place.pre_pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.1+0.05], [0, pi / 2, pi / 2]]
            pick_place.pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.0+0.07], [0, pi / 2, pi / 2]]
            pick_place.post_pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.1+0.05], [0, pi / 2, pi / 2]]
            pick_place.pick()
            print('phaaaaasseeee 2')
            fetch_base.move_backward(second=3)

            ## robot moves to the place location
            print('phaaaaasseeee 4')
            fetch_base.goto(x=-2.57, y=0.14, theta=0)
            # print(fetch_base.get_pose())
            time.sleep(2)
            print('phaaaaasseeee 5')
            ## robot sweeps its head to find the place location
            turns, actual_pose = head_slow_sweep(pi / 4)
            for i in turns:
                ctime = time.time()
                while time.time() - ctime < 0.2:
                    imdp, idsp, minfop = is_marker_detected(markers.get_markers_info(), place_ids[pick_id])
                print(imdp)
                if imdp:
                    break
                else:
                    fetch_head.move_head(i, 0.75)
                    time.sleep(0.1)
            if imdp:
                print('phase 3')
            ## robot places the object on the table
                place_pose = minfop[place_ids[pick_id]][0]
                pick_place.pre_place_h = 0.4
                pick_place.pre_place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.2+0.05], [0, pi / 2, pi / 2]]
                pick_place.place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.12+0.02], [0, pi / 2, pi / 2]]
                pick_place.post_place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.2 + 0.05], [0, pi / 2, pi / 2]]
                pick_place.post_place_h = 0.0
                pick_place.place()
                print('phase 3')
                fetch_base.move_backward(distance=0.5)
