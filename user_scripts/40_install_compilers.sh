#!/bin/bash -ex

basedir=$(dirname $0)
source $basedir/activate_workspace.bashrc

# install compilers
mamba install -y compilers cmake pkg-config make ninja colcon-common-extensions 
