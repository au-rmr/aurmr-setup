#!/bin/bash -eux


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



mamba install -y nodejs yarn

cd src
git clone git@github.com:au-rmr/aurmr_inventory.git

cd aurmr_inventory
yarn install

cd server
yarn install



echo """
=======================
You can launch the server with
aurmr_inventory/server$ node src/index.js
aurmr_inventory$ HOST=localhost yarn start
=======================
"""
