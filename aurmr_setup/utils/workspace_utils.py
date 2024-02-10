import logging
import os

from typing import List

from aurmr_setup.core.workspace import Workspace
from aurmr_setup.core.workspace import get_active_workspace
from aurmr_setup.core.config import system_config

from aurmr_setup.utils import robostack_utils
from aurmr_setup.utils import environment_utils

logger = logging.getLogger(__name__)


def get_active_workspace_path() -> str:
    workspace_name = get_active_workspace()
    if workspace_name:
        return Workspace(workspace_name).full_path

def get_all_workspaces() -> List[str]:
    workspace_dir = os.path.expanduser(system_config.workspace_path)
    if not os.path.isdir(workspace_dir):
        logger.error(
            "Workspace folder does not exists. Please create %s", workspace_dir
        )
        return []
    return [
        workspace
        for workspace in sorted(os.listdir(workspace_dir))
        if os.path.isdir(os.path.join(workspace_dir, workspace))
        and not workspace == system_config.ARCHIVE_DIRNAME
    ]


def get_archived_workspaces() -> List[str]:
    if not os.path.isdir(system_config.archive_path):
        logger.error("Archive folder does not exists. Please create %s", system_config.archive_path)
        return []
    return [
        workspace
        for workspace in sorted(os.listdir(system_config.archive_path))
        if os.path.isdir(os.path.join(system_config.archive_path, workspace))
    ]


def find_and_install_missing_packages(workspace: Workspace) -> List[str]:
    import questionary
    required_packages = environment_utils.get_packages(workspace)
    robostack_packages = [p for p in required_packages if p in robostack_utils.packages]
    missing_packages = [
        p for p in required_packages if p not in robostack_utils.packages
    ]
    if required_packages:
        print(f"Found {len(required_packages)} required packages")
        print("Found required packages on robostack")
        for p in robostack_packages:
            print(f" - {p}")
        print("Unable to find the following packages")
        for p in missing_packages:
            print(f" - {p}")
        if (
            robostack_packages
            and questionary.confirm(
                f"Do you want to install {len(robostack_packages)} packages?"
            ).ask()
        ):
            workspace.install(" ".join(robostack_packages))
