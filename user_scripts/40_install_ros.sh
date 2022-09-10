#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

# install ROS
mamba install -y ros-noetic-desktop-full
mamba install -y catkin_tools rosdep
mamba install -y ros-noetic-ros-numpy

# reload workspace 
conda deactivate 
conda activate $WORKSPACE_NAME

# run rosdep

rosdep init
rosdep update

