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
from rich.progress import Progress
import questionary

import system_scripts
import user_scripts

from rich.logging import RichHandler
from rich.console import Console

from click_prompt import confirm_option
from click_prompt import choice_option

console = Console()



logger = logging.getLogger(__name__)

WORKSPACE_DIR = '~/workspaces/'
ACTIVE_WORKSPACE = '~/.active_workspace'

@click.group()
@click.option("--verbose", "-v", default=False, count=True,
              help="Increase verbosity of the logging output. Can base used multiple times")
@click.option("--quiet", "-q", default=False, is_flag=True,
              help="Suppress all logging output except critical messages")
def cli(**kwargs):
    """
    aurmr command line interface
    """
    log_config = {'handlers': [RichHandler(console=console, markup=True, rich_tracebacks=True)]}
    if kwargs['verbose'] and kwargs['quiet']:
        logger.error('verbose and quiet must be mutually exclusive')
        sys.exit(-1)
    elif kwargs['verbose'] == 1:
        logging.basicConfig(level=logging.INFO, **log_config)
    elif kwargs['verbose'] == 2:
        logging.basicConfig(level=logging.DEBUG, **log_config)
    elif kwargs['verbose'] >= 3:
        logging.basicConfig(level=logging.NOTSET, **log_config)
    elif kwargs['quiet']:
        logging.basicConfig(level=logging.CRITICAL, **log_config)
    else:
        logging.basicConfig(level=logging.INFO, **log_config)


#@cli.group()
#def system():
#    pass
#
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
    workspace_full_path = os.path.join(WORKSPACE_DIR, workspace)
    workspace_full_path = os.path.expanduser(workspace_full_path)
    if os.path.exists(workspace_full_path):
        logger.error('Workspace already exists %s', workspace_full_path)
        sys.exit(1)
    with path(user_scripts, '10_create_new_workspace.sh') as script_full_path:
        subprocess.run([str(script_full_path), workspace], check=True)

@lru_cache(1)
def get_all_workspaces() -> List[str]:
    workspaces = os.path.expanduser(WORKSPACE_DIR)
    if not os.path.isdir(workspaces):
        logger.error('Workspace folder does not exists. Please create %s', workspaces)
        return []
    return [workspace
           for workspace in os.listdir(workspaces)
           if os.path.isdir(os.path.join(workspaces, workspace))]


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
def remove(workspace):
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

@lru_cache(1)
def get_user_scripts() -> List[str]:
    scripts = [os.path.splitext(s)[0]
               for s in files(user_scripts)
               if s.endswith('.sh')]
    return sorted(scripts)


@cli.command()
@choice_option('--software', multiple=True, type=click.Choice(get_user_scripts()))
@choice_option('--workspace', type=click.Choice(get_all_workspaces() + ['new']))
def install(software: str, workspace: str):
    """
    Installs software for a given workspace
    """
    select_workspace(workspace)

    if not questionary.confirm(f'Do you really want to run these scripts: {software}', default=False).ask():
        sys.exit(1)

    with Progress(console=console) as progress:
        for script_name in progress.track(software):
            script = f'{script_name}.sh'
            my_env = os.environ.copy()
            my_env['WORKSPACE_NAME'] = workspace
            task = progress.add_task(f'Installing {script_name}', total=None)
            with path(user_scripts, script) as script_full_path:
                logger.info('Running %s', script_full_path)
                subprocess.run(str(script_full_path), check=True, env=my_env)
            progress.update(task, total=1.0, completed=1.0)


def get_active_workspace():
    workspace_name = os.environ.get('WORKSPACE_NAME', None)
    return workspace_name

@cli.command()
def run():
    pass
 

@cli.command()
def update():
    """
    Updates the git repositories within a workspace
    """
    workspace_name = get_active_workspace()
    if not workspace_name:
        logger.error('Select a workspace first')
        sys.exit(1)

    workspace_full_path = os.path.join(WORKSPACE_DIR, workspace_name, 'src')
    workspace_full_path = os.path.expanduser(workspace_full_path)

    for r in os.listdir(workspace_full_path):
        if os.path.isdir(os.path.join(r, '.git')):
            cmd = ['git', 'pull', '-r']
            subprocess.run(cmd, check=True)
    
@lru_cache(1)
def get_system_scripts() -> List[str]:
    scripts = [os.path.splitext(s)[0]
               for s in files(system_scripts)
               if s.endswith('.sh')]
    return sorted(scripts)

@cli.command()
@choice_option('--software', multiple=True, type=click.Choice(get_system_scripts()))
def system_prepare(software: str):
    """
    Configures the system. Usually these scripts needs to be only run once
    """
    if not questionary.confirm(f'Do you really want to run these scripts: {software}', default=False).ask():
        sys.exit(1)
    for script_name in software:
        logger.info('Running script %s', script_name)
        script = f'{script_name}.sh'
        with path(system_scripts, script) as script_full_path:
            logger.info('Running %s', script_full_path)
            subprocess.run(script_full_path, check=True)
