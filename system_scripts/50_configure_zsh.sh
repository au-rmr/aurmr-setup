#!/bin/bash -exu

sudo apt install zsh fzf


aurmr_dir=$(dirname "$0")
aurmr_dir=${aurmr_dir}/../

user_setup_script=$(readlink -f "${aurmr_dir}/user_scripts/aurmr_setup.bashrc")


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

if [ -f ${aurmr_dir}/shell-complete/aurmr-complete.zsh ]; then
	source ${aurmr_dir}/shell-complete/aurmr-complete.zsh
fi

if [ -f ${user_setup_script} ]; then
	source ${user_setup_script}
fi

export PATH=$HOME/.local/bin:\$PATH
export PROMPT='%(!.%{%F{yellow}%}.)\$USER @ %{\$fg[white]%}%M %{\$fg_bold[red]%}➜ %{\$fg_bold[green]%}%p %{\$fg[cyan]%}%c %{\$fg_bold[blue]%}\$(git_prompt_info)%{\$fg_bold[blue]%} % %{\$reset_color%}'
export RPROMPT="[%D{%Y-%m-%d %T}]"
EOF


chsh -s /usr/bin/zsh
