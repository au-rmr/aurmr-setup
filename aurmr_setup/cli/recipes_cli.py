import sys
import os

from typing import List

import subprocess

import logging

from functools import lru_cache


from importlib.resources import contents as files
from importlib.resources import path

import rich_click as click
from rich.progress import Progress

from click_prompt import choice_option

import questionary

from aurmr_setup.core.workspace import Workspace

from aurmr_setup.cli.main_cli import cli
from aurmr_setup.cli.main_cli import console

import system_scripts
import user_scripts


logger = logging.getLogger(__name__)


@cli.group()
def recipes():
    """
    Excecute recipts to configure the system or the user account
    """
    pass

@lru_cache(1)
def get_system_scripts() -> List['Recipe']:
    scripts = [os.path.splitext(s)[0]
               for s in files(system_scripts)
               if s.endswith('.sh')]
    return sorted(scripts)

@recipes.command()
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



@lru_cache(1)
def get_user_scripts() -> List[str]:
    scripts = [os.path.splitext(s)[0]
               for s in files(user_scripts)
               if s.endswith('.sh')]
    return sorted(scripts)


@recipes.command()
@choice_option('--software', multiple=True, type=click.Choice(get_user_scripts()))
@choice_option('--workspace', type=click.Choice(Workspace.list()))
def user(software: str, workspace: str):
    """
    Installs software from a given recipe, i.e. shell script, to a given workspace
    """

    Workspace(workspace).activate()

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

