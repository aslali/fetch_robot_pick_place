import cv2
import sys
import rospy
from camera_modules import RGBCamera, YoloDetector
from fuzzyDecision import AmbiguityFuzzy
import threading

userCMD = ""
printOnce = 0
runOnce = 0
def getUserInput():
    global printOnce, runOnce #flags
    global userCMD #we don't want to use thread.join to get the return value becuase .join() will block
    print("Type down the object you want Fetch to pick up!")

    while True:
        userCMD = sys.stdin.readline().strip()
        printOnce = 0
        runOnce = 0
        if userCMD=="":
            break
        print("User input: "+userCMD)

backgroundThread=threading.Thread(target=getUserInput)
backgroundThread.daemon=True
backgroundThread.start()



def get_confidence(boxes):
    confidence=[]
    for box in boxes:
        confidence.append(box[-1])
    return confidence

def fuzzy_input_extract(userCMD, detected_obj, detected_confidence):
    global printOnce
    # print(0)
    if userCMD == "":# dummy code, maybe the entire ambiguity block will not invoke if user command is empty
        confidence=0
        count=0
        #print((confidence, count))
        return
    # print(1)
    userInput=userCMD
    userInput=userInput.lower()
    indices = [i for i, x in enumerate(detected_obj) if x == userInput]
    count=len(indices)
    # print(2)
    if count ==0:
        confidence = 0
        if printOnce == 0:
            print((confidence, count))
            printOnce = 1
        return (confidence, count)
    # print(3)
    targetConfLs= [detected_confidence[i] for i in indices]
    confidence=max(targetConfLs)

    if printOnce == 0:
        print((confidence, count))
        printOnce = 1
    # print("end of the function")
    return (confidence, count)



if __name__ == '__main__':

    rospy.init_node("test_cameras")
    rgb = RGBCamera()
    yd = YoloDetector()
    aFuzzyCtrl= AmbiguityFuzzy()

    print("Testing cameras")
    while 1:
        #print("in the loop") #in the loop
        try:
            cv2.imshow("window_rgb", rgb.getRGBImage())
            # print("show")
        except:
            continue
            # print("continue")
        try:
            cv2.imshow("window_dn", yd.getDetectionImage())
            detection = yd.detect()
            boxes = detection[0]
            detected_obj = detection[1]
            detected_confidence = get_confidence(boxes)
            # fuzzy_input_extract(userCMD, detected_obj, detected_confidence)
            # print(detected_obj)
            if runOnce==0:
                print("run fuzzy extraction")
                visionCrispSet=fuzzy_input_extract(userCMD, detected_obj, detected_confidence)
                runOnce=1
                # aFuzzyCtrl.determine(visionCrispSet)
                aFuzzyCtrl.determine(visionCrispSet[0],visionCrispSet[1])
        except:
            continue
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
