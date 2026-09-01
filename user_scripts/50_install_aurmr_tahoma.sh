#!/bin/bash -ex


basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

git clone --recurse-submodules git@github.com:au-rmr/aurmr_tahoma.git

# install sip. newer versions of sip do not seem to work
mamba install -y sip=4.19.22

mamba install -y ros-noetic-ros-controllers 
mamba install -y ros-noetic-ros-control
mamba install -y ros-noetic-roslint
mamba install -y ros-noetic-ur-msgs
mamba install -y ros-noetic-actionlib
mamba install -y ros-noetic-handeye

#dependencies for aurmr_tahoma
mamba install -y ros-noetic-soem ros-noetic-industrial-robot-status-interface 
mamba install -y ros-noetic-moveit-servo ros-noetic-scaled-joint-trajectory-controller ros-noetic-speed-scaling-state-controller 
mamba install -y ros-noetic-realsense2-description 
# mamba install -y ros-noetic-moveit-planners-ompl ros-noetic-moveit-ros-visualization ros-noetic-moveit-fake-controller-manager ros-noetic-moveit-simple-controller-manager ros-noetic-trac-ik-kinematics-plugin ros-noetic-cartesian-trajectory-controller ros-noetic-force-torque-sensor-controller ros-noetic-industrial-robot-status-controller ros-noetic-twist-controller ros-noetic-velocity-controllers ros-noetic-effort-controllers ros-noetic-gripper-action-controller ros-noetic-roboticsgroup-upatras-gazebo-plugins ros-noetic-moveit-commander ros-noetic-realsense2-camera ros-noetic-ros-numpy ros-noetic-rqt-controller-manager ros-noetic-pass-through-controllers ros-noetic-ur-msgs 
#ros-noetic-ur-client-library 
#ros-noetic-moveit-ros-perception

pip install pyassimp


# https://github.com/RoboStack/ros-noetic/issues/193
# mamba install -y ros-noetic-moveit-ros-perception=1.1.0
mamba install -y ros-noetic-moveit-ros-perception

#rosdep install --ignore-src --from-paths . -y -r --os="ubuntu:focal" --rosdistro=noetic


cd ..

catkin build


# dependencies for perception python > 3.9
# mamba install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia


