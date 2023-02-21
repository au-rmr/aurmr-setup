import sys
import logging
import subprocess

import questionary

import rich_click as click
from click_prompt import confirm_option
from click_prompt import choice_option
from click_prompt import auto_complete_option

from aurmr_setup.cli.main_cli import cli
from aurmr_setup.cli.main_cli import console

from aurmr_setup.core.workspace import WORKSPACE_DIR
from aurmr_setup.core.workspace import Workspace
from aurmr_setup.core.workspace import get_active_workspace
from aurmr_setup.core.workspace import get_all_workspaces

logger = logging.getLogger(__name__)

@cli.command()
@click.option('--workspace_name', prompt="Name of the new workspace")
@choice_option('--python-version', type=click.Choice(['3.8', '3.9']))
def init(workspace_name: str, python_version: str):
    """
    Initializes a new and empty workspace
    """
    create_workspace(workspace_name, python_version)

def create_workspace(workspace_name: str, python_version: str = '3.8'):
    if not workspace_name:
        logger.warning('No workspace selected')
        sys.exit(1)
    logger.info(f'creating workspace {workspace_name} with python {python_version}')
    workspace = Workspace.create(workspace_name, python_version)
    if not workspace:
        logger.error('Unable to create workspace %s', workspace_name)
        sys.exit(1)

@cli.command()
@click.option('--all', '-a', default=False, is_flag=True)
def list(all: bool):
    """
    Lists all existing workspaces
    """
    for w in Workspace.list(all):
        console.print(w)

@cli.command()
@choice_option('--workspace', type=click.Choice(get_all_workspaces() + ['new']))
def select(workspace: str):
    """
    Selects a workspace. Typically you want to run `activate` in your shell
    """
    select_workspace(workspace)

def select_workspace(workspace: str):
    if workspace == 'new':
        workspace = questionary.text('Name of the new workspace:').ask()
        create_workspace(workspace)
    return Workspace(workspace).activate()

@cli.command()
@choice_option('--workspace', type=click.Choice(get_all_workspaces()))
def remove_workspace(workspace):
    """
    Removes a workspace
    """
    workspace = Workspace(workspace)
    if questionary.confirm(f'Do you really want to remove the workspace {workspace}', default=False).ask():
        workspace.remove()
       


@choice_option('--clone-from-workspace', type=click.Choice(get_all_workspaces()))
@click.argument('new-workspace-name')
@cli.command()
def clone(clone_from_workspace: str, new_workspace_name: str):
    """
    Clone an existing workspace.
    """
    to_clone = Workspace(clone_from_workspace)
    new_workspace = Workspace(new_workspace_name)
    if new_workspace.exists():
        logger.error('Workspace already exists %s', workspace_full_path)
        sys.exit(1)

    if to_clone.clone(new_workspace):
        console.print("Done.")
        console.print("Missing steps: 1.) activate the workspace 2.) Run catkin build 3.) reopen terminal and activate workspace again")



@cli.command()
def update():
    """
    Updates all git repositories within a workspace
    """
    workspace_name = get_active_workspace()
    if not workspace_name:
        logger.error('Select a workspace first')
        sys.exit(1)

    Workspace(workspace_name).update_src()


def get_all_ros_packages():
    misc = ['catkin_tools', 'rosdep']
    from aurmr_setup.core import robostack_utils
    return robostack_utils.packages + misc
    """
    import pandas as pd
    df = pd.read_html('https://robostack.github.io/noetic.html')[0]
    return list(df.Package)
    """

def get_all_src_packages():
    return ['git@github.com:au-rmr/aurmr_tahoma.git',
            'git@github.com:au-rmr/aurmr_inventory.git',
            'git@github.com:au-rmr/aurmr-dataset.git',
            'git@github.com:au-rmr/Azure_Kinect_ROS_Driver.git#melodic']


@cli.command()
@auto_complete_option('--package', choices=get_all_ros_packages())
def add(package: str):
    """
    Installs a conda package to an activate workspace. Similar to `conda
    install` but with auto completion for robostack.
    """
    workspace_name = get_active_workspace()
    if not workspace_name:
        logger.error('Select a workspace first')
        sys.exit(1)
    workspace = Workspace(workspace_name)
    workspace.install(package)

    find_and_install_missing_packages(workspace)



def find_and_install_missing_packages(workspace: Workspace):
    from aurmr_setup.core import robostack_utils
    from aurmr_setup.core.utils import get_packages
    required_packages = get_packages(workspace)
    robostack_packages = [p for p in required_packages if p in robostack_utils.packages]
    missing_packages = [p for p in required_packages if p not in robostack_utils.packages]
    if not missing_packages:
        console.print(f'Found {len(required_packages)} required packages')
        console.print('Found required packages on robostack')
        for p in robostack_packages:
            console.print(f' - {p}')
        console.print('Unable to find the following packages')
        for p in missing_packages:
            console.print(f' - {p}')
        if questionary.confirm(f'Do you want to install {len(robostack_packages)} packages?').ask():
            workspace.install(' '.join(robostack_packages))


@cli.command()
@click.argument('workspace-name')
@click.option('--overwrite-export', default=False, is_flag=True)
@click.option('--remove-env/--keep-env', default=True)
def archive(workspace_name: str, overwrite_export: bool, remove_env: bool):
    """
    Archives a workspaces

    The current conda environment will be exported to a environment.yaml.
    """
    workspace = Workspace(workspace_name)
    if workspace.archived:
        logging.error('Workspace already archived')
        sys.exit(-1)

    if remove_env:
        print('Conda environment will be exported and [red][b]removed[/b][/red].')
        print('Restoring the environment  might not work for local installed packages.')
        print('Please use the flag --keep-env if you do not want to do this.')

    if questionary.confirm(f'Do you really want to archive the workspace {workspace}', default=False).ask():
        workspace.move_to_archive(overwrite_export, remove_env)


@cli.command()
@click.argument('workspace-name')
def unarchive(workspace_name: str):
    """
    Restores a previously archived workspace
    """
    workspace = Workspace(workspace_name, True)
    if not workspace.exists():
        logging.error('Workspace not archived')
        sys.exit(-1)
    workspace.import_from_archive()



@cli.command()
@auto_complete_option('--package', type=click.Choice(get_all_src_packages()))
def add_src(package: str):
    """
    Clones a given repository to an active workspace.
    """
    workspace_name = get_active_workspace()
    if not workspace_name:
        logger.error('Select a workspace first')
        sys.exit(1)
 
    workspace = Workspace(workspace_name)
    workspace_src_path = workspace.src_path

    if '#' in package:
        url, branch = package.rsplit('#', 2)
    else:
        url = package
        branch = 'main'

    cmd = ['git', 'clone', '-b', branch, url]
    subprocess.run(cmd, check=True, cwd=workspace_src_path)

    find_and_install_missing_packages(workspace)

