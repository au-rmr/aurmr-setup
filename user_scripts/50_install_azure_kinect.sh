#!/bin/bash -ex

if [ -n "$1" ]; then
	echo "workspace name = $1"
else
	echo "Usage $0 <workspace_name>."
	exit 1
fi

WORKSPACE_NAME=$1

source "/home/aurmr/miniconda3/etc/profile.d/conda.sh"

conda activate $WORKSPACE_NAME
mkdir -p $HOME/workspaces/$WORKSPACE_NAME/src
cd $HOME/workspaces/$WORKSPACE_NAME/src

git clone git@github.com:microsoft/Azure_Kinect_ROS_Driver.git

cd ..

catkin build
