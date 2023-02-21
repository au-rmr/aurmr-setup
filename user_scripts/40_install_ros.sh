#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

# install ROS
mamba install -y ros-noetic-desktop-full
mamba install -y ros-noetic-ros-numpy

