import copy
import time

import cv2
# import sys
import numpy as np
import rospy
# from sensor_msgs.msg import Image
import rgbcamera
import aruco_markers as ar
from math import pi
import pickle
from aruco_utils import ARUCO_DICT
import fetch_utils as fu
import threading


class Fetch_markers(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        img2, self.gridboard = ar.gridboard_aruco_create(n_markers_w=10, n_markers_h=10, dict_name="DICT_4X4_100",
                                                         image_size=(1754, 1240),
                                                         marker_side=0.067, marker_separation=0.015,
                                                         padding_size=[0, 5, 0, 0])
        self.cam_calib = pickle.load(open("calibration_output.pickle", "rb"))
        self.aruco_params = cv2.aruco.DetectorParameters_create()
        self.aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_100"])
        self.rgb = rgbcamera.RGBCamera()
        self.all_markers = {}
        self.all_markers_by_distance = {}
        self.all_markers_by_time = {}
        # self.tvecs = None
        # self.rvecs = None

    def get_markers_info(self, dtime=10 ** 10, mode=1):
        markers_info = {}
        # all_markers_info = copy.copy(self.all_markers)
        if mode == 0:
            all_markers_info = copy.copy(self.all_markers_by_time)
        elif mode == 1:
            all_markers_info = copy.copy(self.all_markers_by_distance)
        # print(all_markers_info)
        if all_markers_info:
            for mid in all_markers_info:
                # r = all_markers_info[mid][1]
                # t = all_markers_info[mid][0]
                # print('tx: {}, ty: {}, tz: {}'.format(t[0, 0], t[0, 1], t[0, 2]))
                # print('rx: {}, ry: {}, rz: {}'.format(r[0, 0] * 180 / pi, r[0, 1] * 180 / pi, r[0, 2] * 180 / pi))
                if (time.time() - all_markers_info[mid][2]) < dtime:
                    markers_info[mid] = [all_markers_info[mid][0], all_markers_info[mid][1]]
        return markers_info

    def run(self):
        while True:
            ret, frame = self.rgb.read()
            if ret:
                detected_markers_image, tvecs, rvecs, ids = ar.aruco_position_estimate(frame=frame,
                                                                                       aruco_dict=self.aruco_dict,
                                                                                       aruco_params=self.aruco_params,
                                                                                       board=self.gridboard,
                                                                                       camera_calib=self.cam_calib,
                                                                                       real_marker_size=0.067)
                if tvecs is not None:#camera frame
                    read_time = time.time()
                    for nn, t in enumerate(tvecs):
                        dist = np.sqrt(t[0, 0] ** 2 + t[0, 1] ** 2 + t[0, 2] ** 2)
                        pos_base = fu.aruco_to_base_link(marker_pos=[t[0, 0], t[0, 1], t[0, 2]],
                                                         frame_id=self.rgb.rgb_frame,
                                                         frame_trans=self.rgb.trans_rgb_base)
                        pos_map = fu.aruco_to_map(marker_pos=[t[0, 0], t[0, 1], t[0, 2]], frame_id=self.rgb.rgb_frame,
                                                  frame_trans=self.rgb.trans_rgb_map)
                        if ids[nn] in self.all_markers:
                            if (dist < self.all_markers[ids[nn]][3]) or (read_time - self.all_markers[ids[nn]][2] > 60):
                                self.all_markers[ids[nn]] = [pos_base, pos_map, read_time, dist]
                        else:
                            self.all_markers[ids[nn]] = [pos_base, pos_map, read_time, dist]

                        if ids[nn] in self.all_markers_by_distance:
                            if dist < self.all_markers_by_distance[ids[nn]][3]:
                                self.all_markers_by_distance[ids[nn]] = [pos_base, pos_map, read_time, dist]
                        else:
                            self.all_markers_by_distance[ids[nn]] = [pos_base, pos_map, read_time, dist]

                        # if ids[nn] in self.all_markers_by_time:
                        #     if read_time - self.all_markers_by_time[ids[nn]][2] > 0:
                        #         self.all_markers_by_time[ids[nn]] = [pos_base, pos_map, read_time, dist]
                        # else:
                        self.all_markers_by_time[ids[nn]] = [pos_base, pos_map, read_time, dist]

                cv2.imshow("Detected", detected_markers_image)
                if cv2.waitKey(66) == 27:
                    break
            else:
                pass
                # print("waiting for the video")
            # if cv2.waitKey(66) == 27:
            #     break
            # time.sleep(0.01)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    rospy.init_node("test_markers")
    markde = Fetch_markers()
    markde.start()
