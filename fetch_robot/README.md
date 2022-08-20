**High Level API for Fetch**

Dependencies:

- ROS Melodic

Before starting:

You need to run a couple of things on the robot before getting started
```
ssh fetch_admin@fetch1092
roslaunch robot.bringup.launch                      --> Will launch everything you need on the robot
```
AFTER that, on the computer:
```
cd /wherever/fetchHighLevelAPI/is
roslaunch computer_bringup.launch            --> Will launch everything you need on the computer
```
You can find examples of how to use the module in each file.



**Gazebo for Fetch**

This wrapper is compatible with Gazebo as well. All you need to do is:
```
cd /wherever/fetchHighLevelAPI/is
roslaunch gazebo_bringup.launch            --> Will launch everything you need on the computer
```
