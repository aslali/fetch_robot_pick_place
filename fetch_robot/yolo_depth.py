from sensor_msgs.msg import Image
from darknet_ros_msgs.msg import BoundingBoxes
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2 as pc2
from geometry_msgs.msg import PointStamped

import tf2_py as tf2
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud, transform_to_kdl
import PyKDL
import numpy as np


def do_transform_point(point, transform):
    p = transform_to_kdl(transform) * PyKDL.Vector(point.point.x, point.point.y, point.point.z)
    res = PointStamped()
    res.point.x = p[0]
    res.point.z = p[2]
    res.point.y = p[1]
    res.header = transform.header
    return res

class YoloDetector():
    def __init__(self):
        ##Subscribe to Yolo topics.
        ## IMPORTANT: run "roslaunch darknet_ros darknet_ros" before!!
        if "/darknet_ros/check_for_objects/feedback" not in np.concatenate(rospy.get_published_topics()):
            rospy.logerr("darknet topics do not exist. run roslaunch darknet_ros darknet_ros before!")
            sys.exit(1)
        self._sub_bb = rospy.Subscriber("/darknet_ros/bounding_boxes", BoundingBoxes, self.cb)
        self._sub_img = rospy.Subscriber("/darknet_ros/detection_image", Image, self.cb)
        self.boxes = []
        self.items = {}
        self.class_names = []
        self.detection_image = None
        self._2dto3d = Get3Dcoordinates()
        rospy.loginfo("YOLO initialised!!")

    ## callback function
    def cb(self, data):
        if type(data) is Image:
            self.detection_image = np.frombuffer(data.data, dtype=np.uint8).reshape(data.height, data.width, -1)
        elif type(data) is BoundingBoxes:
            self.boxes = []
            self.class_names = []
            for box in data.bounding_boxes:
                self.boxes.append([box.xmin, box.ymin, box.xmax, box.ymax, box.probability])
                self.class_names.append(box.Class)
                # self.items[box.Class] = [int(box.xmin+box.xmax)//2, int(box.ymin+box.ymax)//2, box.probability]
                self.items[box.Class] = [box.xmin, box.xmax, box.ymin, box.ymax, box.probability]

    ## some stuff that may be useful in the future....
    def detect(self):
        return self.boxes, self.class_names, self.detection_image

    def clear(self):
        self.boxes = None
        self.class_names = None
        self.detection_image = None

    def getDetectionImage(self):
        return self.detection_image

    def get_item_coordinates(self, item_name):
        if item_name in self.items:
            return self.curr_image.shape, (self.items[item_name][0], self.items[item_name][2]), self.items[item_name][2]
        else:
            return None, None, None

    def get_item_3d_coordinates(self, i_name=None, rgb_img=None, obj_box=None):
        if obj_box is not None:
            box = obj_box
            w, h = box[2] - box[0], box[3] - box[1]
            """
            mask = segmentation(rgb_img, box)
            pc = []
            object_loc = np.argwhere(mask[:,:,0] > 0)
            for pix in object_loc:
                c = self._2dto3d.pixelTo3DPoint(pix[1], pix[0])
                if c:
                    pc.append(c)
            pc = np.array(pc)
            coord_3d = np.median(pc, axis = 0)
            """
            # up_3d = [coord_3d[0], coord_3d[1], np.percentile(pc[:,2], 95)]

            # print('for mid point',self._2dto3d.pixelTo3DPoint(int(box[0] + box[2])//2,
            #                                    int(box[1] + box[3])//2))

            """ Following are for mid point in bounding box. Seems to Work """
            coord_3d = self._2dto3d.pixelTo3DPoint(int(box[0] + box[2]) // 2,
                                                   int(box[1] + box[3]) // 2)
            # coord_3d = self._2dto3d.pixelTo3DPoint(int(box[0] + box[2])//2,
            #                                    int(box[1] + box[3])//2-h*.05)

            """Following is for finding the mid x and top y part of the bounding box"""
            """DEFINITELY DOES NOT WORK. DO NOT EVEN TRY"""
            # coord_3d = self._2dto3d.pixelTo3DPoint(int(box[0] + box[2])//2,
            #                                    int(box[1])-h*.05)

            up_3d = self._2dto3d.pixelTo3DPoint(int(box[0] + box[2]) // 2 + w * .25,
                                                int(box[1] + box[3]) // 2 + h * .4)
            return coord_3d, up_3d

    def clicked(self, x, y):
        # print(x, y)
        for k, box in enumerate(self.boxes):
            # print(box)
            if x > box[0] and x < box[2] and y > box[1] and y < box[3]:
                print("clicked: ", self.class_names[k])
                return self.class_names[k]
        return ""

    def get_item_list(self):
        return self.class_names


class Get3Dcoordinates(object):
    """Supposed to read a point cloud snapshot and returns the XYZ coordinates of a corresponding pixel location
    Doesn't work....."""

    def __init__(self):
        ## Subscribe point cloud
        self.cloud = PointCloud2()
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        sub_once = rospy.Subscriber('/head_camera/depth_registered/points', PointCloud2,
                                    self.callback)
        ## Wait until connection
        rospy.wait_for_message('/head_camera/depth_registered/points', PointCloud2, timeout=100.0)

    def callback(self, msg):
        self.cloud = msg

        self.trans = self.tf_buffer.lookup_transform("base_link", msg.header.frame_id,
                                                     # msg.header.stamp,
                                                     rospy.Time().now(),
                                                     rospy.Duration(1.0))

    ## transform 2D point into 3D coordinates in the "base_link" frame
    def pixelTo3DPoint(self, u, v, cloud=None):
        gen = pc2.read_points(self.cloud, field_names=("x", "y", "z"), skip_nans=True, uvs=[[int(u), int(v)]])
        try:
            target_xyz_cam = list(gen)
        except:
            return None

        # do conversion to global coordinate here
        rgbd_point = PointStamped()
        rgbd_point.header.frame_id = "head_camera_rgb_optical_frame"
        rgbd_point.header.stamp = rospy.Time(0)
        try:
            rgbd_point.point.x = target_xyz_cam[0][0]
        except IndexError:
            return None
        rgbd_point.point.y = target_xyz_cam[0][1]
        rgbd_point.point.z = target_xyz_cam[0][2]

        map_point = do_transform_point(rgbd_point, self.trans)

        return [map_point.point.x, map_point.point.y, map_point.point.z]



if __name__ == '__main__':
    import rospy
    from rgbcamera import RGBCamera
    import cv2
    rospy.init_node("test_cameras")
    rgb = RGBCamera()
    yd = YoloDetector()

    print("Testing cameras")
    while 1:

        if rgb.read()[0]:
            cv2.imshow("window_rgb", rgb.read()[1])
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break


            detected_names = yd.get_item_list()
            # print(detected_names)
            img = rgb.read()[1]
            if detected_names:
                for detected_name in detected_names:
                    if detected_name == 'person':
                    # print(detected_names)
                    # print(yd.items)
                        coord_3d, up = yd.get_item_3d_coordinates(detected_name, img, yd.items[detected_name])
                        print('coo', coord_3d)
        # try:
        #     detected_names = yd.get_item_list()
        #     # print(detected_names)
        #     img = rgb.read()[1]
        #     for detected_name in detected_names:
        #         coord_3d, up = yd.get_item_3d_coordinates(detected_name, img)
        #         print('coo', coord_3d)
        #     # print('up', up)
        #     #     cv2.imshow("window_dn", yd.getDetectionImage())
        # except:
        #     continue

