#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

git clone git@github.com:microsoft/Azure_Kinect_ROS_Driver.git

mkdir deb
DEB_DIR=$(readlink -f deb)

apt download libk4a1.3                                                                                                                                                                                                               
apt download libk4a1.3-dev 

deb -x  libk4a1.3.deb ${DEB_DIR}                                                                                                                                                                                                              
deb -x libk4a1.3-dev.deb ${DEB_DIR}

cd ..


#catkin build azure_kinect_ros_driver

catkin build azure_kinect_ros_driver -v --cmake-args  -Dk4a_DIR:PATH=${DEB_DIR}/usr/lib/x86_64-linux-gnu/cmake/k4a -Dk4arecord_DIR:PATH=${DEB_DIR}/usr/lib/x86_64-linux-gnu/cmake/k4arecord 
