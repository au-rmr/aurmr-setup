function activate() {

	if [ -n "$ROS_VERSION" ]; then
		echo "ROS environment already sourced. Aborting"
		return
	fi

	if [ -n "$1" ]; then
		WORKSPACE_NAME=$1
		echo $WORKSPACE_NAME > $HOME/.active_workspace
	else
		aurmr select;

		if [ "$?" -ne 0 ]; then
			echo "Unable to select workspace"
			return
		fi
		WORKSPACE_NAME=$(cat $HOME/.active_workspace)
	fi

	echo "activating workspace $WORKSPACE_NAME"
	conda activate $WORKSPACE_NAME;
	if [ -f $HOME/workspaces/$WORKSPACE_NAME/devel/setup.bash ]; then
		source $HOME/workspaces/$WORKSPACE_NAME/devel/setup.bash
	else
		echo "WORKSPACE not build. Please run catkin build in $HOME/workspaces/$WORKSPACE_NAME/"
	fi

	# load custom envs
	if [ -f $HOME/workspaces/$WORKSPACE_NAME/user.bashrc ]; then
		source $HOME/workspaces/$WORKSPACE_NAME/user.bashrc

	fi
	
}
