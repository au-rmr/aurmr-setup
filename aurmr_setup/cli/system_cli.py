from typing import List
import logging
import os
import subprocess

from functools import lru_cache

import rich_click as click
from importlib.resources import contents as files
from importlib.resources import path


from click_prompt import choice_option

from aurmr_setup.core.workspace import Workspace
from aurmr_setup.core.workspace import get_active_workspace
from aurmr_setup.core.config import system_config
from aurmr_setup.core.system_control import ProcessMonitor

from aurmr_setup.cli.main_cli import cli
from aurmr_setup.cli.main_cli import console


logger = logging.getLogger(__name__)


import launch_scripts


@lru_cache(1)
def get_launch_scripts() -> List[str]:
    scripts = [
        os.path.splitext(s)[0] for s in files(launch_scripts) if s.endswith(".sh")
    ]
    return sorted(scripts)


@cli.command()
@choice_option("--script", multiple=False, type=click.Choice(get_launch_scripts()))
def start(script: str):

    logger.info("Running script %s", script)
    script = f"{script}.sh"
    with path(launch_scripts, script) as script_full_path:
        logger.info("Running %s", script_full_path)
        subprocess.run(script_full_path, check=True)


@cli.command()
def stop():
    monitor = ProcessMonitor()
    for p in monitor.terminate(system_config.conda_env_dir):
        console.print(p)
    for p in monitor.kill(system_config.conda_env_dir):
        console.print(p)


@cli.command()
def status():

    monitor = ProcessMonitor()

    for p in monitor.status(system_config.conda_env_dir):
        console.print(p)
