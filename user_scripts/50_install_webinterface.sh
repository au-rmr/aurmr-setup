#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

mamba install -y nodejs yarn

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
