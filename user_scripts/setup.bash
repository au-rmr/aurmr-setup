function activate() {
	if [ -n "$1" ]; then
		$WORKSPACE_NAME=$i
		echo $WORKSPACE_NAME > $HOME/.active_workspace
	else
		aurmr select-workspace;
		WORKSPACE_NAME=$(cat $HOME/.active_workspace)
	fi

	echo "activating workspace $WORKSPACE_NAME"
	conda activate $WORKSPACE_NAME;
	source $HOME/workspaces/$WORKSPACE_NAME/devel/setup.bash
}
