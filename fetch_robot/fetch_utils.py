import rospy
from geometry_msgs.msg import PointStamped
from tf2_sensor_msgs.tf2_sensor_msgs import transform_to_kdl
import PyKDL


def do_transform_point(point, transform):
    p = transform_to_kdl(transform) * PyKDL.Vector(point.point.x, point.point.y, point.point.z)
    res = PointStamped()
    res.point.x = p[0]
    res.point.z = p[2]
    res.point.y = p[1]
    res.header = transform.header
    return res




def aruco_to_base_link(marker_pos, frame_id, frame_trans):
    rgb_point = PointStamped()
    rgb_point.header.frame_id = frame_id
    rgb_point.header.stamp = rospy.Time(0)

    rgb_point.point.x = marker_pos[0]
    rgb_point.point.y = marker_pos[1]
    rgb_point.point.z = marker_pos[2]

    map_point = do_transform_point(rgb_point, frame_trans)
    return [map_point.point.x, map_point.point.y, map_point.point.z]

def aruco_to_map(marker_pos, frame_id, frame_trans):
    rgb_point = PointStamped()
    rgb_point.header.frame_id = frame_id
    rgb_point.header.stamp = rospy.Time(0)

    rgb_point.point.x = marker_pos[0]
    rgb_point.point.y = marker_pos[1]
    rgb_point.point.z = marker_pos[2]

    map_point = do_transform_point(rgb_point, frame_trans)
    return [map_point.point.x, map_point.point.y, map_point.point.z]