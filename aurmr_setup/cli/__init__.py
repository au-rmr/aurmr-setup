import os
import sys
import logging

import subprocess
import json

from importlib.resources import contents as files
from importlib.resources import path

from functools import lru_cache
from typing import List

import rich_click as click
import questionary


from click_prompt import confirm_option
from click_prompt import choice_option
from click_prompt import auto_complete_option


logger = logging.getLogger(__name__)

ACTIVE_WORKSPACE = '~/.active_workspace'


from aurmr_setup.cli.main import cli
from aurmr_setup.cli.main import console
from aurmr_setup.cli import recipes

from aurmr_setup.cli.workspace import WORKSPACE_DIR
from aurmr_setup.cli.workspace import Workspace
from aurmr_setup.cli.workspace import get_all_workspaces

#@cli.group()
#def workspace():
#    pass


@cli.command()
@click.option('--workspace_name', prompt="Name of the new workspace")
def init(workspace_name: str):
    """
    Initializes a new and empty workspace
    """
    create_workspace(workspace_name)

def create_workspace(workspace: str):
    if not workspace:
        logger.warning('No workspace selected')
        sys.exit(1)
    workspace = Workspace.create(workspace_name)
    if not workspace:
        logger.error('Unable to create workspace %s', workspace_name)
        sys.exit(1)



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
    with open(os.path.expanduser(ACTIVE_WORKSPACE), 'w') as f:
        f.write(workspace)

@cli.command()
@choice_option('--workspace', type=click.Choice(get_all_workspaces()))
def remove_workspace(workspace):
    """
    Removes a workspace
    """
    from shutil import rmtree
    if questionary.confirm(f'Do you really want to remove the workspace {workspace}', default=False).ask():
        cmd = f'conda env remove -n {workspace}'
        subprocess.run(cmd, check=True, shell=True)
        workspace_full_path = os.path.join(WORKSPACE_DIR, workspace)
        workspace_full_path = os.path.expanduser(workspace_full_path)
        rmtree(workspace_full_path)


def get_active_workspace():
    workspace_name = os.environ.get('WORKSPACE_NAME', None)
    return workspace_name


@choice_option('--clone-from-workspace', type=click.Choice(get_all_workspaces()))
@click.argument('new-workspace-name')
@cli.command()
def clone(clone_from_workspace: str, new_workspace_name: str):
    """
    Clone an existing workspace.
    """
    if not clone_from_workspace:
        logger.warning('No workspace selected')
        sys.exit(1)

    workspace_full_path = os.path.join(WORKSPACE_DIR, new_workspace_name)
    workspace_full_path = os.path.expanduser(workspace_full_path)
    if os.path.exists(workspace_full_path):
        logger.error('Workspace already exists %s', workspace_full_path)
        sys.exit(1)

    cmd = ['conda', 'create', '--clone', clone_from_workspace, '-n', new_workspace_name]
    subprocess.run(cmd, check=True)

    clone_workspace_full_path = os.path.join(WORKSPACE_DIR, clone_from_workspace)
    clone_workspace_full_path = os.path.expanduser(clone_workspace_full_path)
    clone_workspace_full_path = clone_workspace_full_path + '/'

    cmd = ['rsync', '-av', '-P', '--exclude=build', '--exclude=devel',
            '--exclude=logs', clone_workspace_full_path, workspace_full_path]
    subprocess.run(cmd, check=True)

    #cmd = ['catkin', 'build']
    #subprocess.run(cmd, check=True, cwd=workspace_full_path)

    print("Missing steps: 1.) activate the workspace 2.) Run catkin build 3.) reopen terminal and activate workspace again")

    print('Done. Please close the terminal and activate the workspace again')



def get_all_ros_packages():
    from . import robostack_utils
    return robostack_utils.packages
    """
    import pandas as pd
    df = pd.read_html('https://robostack.github.io/noetic.html')[0]
    return list(df.Package)
    """

def get_all_src_packages():
    return ['git@github.com:au-rmr/aurmr_tahoma.git',
            'git@github.com:au-rmr/aurmr_inventory.git',
            'git@github.com:au-rmr/aurmr-dataset.git']


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
    cmd = ['mamba', 'install', package]
    subprocess.run(cmd, check=True)


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

    workspace_full_path = os.path.join(WORKSPACE_DIR, workspace_name, 'src')
    workspace_full_path = os.path.expanduser(workspace_full_path)

    url = package
    branch = 'main'

    cmd = ['git', 'clone', '-b', branch, url]
    subprocess.run(cmd, check=True, cwd=workspace_full_path)



@cli.command()
def update():
    """
    Updates all git repositories within a workspace
    """
    workspace_name = get_active_workspace()
    if not workspace_name:
        logger.error('Select a workspace first')
        sys.exit(1)

    workspace_full_path = os.path.join(WORKSPACE_DIR, workspace_name, 'src')
    workspace_full_path = os.path.expanduser(workspace_full_path)

    for r in os.listdir(workspace_full_path):
        r = os.path.join(workspace_full_path, r)
        if os.path.isdir(os.path.join(r, '.git')):
            cmd = ['git', 'pull', '-r']
            subprocess.run(cmd, check=True, cwd=r)
    
