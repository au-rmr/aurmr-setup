#!/bin/bash -ex

if [ -n "$1" ]; then
	echo "workspace name = $1"
    WORKSPACE_NAME=$1
elif [ -n "WORKSPACE_NAME" ]; then
	echo "workspace name = $WORKSPACE_NAME"
else
	echo "Usage $0 <workspace_name>."
	exit 1
fi

source "/home/aurmr/miniconda3/etc/profile.d/conda.sh"
conda activate $WORKSPACE_NAME

mkdir -p $HOME/workspaces/$WORKSPACE_NAME/src
cd $HOME/workspaces/$WORKSPACE_NAME/src


# install ROS
mamba install -y ros-noetic-desktop-full
mamba install -y catkin_tools rosdep

# reload workspace 
conda deactivate 
conda activate $WORKSPACE_NAME

# run rosdep

rosdep init
rosdep update

