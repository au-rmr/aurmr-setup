import os
import sys
import logging

import subprocess
import json

from importlib.resources import contents as files
from importlib.resources import path

from typing import List

import rich_click as click
import questionary

import system_scripts
import user_scripts

from rich.logging import RichHandler

logger = logging.getLogger(__name__)

WORKSPACE_DIR = '~/workspaces/'
ACTIVE_WORKSPACE = '~/.active_workspace'

class QuestionaryCheckbox(click.Option):
    """
    Prompts user the option

    ..see::
    https://stackoverflow.com/questions/54311067/using-a-numeric-identifier-for-value-selection-in-click-choice
    """
    def __init__(self, param_decls=None, **attrs):
        click.Option.__init__(self, param_decls, **attrs)
        if not isinstance(self.type, click.Choice):
            raise Exception('ChoiceOption type arg must be click.Choice')

    def prompt_for_value(self, ctx):
        if len(self.type.choices) == 1:
            return self.type.choices[0]
        choices = questionary.checkbox(self.prompt, choices=self.type.choices).unsafe_ask()
        return ','.join(choices)


class QuestionaryChoice(click.Option):
    """
    Prompts user the option

    ..see::
    https://stackoverflow.com/questions/54311067/using-a-numeric-identifier-for-value-selection-in-click-choice
    """
    def __init__(self, param_decls=None, **attrs):
        click.Option.__init__(self, param_decls, **attrs)
        if not isinstance(self.type, click.Choice):
            raise Exception('ChoiceOption type arg must be click.Choice')

    def prompt_for_value(self, ctx):
        if len(self.type.choices) == 1:
            return self.type.choices[0]
        return questionary.select(self.prompt, choices=self.type.choices).unsafe_ask()



@click.group()
@click.option("--verbose", "-v", default=False, count=True,
              help="Increase verbosity of the logging output. Can base used multiple times")
@click.option("--quiet", "-q", default=False, is_flag=True,
              help="Suppress all logging output except critical messages")
def cli(**kwargs):
    """
    aurmr command line interface
    """
    log_config = {'handlers': [RichHandler()]}
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
@click.argument('workspace_name', type=str)
def init(workspace_name):
    """
    Initializes a new and empty workspace
    """
    workspace_full_path = os.path.join(WORKSPACE_DIR, workspace_name)
    workspace_full_path = os.path.expanduser(workspace_full_path)
    if os.path.exists(workspace_full_path):
        logger.error('Workspace already exists %s', workspace_full_path)
        sys.exit(1)
    create_workspace(workspace_name)

def create_workspace(workspace_name):
    with path(user_scripts, '10_create_new_workspace.sh') as script_full_path:
        cmd = f'{script_full_path} {workspace_name}'
        subprocess.run(cmd, shell=True, check=True)


def get_all_workspaces() -> List[str]:
    workspaces = os.path.expanduser(WORKSPACE_DIR)
    if not os.path.isdir(workspaces):
        logger.error('Workspace folder does not exists. Please create %s', workspaces)
        return []
    return [w for w in os.listdir(workspaces) if os.path.isdir(os.path.join(workspaces, w))]


@cli.command()
@click.option('--workspace', prompt=True, type=click.Choice(get_all_workspaces() + ['new']), cls=QuestionaryChoice)
def select(workspace: str):
    """
    Selects a workspace. Typically you want to run `activate` in your shell
    """
    if workspace == 'new':
        workspace = questionary.text('Name of the new workspace:').ask()
        if not workspace:
            print('No workspace selected')
            sys.exit(1)
        create_workspace(workspace)
    with open(os.path.expanduser(ACTIVE_WORKSPACE), 'w') as f:
        f.write(workspace)

@cli.command()
@click.option('--workspace', prompt=True, type=click.Choice(get_all_workspaces()), cls=QuestionaryChoice)
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


def get_user_scripts() -> List[str]:
    scripts =  [os.path.splitext(s)[0]
                for s in files(user_scripts)
                if s.endswith('.sh')]
    return sorted(scripts)


@cli.command()
@click.option('--software', prompt=True, type=click.Choice(get_user_scripts()), cls=QuestionaryCheckbox)
@click.option('--workspace', prompt=True, type=click.Choice(get_all_workspaces()), cls=QuestionaryChoice)
def install(software: str, workspace: str):
    """
    Installs software for a given workspace
    """
    if not questionary.confirm(f'Do you really want to run these scripts: {software}', default=False).ask():
        sys.exit(1)
    for script_name in software.split(','):
        logger.info('Running script %s', script_name)
        script = f'{script_name}.sh'
        with path(user_scripts, script) as script_full_path:
            subprocess.run(script_full_path, check=True)

def get_active_workspace():
    workspace_name = os.environ.get('WORKSPACE_NAME', None)
    return workspace_name
 

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
    

def get_system_scripts() -> List[str]:
    scripts =  [os.path.splitext(s)[0]
                for s in files(system_scripts)
                if s.endswith('.sh')]
    return sorted(scripts)

@cli.command()
@click.option('--software', prompt=True, type=click.Choice(get_system_scripts()), cls=QuestionaryCheckbox)
def system_prepare(software: str):
    """
    Configures the system. Usually these scripts needs to be only run once
    """
    if not questionary.confirm(f'Do you really want to run these scripts: {software}', default=False).ask():
        sys.exit(1)
    for script_name in software.split(','):
        logger.info('Running script %s', script_name)
        script = f'{script_name}.sh'
        with path(system_scripts, script) as script_full_path:
            subprocess.run(script_full_path, check=True)
