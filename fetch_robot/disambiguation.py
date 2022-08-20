import rospy
# from head_control import HeadControl
# from camera_modules import RGBCamera, YoloDetector
# from head_control import HeadControl
# from arm_control import ArmControl
# from gripper_control import GripperControl
# from robot import Robot
from kf_robot import kf_Robot

if __name__ == '__main__':
    rospy.init_node("test_disambiguation")
    robot = kf_Robot()
    rgb = robot.rgbCamera
    yolo = robot.yoloDetector
    head = robot.head
    arm_module=robot.arm
    gripper = robot.gripper
    torso = robot.torso
    torso.move_to(0.3)
    while True:
        raw_input('in front of the table?')
        print(yolo.get_item_list())
        obj_name = raw_input("Which object do you want to pick?")
        coord_3d, up = yolo.get_item_3d_coordinates(obj_name, rgb.read())
        print("Picking " + obj_name + ": ", coord_3d, up)
        raw_input('Good to go?')
        head.look_at(coord_3d[0],coord_3d[1],coord_3d[2])
        coord_3d[0]=0.7
        coord_3d[2]+=0.05
        # for i in range(len(up)):
        #     if up[i]>=1:
        #         up[i]=0.9
        print(coord_3d)
        robot.pointing(coord_3d)
