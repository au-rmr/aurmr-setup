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

source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate $WORKSPACE_NAME

mkdir -p $HOME/workspaces/$WORKSPACE_NAME/src
cd $HOME/workspaces/$WORKSPACE_NAME/src
