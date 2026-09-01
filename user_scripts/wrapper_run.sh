#!/usr/bin/zsh
WORKSPACE_NAME=$CONDA_DEFAULT_ENV
if [ -f $HOME/workspaces/$WORKSPACE_NAME/devel/setup.zsh ] && [ $SHELL = "/usr/bin/zsh" ]; then
	source $HOME/workspaces/$WORKSPACE_NAME/devel/setup.zsh
elif [ -f $HOME/workspaces/$WORKSPACE_NAME/devel/setup.bash ]; then
	source $HOME/workspaces/$WORKSPACE_NAME/devel/setup.bash
else
	echo "WORKSPACE not build. Please run catkin build in $HOME/workspaces/$WORKSPACE_NAME/"
fi

env
$*
