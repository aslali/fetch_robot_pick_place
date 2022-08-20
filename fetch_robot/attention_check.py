import rospy
import threading
from socket import *
import sys
import time

#listening data from headandGaze, run this file first

host = "kd-pc29.local"
port = 8090
size = 1
s = socket(AF_INET, SOCK_STREAM) #socket.socket(socket.AF_INET, SOCK_DGRAM) for UDP connection
s.bind((host,port))
s.listen(5)
client, address = s.accept()
stop=0



def threadCheckAttention(data):
    global stop
    from kf_robot import kf_Robot

    robot=kf_Robot()
    speech = robot.speaker


    while True:
        if data[0] == "2": # "full attention"
            stop=1 # run user cmd input and ambiguity determine
        elif data[0] == "1": # "semi-attention"
            speech.say("Hi, please look at me!")
            time.sleep(5)
            # stop=0
        elif data[0] == "0": # "no attention"
            # stop=0
            speech.say("Hello, may I have your attention please?")
            initial_time = time.time()
            # arm_module.wave(initial_time, 25)# does not work, in ArmControl(), gripper controller is not recognized
            robot.wave(initial_time, 25)
            time.sleep(10)
        else:
            # stop=0
            print("I am here!")
        # print(data)
        # print("size:", sys.getsizeof(data))
        # print("stop is: ", stop)
        # print("==================")


def checkAttention():
    import time
    rospy.init_node("test_attention")

    data = client.recv(size)# initail read
    data = [data.strip().decode("utf-8")]
    attentionBackground=threading.Timer(1,threadCheckAttention,args=(data,))
    attentionBackground.setDaemon(True)
    attentionBackground.start()

    while True:
        data[0] = client.recv(size)
        data[0] = data[0].strip().decode("utf-8")

        # print(data)
        if stop==1:
            client.close()
            torso.move_to(0.0)
            break
        # print(data)
    print("finished")





if __name__ == '__main__':
    checkAttention()
    # import time
    # initial_time = time.time()
    # rospy.init_node("test_kf_arm")
    # from kf_robot import kf_Robot
    #
    # robot=kf_Robot()
    #
    #
    # head = robot.head
    # arm_module=robot.fetch_arm
    # gripper = robot.gripper
    # fetch_torso = robot.fetch_torso
    # speech = robot.speaker
    #
    # data = client.recv(size)# initail read
    # data = [data.strip().decode("utf-8")]
    # attentionBackground=threading.Timer(1,threadCheckAttention,args=(data,))
    # attentionBackground.setDaemon(True)
    # attentionBackground.start()
    #
    # while True:
    #     data[0] = client.recv(size)
    #     data[0] = data[0].strip().decode("utf-8")
    #
    #     # print(data)
    #     if stop==1:
    #         client.close()
    #         fetch_torso.move_to(0.0)
    #         break
    #     # print(data)
    # print("finished")
    # arm_module.scene.clear()
