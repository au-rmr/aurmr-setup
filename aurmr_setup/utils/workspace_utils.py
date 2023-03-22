import logging
import os

from typing import List

from aurmr_setup.core.workspace import Workspace
from aurmr_setup.core.config import system_config

from aurmr_setup.utils import robostack_utils
from aurmr_setup.utils import environment_utils

logger = logging.getLogger(__name__)

def get_all_workspaces() -> List[str]:
    workspace_dir = os.path.expanduser(system_config.WORKSPACE_DIR)
    if not os.path.isdir(workspace_dir):
        logger.error('Workspace folder does not exists. Please create %s', workspace_dir)
        return []
    return [workspace
           for workspace in os.listdir(workspace_dir)
           if os.path.isdir(os.path.join(workspace_dir, workspace))
           and not workspace == system_config.ARCHIVE_DIR]


def get_archived_workspaces() -> List[str]:
    workspace_dir = os.path.expanduser(system_config.WORKSPACE_DIR)
    archive_dir = os.path.join(workspace_dir, system_config.ARCHIVE_DIR)
    if not os.path.isdir(archive_dir):
        logger.error('Archive folder does not exists. Please create %s', archive_dir)
        return []
    return [workspace 
            for workspace in os.listdir(archive_dir)
            if os.path.isdir(os.path.join(archive_dir, workspace))]


def find_and_install_missing_packages(workspace: Workspace) -> List[str]:
    required_packages = environment_utils.get_packages(workspace)
    robostack_packages = [p for p in required_packages if p in robostack_utils.packages]
    missing_packages = [p for p in required_packages if p not in robostack_utils.packages]
    if required_packages:
        print(f'Found {len(required_packages)} required packages')
        print('Found required packages on robostack')
        for p in robostack_packages:
            print(f' - {p}')
        print('Unable to find the following packages')
        for p in missing_packages:
            print(f' - {p}')
        if robostack_packages and questionary.confirm(f'Do you want to install {len(robostack_packages)} packages?').ask():
            workspace.install(' '.join(robostack_packages))


