#!/bin/bash -exu

user_setup_script=$(dirname "$0")
user_setup_script=${user_setup_script}/../user_scripts/setup.bash
user_setup_script=$(readlink -f "${user_setup_script}")


curl -L git.io/antigen > $HOME/antigen.zsh

cat >> $HOME/.antigenrc <<EOF
antigen use oh-my-zsh

antigen bundle git
antigen bundle git-prompt
antigen bundle git-lfs
antigen bundle command-not-found
antigen bundle colored-man-pages
antigen bundle fzf
antigen bundle tmux
antigen bundle vim-interaction
antigen bundle z

antigen bundle zsh-users/zsh-completions
antigen bundle zsh-users/zsh-autosuggestions
antigen bundle zsh-users/zsh-syntax-highlighting

antigen theme robbyrussell

antigen apply
EOF


cat >> $HOME/.zshrc <<EOF
source $HOME/antigen.zsh
antigen init $HOME/.antigenrc

export CDPATH=\$CDPATH:$HOME/workspaces/

source $user_setup_script

export PATH=$HOME/.local/bin:\$PATH
EOF


chsh -s /usr/bin/zsh
