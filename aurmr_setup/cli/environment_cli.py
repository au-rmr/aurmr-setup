import sys
import logging
import subprocess
import rich_click as click

from click_prompt import choice_option
from click_prompt import auto_complete_option

from aurmr_setup.core.workspace import Workspace
from aurmr_setup.core.workspace import get_active_workspace

from aurmr_setup.cli.main_cli import cli
from aurmr_setup.cli.utils import find_and_install_missing_packages


logger = logging.getLogger(__name__)


def get_all_ros_packages():
    """
    import pandas as pd
    df = pd.read_html('https://robostack.github.io/noetic.html')[0]
    return list(df.Package)
    """
    misc = ["catkin_tools", "rosdep"]
    from aurmr_setup.utils import robostack_utils

    return robostack_utils.packages + misc


@cli.command()
@auto_complete_option("--package", choices=get_all_ros_packages())
def add(package: str):
    """
    Installs a conda package to an activate workspace. Similar to `conda
    install` but with auto completion for robostack.
    """
    workspace_name = get_active_workspace()
    if not workspace_name:
        logger.error("Select a workspace first")
        sys.exit(1)
    workspace = Workspace(workspace_name)
    workspace.install(package)

    try:
        find_and_install_missing_packages(workspace)
    except subprocess.CalledProcessError as ex:
        logging.error("Unable to install package %s. Exception is %s", package, ex)
