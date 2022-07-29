function activate() {
	conda activate $1;
	source $HOME/workspaces/$1/devel/setup.bash
}
