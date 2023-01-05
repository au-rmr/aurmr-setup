from typing import List

import os
import subprocess

import logging

from functools import lru_cache
from importlib.resources import path

import user_scripts



logger = logging.getLogger(__name__)

WORKSPACE_DIR = '~/workspaces/'

@lru_cache(1)
def get_all_workspaces() -> List[str]:
    workspaces = os.path.expanduser(WORKSPACE_DIR)
    if not os.path.isdir(workspaces):
        logger.error('Workspace folder does not exists. Please create %s', workspaces)
        return []
    return [workspace
           for workspace in os.listdir(workspaces)
           if os.path.isdir(os.path.join(workspaces, workspace))]


class Workspace:

    workspace_name: str

    @classmethod
    def create(cls, name: str) -> 'Workspace':
        workspace_full_path = os.path.join(WORKSPACE_DIR, name)
        workspace_full_path = os.path.expanduser(workspace_full_path)
        if os.path.exists(workspace_full_path):
            return None

        with path(user_scripts, '10_create_new_workspace.sh') as script_full_path:
            subprocess.run([str(script_full_path), workspace], check=True)
            # ..excute setup script

        return Workspace(workspace_name=name)

    @classmethod
    def list(cls) -> List['Workspace']:
        return [Workspace(w) for w in get_all_workspaces()]

    @classmethod
    def activate(cls) -> 'Workspace':
        pass

    def __str__(self):
        return self.workspace_name


    def remove(self):
        pass
