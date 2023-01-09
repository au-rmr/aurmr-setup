import os
import logging
from functools import lru_cache
from typing import List

import subprocess


from importlib.resources import contents as files
from importlib.resources import path


import system_scripts
import user_scripts

import rich_click as click
from rich.progress import Progress

from click_prompt import choice_option

import questionary

from aurmr_setup.cli.main import cli
from aurmr_setup.cli.workspace import get_all_workspaces


logger = logging.getLogger(__name__)

