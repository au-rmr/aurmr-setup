#!/bin/bash -exu

sudo apt install fzf


aurmr_dir=$(dirname "$0")
aurmr_dir=${aurmr_dir}/../
user_setup_script=$(readlink -f "${aurmr_dir}/user_scripts/aurmr_setup.bashrc")

cat >> $HOME/.bashrc <<EOF
if [ -f /usr/share/doc/fzf/examples/completion.bash ]; then
	source /usr/share/doc/fzf/examples/completion.bash

fi
if [ -f /usr/share/doc/fzf/examples/key-bindings.bash ]; then
	source /usr/share/doc/fzf/examples/key-bindings.bash
fi

if [ -f ${aurmr_dir}/shell-complete/aurmr-complete.bash ]; then
	source ${aurmr_dir}/shell-complete/aurmr-complete.bash
fi

if [ -f ${user_setup_script} ]; then
	source ${user_setup_script}
fi


export PATH=$HOME/.local/bin:\$PATH
EOF
