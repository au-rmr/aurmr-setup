#!/bin/bash -ex


if [ -n "$1" ]; then
	echo "workspace name = $1"
else
	echo "Usage $0 <workspace_name>."
	exit 1
fi


if [ -n "$2" ]; then
	PYTHON_VERSION=$2
else
	PYTHON_VERSION=3.11 #robostack not maintained for 3.8 anymore
fi

WORKSPACE_NAME=$1

if [ -f $HOME/workspaces/$WORKSPACE_NAME ]; then
	echo "WORKSPACE already exists"
	exit 1
fi

mamba create -y -n $WORKSPACE_NAME python=$PYTHON_VERSION -c conda-forge --override-channels

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

echo "https://robostack.github.io/GettingStarted.html"

conda config --env --add channels conda-forge
# and the robostack channels
conda config --env --add channels robostack-noetic #-staging

mamba install -y catkin_tools rosdep ros-noetic-catkin -c robostack-noetic --override-channels
rosdep update || true


cat >/tmp/50_ros_workspace.sh <<EOF

export WORKSPACE_PATH=$HOME/workspaces/$WORKSPACE_NAME

if [ -f $WORKSPACE_PATH/devel/setup.zsh ] && [ $SHELL = "/usr/bin/zsh" ]; then
	source $WORKSPACE_PATH/devel/setup.zsh
elif [ -f $WORKSACE_PATH/devel/setup.bash ]; then
	source $WORKSPACE_PATH/devel/setup.bash
fi
if [ -f $WORSPACE_PATH/user.bashrc ]; then
	source $WORKSPACE_PATH/user.bashrc
fi



EOF

conda run -n $WORKSPACE_NAME catkin build --workspace $HOME/workspaces/$WORKSPACE_NAME/ || true

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
