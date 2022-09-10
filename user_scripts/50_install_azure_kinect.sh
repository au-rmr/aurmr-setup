#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

git clone git@github.com:microsoft/Azure_Kinect_ROS_Driver.git

cd ..

catkin build
