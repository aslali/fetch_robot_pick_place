import rospy
from math import pi
if __name__ == '__main__':
    rospy.init_node("test_pick_place")

    from arm_control import ArmControl
    from camera_modules import *
    from torso_control import TorsoControl
    from gripper_control import GripperControl, CLOSED_POS
    
    arm = ArmControl()
    # yolo = YoloDetector()
    # rgb = RGBCamera()
    gripper = GripperControl()
    torso = TorsoControl()
    # pp = PickPlace()

    torso.move_to(.4)
    time.sleep(2.0)
    arm.stow()
    time.sleep(3)
    #fetch_arm.stow()
    #gripper.open()
    # print (object_name)
    contin = True
    coord_3d = [0.7942, 0.0128, 0.9205]
    coord_3d = [0.8134044702277726, -0.06401807205241584, 1.1138920127486247]

    while contin is True:
        # raw_input('in front of the table?')
        # print(yolo.get_item_list())
        # if object_name in yolo.get_item_list():
        #     print ('YES')
        # obj_name = raw_input("Which object do you want to pick?")
        # coord_3d, up = yolo.get_item_3d_coordinates(obj_name, rgb.getRGBImage())
        # print("Picking " + obj_name + ": ", coord_3d, up)
        # raw_input('Good to go?')

        torso.move_to(.35)
        time.sleep(2.0)
        # coord_3d = [0.9, 0.1, 0.8]
          # center  # [0.6478926483367018, -0.16955347545496427, 0.8426119154023802]
        # coord_3d_b = [0.65, 0.3, 0.6]  # human right
        # coord_3d_c = [0.65, -0.3, 0.6]
        print('coords are', [coord_3d[0], coord_3d[1], coord_3d[2]])
        plan = arm.move_cartesian_position([coord_3d[0], coord_3d[1], coord_3d[2]], [0, pi/2, 0])
        if plan is True:
            time.sleep(30.0)
            # gripper.close(CLOSED_POS, 60)
            # time.sleep(3.0)
            # fetch_arm.stow()
            # time.sleep(3.0)
            # fetch_torso.move_to(.4)
            # time.sleep(2.0)
            # gripper.open()
            arm.stow()
            time.sleep(3.0)

        if raw_input('continue') == 'n':
            contin = False
            if contin is False:
                arm.tuck()
                time.sleep(3)
        else:
            coord_3d[0] = float(raw_input('coord1'))
            coord_3d[1] = float(raw_input('coord2'))
            coord_3d[2] = float(raw_input('coord3'))


