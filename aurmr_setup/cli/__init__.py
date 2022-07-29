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
        return questionary.checkbox(self.prompt, choices=self.type.choices).unsafe_ask()


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
def cli():
    pass


@cli.group()
def system():
    pass

@cli.command()
@click.argument('workspace_name', type=str)
def init(workspace_name):
    workspace_full_path = os.path.join(WORKSPACE_DIR, workspace_name)
    workspace_full_path = os.path.expanduser(workspace_full_path)
    if os.path.exists(workspace_full_path):
        logger.error('Workspace already exists %s', workspace_full_path)
        sys.exit(1)
    create_workspace(workspace_name)

def create_workspace(workspace_name):
    with path(user_scripts, 'create_new_workspace.sh') as script_full_path:
        cmd = f'{script_full_path} {workspace_name}'
        subprocess.run(cmd, shell=True, check=True)


def get_all_workspaces() -> List[str]:
    workspaces = os.path.expanduser(WORKSPACE_DIR)
    return [w for w in os.listdir(workspaces) if os.path.isdir(os.path.join(workspaces, w))]


@cli.command()
@click.option('--workspace', prompt=True, type=click.Choice(get_all_workspaces() + ['new']), cls=QuestionaryChoice)
def select_workspace(workspace: str):
    if workspace == 'new':
        workspace = questionary.text('Name of the new workspace:').ask()
        create_workspace(workspace)
    with open(os.path.expanduser(ACTIVE_WORKSPACE), 'w') as f:
        f.write(workspace)

@cli.command()
def update():
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
    return [os.path.splitext(s)[0]
            for s in files(system_scripts)
            if s.endswith('.sh')]

@system.command()
@click.option('--software', prompt=True, type=click.Choice(get_system_scripts()), cls=QuestionaryCheckbox)
def prepare(software_scripts: List[str]):
    for script_name in software_scripts:
        logger.info('Running script %s', script_name)
        script = f'{script_name}.sh'
        with path(system_scripts, script) as script_full_path:
            subprocess.run(script_full_path, shell=True, check=True)
