import copy

import rospy
from base_control import BaseControl
from head_control import HeadControl
from pickplace import PickPlace
from arm_control import ArmControl
from torso_control import TorsoControl
import numpy as np
import time

from fetch_detect_markers import Fetch_markers
# from fetch_driver_msgs.msg import RobotState
import matplotlib.pyplot as plt

import server

pi = np.pi


# def cb(data):
#     global joint_effort
#     # print(data)
#     # print(data.joints)
#     a = data.joints
#     for ii in range(7):
#         joint_effort[a[ii + 5].name].append(a[ii + 5].effort)


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
    markers.daemon = True
    markers.start()
    pick_ids = [2]

    if not arm.is_there(arm.stow_values):
        if not torso.is_there(0.4):
            torso.move_to(0.4, duration=2)
            time.sleep(2)
        arm.stow()
        time.sleep(2)

    if not torso.is_there(0.0):
        torso.move_to(0.0, duration=2)
        time.sleep(6)

    while pick_ids and markers.is_alive():
        pick_id = pick_ids[0]
        if not markers.is_alive():
            break

        imd = False
        while not imd:
            imd, ids, minfo = is_marker_detected(markers.get_markers_info(), pick_id)

        print('heeey', minfo[pick_id][1][0])
        dro = abs(minfo[pick_id][1][1] - fetch_base.get_pose()[1])
        if dro > 0.7:
            fetch_base.move_forward(distance=dro - 0.7)

        time.sleep(2)
        fetch_head.look_at(0.7, 0.0, minfo[pick_id][0][2] - 0.3)
        time.sleep(1)

        ## robot detects the object position
        ctime = time.time()
        head_move_cnt = 0
        while time.time() - ctime < 6:
            cctime = time.time()
            while time.time() - cctime < 0.5:
                imd, ids, minfo = is_marker_detected(markers.get_markers_info(dtime=100), pick_id)
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
        print(imd)
        if imd:
            # robot picks up the object
            pos_base = minfo[pick_id][0]
            pos_base[0] += 0.03
            pick_place.pre_pick_h = 0.4
            pick_place.post_pick_h = 0.4
            pick_place.pre_pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.1 + 0.05], [0, pi / 2, pi/2]]
            pick_place.pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.0 + 0.05], [0, pi / 2, pi/2]]
            pick_place.post_pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.1 + 0.05],
                                        [0, pi / 2, pi / 2]]
            pick_place.pick()
            print('phaaaaasseeee 2')

            ## robot moves to the place location
            print('phaaaaasseeee 4')

            ## robot places the object on the table
            joint_val = {"shoulder_pan_joint": [], "shoulder_lift_joint": [],
                            "upperarm_roll_joint": [], "elbow_flex_joint": [],
                            "forearm_roll_joint": [], "wrist_flex_joint": [],
                            "wrist_roll_joint": []}
            # _sub = rospy.Subscriber("/robot_state", RobotState, cb)
            place_pose = pos_base
            pick_place.pre_place_h = 0.4
            pick_place.pre_place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.2],
                                        [0, pi / 2, pi / 2]]
            pick_place.place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.03],
                                    [0, pi / 2, pi / 2]]
            pick_place.post_place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.2],
                                         [0, pi / 2, pi / 2]]
            pick_place.post_place_h = 0.0
            pick_place.place(do_stow=True)
            # _sub.unregister()
            # fetch_arm.stow()
            # time.sleep(1)
            # fetch_torso.move_to(0, duration=2.0)
            print('phase 3')

        if pick_id is not None:
            pick_ids.remove(pick_id)

    plt.figure(1)
    for joint in pick_place.joint_effort:
        plt.plot(range(len(pick_place.joint_effort[joint])), pick_place.joint_effort[joint], label=joint)
    plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    plt.show()

    # lt = len(fetch_pick_place.curtime)
    # plt.figure(2)
    # for joint in fetch_pick_place.joint_velocity:
    #     ld = len(fetch_pick_place.joint_velocity[joint])
    #     plt.plot(fetch_pick_place.curtime, fetch_pick_place.joint_velocity[joint][ld-lt:], label=joint)
    # plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    # plt.show()
    #
    # lt = len(fetch_pick_place.curtime)
    # plt.figure(3)
    # for joint in fetch_pick_place.joint_dv:
    #     ld = len(fetch_pick_place.joint_dv[joint])
    #     plt.plot(fetch_pick_place.curtime, fetch_pick_place.joint_dv[joint][ld-lt:], label=joint)
    # plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    # plt.show()

    # ld = len(fetch_pick_place.joint_velocity["shoulder_lift_joint"])
    # plt.figure(4)
    # plt.plot(fetch_pick_place.curtime, fetch_pick_place.joint_velocity["shoulder_lift_joint"][ld-lt:], label="velocity")
    # plt.plot(fetch_pick_place.curtime, fetch_pick_place.desired_velocity["shoulder_lift_joint"][ld - lt:], label="dvelocity")
    # plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    # plt.show()
    #
    # ld = len(fetch_pick_place.joint_effort["shoulder_lift_joint"])
    # plt.figure(5)
    # plt.plot(fetch_pick_place.curtime, fetch_pick_place.joint_effort["shoulder_lift_joint"][ld-lt:], label="effort")
    # plt.plot(fetch_pick_place.curtime, fetch_pick_place.desired_effort["shoulder_lift_joint"][ld - lt:], label="desired")
    # plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    # plt.show()
    #
    # ld = len(fetch_pick_place.joint_position["shoulder_lift_joint"])
    # plt.figure(6)
    # plt.plot(fetch_pick_place.curtime, fetch_pick_place.joint_position["shoulder_lift_joint"][ld-lt:], label="position")
    # plt.plot(fetch_pick_place.curtime, fetch_pick_place.desired_position["shoulder_lift_joint"][ld - lt:], label="desired")
    # plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    # plt.show()




    # for xyz in fetch_pick_place.imu_vel_val:
    #     plt.plot(range(len(fetch_pick_place.imu_vel_val[xyz])), fetch_pick_place.imu_vel_val[xyz], label=xyz)
    # plt.legend(bbox_to_anchor=(0.98, 1), loc='upper left')
    # plt.show()
