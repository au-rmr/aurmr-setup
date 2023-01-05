#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

git clone git@github.com:microsoft/Azure_Kinect_ROS_Driver.git

cd ..

# catkin config --cmake-args -Dk4a_DIR:PATH=/usr/lib/x86_64-linux-gnu/cmake/k4a

catkin build azure_kinect_ros_driver
