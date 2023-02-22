#!/bin/bash -exu

sudo apt install fzf

user_setup_script=$(dirname "$0")
user_setup_script=${user_setup_script}/../user_scripts/setup.bash
user_setup_script=$(readlink -f "${user_setup_script}")

cat >> $HOME/.bashrc <<EOF
if [ -f /usr/share/doc/fzf/examples/completion.bash ]; then
	source /usr/share/doc/fzf/examples/completion.bash

fi
if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then
	source /usr/share/doc/fzf/examples/key-bindings.bash
fi

source $user_setup_script

export PATH=$HOME/.local/bin:\$PATH
EOF
