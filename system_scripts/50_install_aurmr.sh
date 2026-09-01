#!/bin/bash -eu

sudo apt install python3-pip 


pip install -U pip
pip install -U poetry


aurmr_dir=$(dirname "$0")
aurmr_dir=${aurmr_dir}/../

poetry run -C ${aurmr_dir} pip install -e .

_AURMR_COMPLETE=bash_source aurmr > ${aurmr_dir}/shell-complete/aurmr-complete.bash
_AURMR_COMPLETE=zsh_source aurmr > ${aurmr_dir}/shell-complete/aurmr-complete.zsh
