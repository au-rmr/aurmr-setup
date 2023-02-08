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
ARCHIVE_DIR = 'archive'
ENVIRONMENT_FILE = 'environment.yml'

@lru_cache(1)
def get_all_workspaces() -> List[str]:
    workspace_dir = os.path.expanduser(WORKSPACE_DIR)
    if not os.path.isdir(workspace_dir):
        logger.error('Workspace folder does not exists. Please create %s', workspace_dir)
        return []
    return [workspace
           for workspace in os.listdir(workspace_dir)
           if os.path.isdir(os.path.join(workspace_dir, workspace))
           and not workspace == ARCHIVE_DIR]


@lru_cache(1)
def get_archived_workspaces() -> List[str]:
    workspace_dir = os.path.expanduser(WORKSPACE_DIR)
    archive_dir = os.path.join(workspace_dir, ARCHIVE_DIR)
    if not os.path.isdir(archive_dir):
        logger.error('Archive folder does not exists. Please create %s', archive_dir)
        return []
    return [workspace 
            for workspace in os.listdir(archive_dir)
            if os.path.isdir(os.path.join(archive_dir, workspace))]


def get_active_workspace():
    workspace_name = os.environ.get('WORKSPACE_NAME', None)
    return workspace_name

class Workspace:

    def __init__(self, workspace_name: str, archived: bool=False):
        self.workspace_name = workspace_name
        self.archived = archived

    @property
    def full_path(self):
        if self.archived:
            archive_dir = os.path.join(WORKSPACE_DIR, ARCHIVE_DIR)
            workspace_full_path = os.path.join(archive_dir, self.workspace_name)
        else:
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
        if Workspace(name, True).exists():
            logger.error('Workspace already exists and is archived.')
            return None

        with path(user_scripts, '10_create_new_workspace.sh') as script_full_path:
            subprocess.run([str(script_full_path), name, python_version], check=True)
            # ..excute setup script

        return Workspace(workspace_name=name)

    @classmethod
    def list(cls, list_archived: bool = False) -> List['Workspace']:
        workspaces = [Workspace(w) for w in sorted(get_all_workspaces())]
        if list_archived:
            archives = [Workspace(w, True) for w in sorted(get_archived_workspaces())]
            return archives + workspaces
        else:
            return workspaces

    def activate(self) -> None:
        with open(os.path.expanduser(ACTIVE_WORKSPACE), 'w') as f:
            f.write(str(self.workspace_name))

    def clone(self, other):

        if isinstance(other, str):
            other = Workspace(other)

        if other.exists():
            return None

        cmd = ['conda', 'create', '--clone', self.workspace_name, '-n', other.workspace_name]
        subprocess.run(cmd, check=True)

        cmd = ['rsync', '-av', '-P', '--exclude=build', '--exclude=devel',
                '--exclude=logs', self.full_path + '/', other.full_path]
        subprocess.run(cmd, check=True)

        return other


    def exists(self) -> bool:
        return os.path.exists(self.full_path)

    def remove(self):
        from shutil import rmtree
        cmd = f'conda env remove -n {self.workspace_name}'
        subprocess.run(cmd, check=True, shell=True)
        rmtree(self.full_path)

    def update_src(self):
        for r in os.listdir(self.src_path):
            r = os.path.join(self.full_path, r)
            if os.path.isdir(os.path.join(r, '.git')):
                cmd = ['git', 'pull', '-r']
                subprocess.run(cmd, check=True, cwd=r)


    def import_from_archive(self):
        import shutil

        env_file = os.path.join(self.full_path, ENVIRONMENT_FILE)
        cmd = f'conda env create -f {env_file}'
        subprocess.run(cmd, check=True, shell=True)

        target = os.path.expanduser(WORKSPACE_DIR)
        shutil.move(self.full_path , target)

        self.archived = False

    def move_to_archive(self):
        import shutil

        env_file = os.path.join(self.full_path, ENVIRONMENT_FILE)
        cmd = f'conda env export -n {self.workspace_name} -f {env_file}'
        subprocess.run(cmd, check=True, shell=True)

        target = os.path.join(WORKSPACE_DIR, ARCHIVE_DIR)
        target = os.path.expanduser(target)
        shutil.move(self.full_path , target)

        cmd = f'conda env remove -n {self.workspace_name}'
        subprocess.run(cmd, check=True, shell=True)

        self.archived = True

    def __str__(self):
        return self.workspace_name
