#!/bin/bash -ex

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

mamba create -y -n $WORKSPACE_NAME python=3.8

source "/home/aurmr/miniconda3/etc/profile.d/conda.sh"

conda activate $WORKSPACE_NAME

echo "https://robostack.github.io/GettingStarted.html"

conda config --env --add channels conda-forge
# and the robostack channels
conda config --env --add channels robostack

# install compilers
mamba install -y compilers cmake pkg-config make ninja colcon-common-extensions 

# install ROS
mamba install -y ros-noetic-desktop-full
mamba install -y catkin_tools rosdep

# reload workspace 
conda deactivate 
conda activate $WORKSPACE_NAME

# run rosdep

rosdep init
rosdep update

# create workspace

mkdir -p $HOME/workspaces/$WORKSPACE_NAME/src

echo """
=========================================
Done setting up workspace $WORKSPACE_NAME
=========================================

You can now run activate $WORKSPACE_NAME or 
simply type 'activate'. 

To build your workspace use catkin build, i.e.

cd $HOME/workspaces/$WORKSPACE_NAME/
catkin build
"""
