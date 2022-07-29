#!/bin/bash -exu

if [ -n "$1" ]; then
	echo "workspace name = $1"
else
	echo "Usage $0 <workspace_name>."
	exit 1
fi

WORKSPACE_NAME=$1

if [ -f $HOME/workspaces/$WORKSPACE_NAME ]; then
	echo "WORKSPACE already exists"
	exit 1
fi

mamba create -n $WORKSPACE_NAME python=3.8

source "/home/aurmr/miniconda3/etc/profile.d/conda.sh"

conda activate $WORKSPACE_NAME

echo "https://robostack.github.io/GettingStarted.html"

conda config --env --add channels conda-forge
# and the robostack channels
conda config --env --add channels robostack


mamba install ros-noetic-desktop-full
mamba install ros-noetic-moveit-servo
# mamba install ros-noetic-desktop
# mamba install ros-noetic-image-geometry
# mamba install ros-noetic-camera-info-manager
# mamba install ros-noetic-realsense2-camera
mamba install compilers cmake pkg-config make ninja colcon-common-extensions
mamba install catkin_tools

conda deactivate 
conda activate $WORSPACE_NAME

#mamba install rosdep
#rosdep init
#rosdep update

mkdir -p $HOME/workspaces/$WORKSPACE_NAME/src
cd $HOME/workspaces/$WORKSPACE_NAME/src

git clone git@github.com:microsoft/Azure_Kinect_ROS_Driver.git
git clone git@github.com:au-rmr/aurmr_perception.git
git clone git@github.com:au-rmr/aurmr_tahoma.git

#git clone git@github.com:au-rmr/aurmr_storm.git
#git clone git@github.com:au-rmr/aurmr_web_interface.git

cd ..
catkin build
