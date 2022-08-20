import cv2
import time
# import sys
import rospy
from sensor_msgs.msg import Image
import numpy as np
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud, transform_to_kdl


class RGBCamera:
    def __init__(self):
        ## Subscribe to the camera of the robot
        topic_name = '/head_camera/rgb/image_raw'
        self.curr_image = None
        self._image_sub = rospy.Subscriber(topic_name, Image, self._color_image_cb)
        # time.sleep(1)
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.rgb_frame = None
        self.rgb_trans = None

    def _color_image_cb(self, data):
        self.rgb_frame = data.header.frame_id
        self.trans_rgb_map = self.tf_buffer.lookup_transform("map", data.header.frame_id,
                                                              # msg.header.stamp,
                                                              rospy.Time(0),
                                                              rospy.Duration(1.0))
        self.trans_rgb_base = self.tf_buffer.lookup_transform("base_link", data.header.frame_id,
                                                              # msg.header.stamp,
                                                              rospy.Time(0),
                                                              rospy.Duration(1.0))
        self.curr_image = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)

        # rospy.Time().now()


    def save_image(self):
        if self.curr_image is not None:
            cv2.imwrite("./trainingset/" + str(time.time()) + ".jpg", self.curr_image);

    def read(self):
        if np.size(self.curr_image) > 10:
            return True, cv2.cvtColor(self.curr_image, cv2.COLOR_BGR2RGB)
        else:
            # print('no video')
            return False, None

    def release(self):
        pass
