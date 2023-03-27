import time
from .tp_parameters import PICK_TABLE_POS, PLACE_TABLE_POS, PLACE_IDS, BLOCK_LOCATIONS
import copy
from math import pi
import numpy as np

YELLOW_HSV = cur_hsv = [0, 0, 100]
RED_HSV = [0, 100, 80]


def pickplace(robot_control, place_loc, place_num, blocks, pick_loc=None, pick_id=None, pick_col=None, returning=False, d_thrd_pick=0.7, d_thrd_place=0.76):
    # pick_id = blocks.color2id(pick_col, robot_con.markers.all_markers_by_distance)
    # imd, ids, minfo = is_marker_detected(robot_control.markers.get_markers_info(), pick_id)
    if pick_loc is None:
        pick_loc = BLOCK_LOCATIONS[pick_col]
    p1 = PICK_TABLE_POS[pick_loc]
    robot_control.fetch_base.goto(x=p1[0], y=p1[1], theta=p1[2])
    if returning:
        safety_light(stat=1)
    else:
        safety_light(stat=0)

    if not False:
        if pick_id is None:
            pick_id = blocks.color2id(pick_col, robot_control.markers.get_markers_info(mode=0, dtime=30), p1)
        imd, ids, minfo = is_marker_detected(robot_control.markers.get_markers_info(mode=0, dtime=30), pick_id)
        if not imd:
            turns, actual_pose = head_slow_sweep(robot_control, pi / 6)
            for i in turns:
                ctime = time.time()
                while time.time() - ctime < 1:
                    if pick_id < 0:
                        pick_id = blocks.color2id(pick_col, robot_control.markers.get_markers_info(mode=0, dtime=30), p1)
                    imd, ids, minfo = is_marker_detected(robot_control.markers.get_markers_info(mode=0, dtime=30), pick_id)
                    if imd:
                        break
                if not imd:
                    robot_control.fetch_head.move_head(i, 0.4)
                    time.sleep(0.1)

    if not imd:  # todo: what we can do for this case?
        return False

    p2 = near_table_loc(marker_info=minfo[pick_id][1], pick_pos=p1, dxy=0.1)
    robot_control.fetch_base.goto(x=p2[0], y=p2[1], theta=p2[2])
    dro = d_marker_robot(marker_info=minfo[pick_id][1], rob_pos=robot_control.fetch_base.get_pose(), theta=p2[2])
    while dro > d_thrd_pick:
        robot_control.fetch_base.move_forward(distance=dro - d_thrd_pick)
        dro = d_marker_robot(marker_info=minfo[pick_id][1], rob_pos=robot_control.fetch_base.get_pose(), theta=p2[2])
    time.sleep(0.5)
    robot_control.fetch_head.look_at(d_thrd_pick, 0.0, minfo[pick_id][0][2] - 0.3)
    time.sleep(0.5)

    while True:
        ctime = time.time()
        head_move_cnt = 0
        while time.time() - ctime < 8:
            cctime = time.time()
            while time.time() - cctime < 1:
                imd, ids, minfo = is_marker_detected(robot_control.markers.get_markers_info(mode=0, dtime=5), pick_id)
                if imd:
                    break
            if not imd:
                if head_move_cnt % 4 == 0 or head_move_cnt % 4 == 1:
                    robot_control.fetch_head.move_down(offset=0.15)
                elif head_move_cnt % 4 == 2 or head_move_cnt % 4 == 3:
                    robot_control.fetch_head.move_up(offset=0.15)
                head_move_cnt += 1
            else:
                break

        if not imd:
            if not returning:
                pick_id = blocks.color2id(pick_col, robot_control.markers.get_markers_info(mode=0, dtime=10), p2)
                print("near the table, couldn't find the object")
            else:
                print('cannot return')
                return False
        else:
            break

    pos_base = minfo[pick_id][0]
    pos_base[0] += 0.04
    robot_control.fetch_pick_place.pre_pick_h = 0.4
    robot_control.fetch_pick_place.post_pick_h = 0.15
    robot_control.fetch_pick_place.post_pick_x = 0.35
    robot_control.fetch_pick_place.pre_pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.1 + 0.05],
                                                   [0, pi / 2, pi / 2]]
    robot_control.fetch_pick_place.pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.0 + 0.05],
                                               [0, pi / 2, pi / 2]]
    robot_control.fetch_pick_place.post_pick_pos = [[pos_base[0], pos_base[1], pos_base[2] + 0.20 + 0.1 + 0.05],
                                                    [0, pi / 2, pi / 2]]
    robot_control.fetch_pick_place.pick()

    if returning:
        safety_light(stat=0)
    else:
        safety_light(stat=1)
    PLACE_ID = PLACE_IDS[place_loc]
    imdp, idsp, minfop = is_marker_detected(robot_control.markers.get_markers_info(mode=1, dtime=450), PLACE_ID[place_num])
    p3 = PLACE_TABLE_POS[place_loc]
    if not imdp:
        robot_control.fetch_base.goto(x=p3[0], y=p3[1], theta=p3[2])  # x=-2.57
        robot_control.fetch_base.move_forward(distance=0.1)
        time.sleep(1)
        imdp, idsp, minfop = is_marker_detected(robot_control.markers.get_markers_info(mode=0, dtime=20), PLACE_ID[place_num])

        if not imdp:
            ## robot sweeps its head to find the place location
            turns, actual_pose = head_slow_sweep(robot_control, pi / 4)
            for i in turns:
                ctime = time.time()
                while time.time() - ctime < 0.2:
                    imdp, idsp, minfop = is_marker_detected(robot_control.markers.get_markers_info(mode=0, dtime=20),
                                                            PLACE_ID[place_num])
                if imdp:
                    break
                else:
                    robot_control.fetch_head.move_head(i, 0.4)
                    time.sleep(0.1)
    if not imdp:  # todo: the robot doesn't release the object. this must be fixed
        return False

    p4 = near_table_loc(marker_info=minfop[PLACE_ID[place_num]][1], pick_pos=p3, dxy=0.1)
    robot_control.fetch_base.goto(x=p4[0], y=p4[1], theta=p4[2])
    dro = d_marker_robot(marker_info=minfop[PLACE_ID[place_num]][1], rob_pos=robot_control.fetch_base.get_pose(),
                         theta=p4[2])
    if dro > d_thrd_place:
        robot_control.fetch_base.move_forward(distance=dro - d_thrd_place)

    time.sleep(0.5)
    robot_control.fetch_head.look_at(d_thrd_place, 0.0, minfop[PLACE_ID[place_num]][0][2] - 0.3)
    time.sleep(0.5)

    ctime = time.time()
    head_move_cnt = 0
    while time.time() - ctime < 6:
        cctime = time.time()
        while time.time() - cctime < 0.5:
            imdp, idsp, minfop = is_marker_detected(robot_control.markers.get_markers_info(mode=0, dtime=20),
                                                    PLACE_ID[place_num])
            if imdp:
                break
        if not imdp:
            if head_move_cnt % 4 == 0 or head_move_cnt % 4 == 1:
                robot_control.fetch_head.move_down(offset=0.15)
            elif head_move_cnt % 4 == 2 or head_move_cnt % 4 == 3:
                robot_control.fetch_head.move_up(offset=0.15)
            head_move_cnt += 1
        else:
            break

    if not imdp:
        print("near the table, couldn't find the object")  # todo: this has to be fixed for the same reason
        return False

    ## robot places the object on the table
    place_pose = minfop[PLACE_ID[place_num]][0]
    place_pose[0] -= 0.02
    robot_control.fetch_pick_place.pre_place_h = 0.4
    if not returning:
        robot_control.fetch_pick_place.pre_place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.2 + 0.05],
                                                        [0, pi / 2, pi / 2]]
        robot_control.fetch_pick_place.place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.08],
                                                    [0, pi / 2, pi / 2]]  # + 0.20 + 0.1
        robot_control.fetch_pick_place.post_place_pos = [[place_pose[0], place_pose[1], place_pose[2] + 0.20 + 0.2 + 0.05],
                                                         [0, pi / 2, pi / 2]]
    else:
        robot_control.fetch_pick_place.pre_place_pos = [
            [place_pose[0]+0.2, place_pose[1] - 0.1, place_pose[2] + 0.25 + 0.2 + 0.05], [0, pi / 2, pi / 2]]
        robot_control.fetch_pick_place.place_pos = [
            [place_pose[0]+0.2, place_pose[1] - 0.1, place_pose[2] + 0.25 + 0.2 + 0.05], [0, pi / 2, pi / 2]]
        robot_control.fetch_pick_place.post_place_pos = [
            [place_pose[0]+0.2, place_pose[1] - 0.1, place_pose[2] + 0.25 + 0.2 + 0.05], [0, pi / 2, pi / 2]]

    robot_control.fetch_pick_place.post_place_h = 0.0
    robot_control.fetch_pick_place.post_place_x = 0.7
    robot_control.fetch_pick_place.place()
    safety_light(stat=0)


    if not imdp:
        return False

    return True


def safety_light(stat):
    if stat == 0:  # it's safe
        hsv = YELLOW_HSV
    if stat == 1:  # it's not safe
        hsv = RED_HSV
    with open("fetch_robot/lamp_stat.txt", "w") as f:
        for s in hsv:
            f.write(str(s) + "\n")


def near_table_loc(marker_info, pick_pos, dxy):
    if pick_pos[2] == pi / 2:
        pnew = [marker_info[0], pick_pos[1] + dxy, pick_pos[2]]
    elif pick_pos[2] == -pi / 2:
        pnew = [marker_info[0], pick_pos[1] - dxy, pick_pos[2]]
    elif pick_pos[2] == 0:
        pnew = [pick_pos[0] + dxy, marker_info[1], pick_pos[2]]
    elif pick_pos[2] == pi:
        pnew = [pick_pos[0] - dxy, marker_info[1], pick_pos[2]]
    else:
        print("Angle is not defined")
        return False
    return pnew


def d_marker_robot(marker_info, rob_pos, theta):
    if abs(theta) == pi / 2:
        dro = abs(marker_info[1] - rob_pos[1])
    elif theta == pi or theta == 0:
        dro = abs(marker_info[0] - rob_pos[0])
    else:
        print("Angle is not defined")
        return False
    return dro


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


def head_slow_sweep(robot_con, max_turn):
    max_turn = abs(max_turn)
    actual_pos = robot_con.fetch_head.get_pose()
    cur_pan = actual_pos[0]
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


if __name__ == '__main__':
    import rospy
    from tp_initialize_robot import RobotControl
    import tp_blocks

    rospy.init_node('test_code')
    robot_con = RobotControl()
    block_count = tp_blocks.Blocks()

    # a = pickplace(robot_control=robot_con, pick_col='o', blocks=block_count, pick_loc=1, place_loc=1, place_num=3)
    # a = pickplace(robot_control=robot_con, pick_col='o', blocks=block_count, pick_loc=1, place_loc=1, place_num=5)
    a = pickplace(robot_control=robot_con, place_loc=6, place_num=1, blocks=block_count, pick_loc=1, pick_id=86,
                  returning=True)
    # a = pickplace(robot_control=robot_con, pick_col='o', pick_loc=1, place_loc=1, place_num=1)
    # a = pickplace(robot_control=robot_con, pick_id=80, pick_loc=1, place_loc=1, place_num=4)
    # a = pickplace(robot_control=robot_con, pick_id=25, pick_loc=4, place_loc=1, place_num=3)
    # a = pickplace(robot_control=robot_con, pick_id=26, pick_loc=4, place_loc=1, place_num=2)
    print(a)

    # a = pickplace(robot_control=robot_con, pick_id=3, pick_loc=3, place_loc=1, place_num=4)
    # a = pickplace(robot_control=robot_con, pick_id=20, pick_loc=3, place_loc=1, place_num=5)
