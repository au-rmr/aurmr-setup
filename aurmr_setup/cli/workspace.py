from typing import List

import os

import logging

from functools import lru_cache

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


