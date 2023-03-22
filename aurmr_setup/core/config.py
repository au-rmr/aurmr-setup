from dataclasses import dataclass


@dataclass
class SystemConfig:
    WORKSPACE_DIR = "~/workspaces/"
    ACTIVE_WORKSPACE = "~/.active_workspace"
    ARCHIVE_DIR = "archive"
    ENVIRONMENT_FILE = "environment.yml"


@dataclass
class WorkspaceConfig:
    rosdistro: str = "noetic"


system_config = SystemConfig()
