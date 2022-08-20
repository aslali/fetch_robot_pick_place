from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import rospy
import numpy as np
import cv2





class RGBDcamera():
    def __init__(self):
        self.cloud = PointCloud2()
        # self.tf_buffer = tf2_ros.Buffer()
        # self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        sub_once = rospy.Subscriber('/head_camera/depth_registered/points', PointCloud2,
                                    self.callback)
        rospy.wait_for_message('/head_camera/depth_registered/points', PointCloud2, timeout=100.0)

    def callback(self, msg):
        self.cloud = msg
        # print(self.cloud)

    def get_depth(self):
        # print(self.cloud)
        # self.curr_image = np.frombuffer(self.cloud.data, dtype=np.uint8).reshape(640, 480, -1)
        # self.trans = self.tf_buffer.lookup_transform("base_link", msg.header.frame_id,
        #                                              # msg.header.stamp,
        #                                              rospy.Time().now(),
        #                                              rospy.Duration(1.0))
        print((self.cloud.fields))


if __name__ == "__main__":
    rospy.init_node("test_speech", anonymous=True)
    rgbd = RGBDcamera()
    for i in range(5):
        rgbd.get_depth()