from typing import List

import os
import subprocess

import logging

from functools import lru_cache
from importlib.resources import path

import user_scripts

logger = logging.getLogger(__name__)

WORKSPACE_DIR = '~/workspaces/'
ACTIVE_WORKSPACE = '~/.active_workspace'

@lru_cache(1)
def get_all_workspaces() -> List[str]:
    workspaces = os.path.expanduser(WORKSPACE_DIR)
    if not os.path.isdir(workspaces):
        logger.error('Workspace folder does not exists. Please create %s', workspaces)
        return []
    return [workspace
           for workspace in os.listdir(workspaces)
           if os.path.isdir(os.path.join(workspaces, workspace))]

def get_active_workspace():
    workspace_name = os.environ.get('WORKSPACE_NAME', None)
    return workspace_name

class Workspace:

    def __init__(self, workspace_name: str):
        self.workspace_name = workspace_name

    @property
    def full_path(self):
        workspace_full_path = os.path.join(WORKSPACE_DIR, self.workspace_name)
        workspace_full_path = os.path.expanduser(workspace_full_path)
        return workspace_full_path

    @property
    def src_path(self):
        return os.path.join(self.full_path, 'src')

    @classmethod
    def create(cls, name: str, python_version: str = '3.8') -> 'Workspace':
        if Workspace(name).exists():
            logger.error('Workspace already exists')
            return None

        with path(user_scripts, '10_create_new_workspace.sh') as script_full_path:
            subprocess.run([str(script_full_path), name, python_version], check=True)
            # ..excute setup script

        return Workspace(workspace_name=name)

    @classmethod
    def list(cls) -> List['Workspace']:
        return [Workspace(w) for w in sorted(get_all_workspaces())]

    def activate(self) -> None:
        with open(os.path.expanduser(ACTIVE_WORKSPACE), 'w') as f:
            f.write(str(self.workspace_name))


    def clone(self, other):
        pass

    def exists(self) -> bool:
        return os.path.exists(self.full_path)

    def remove(self):
        from shutil import rmtree
        cmd = f'conda env remove -n {self.workspace_name}'
        subprocess.run(cmd, check=True, shell=True)
        rmtree(self.full_path)

    def __str__(self):
        return self.workspace_name
