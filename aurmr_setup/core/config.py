from dataclasses import dataclass
import os


@dataclass
class SystemConfig:

    WORKSPACE_PATH = "~/workspaces/"
    ACTIVE_WORKSPACE = "~/.active_workspace"

    # replace with conda config --show envs_dirs
    CONDA_ENV_DIR = "~/miniconda3/envs"

    ARCHIVE_DIRNAME = "archive"
    ENVIRONMENT_FILENAME = "environment.yml"

    @property
    def archive_path(self):
        return os.path.join(self.workspace_path, self.ARCHIVE_DIRNAME)

    @property
    def workspace_path(self):
        return os.path.expanduser(self.WORKSPACE_PATH)

    @property
    def active_workspace_file(self):
        return os.path.expanduser(self.ACTIVE_WORKSPACE)

    @property
    def conda_env_dir(self):
        return os.path.expanduser(self.CONDA_ENV_DIR)


system_config = SystemConfig()


@dataclass
class WorkspaceConfig:

    workspace_name: str

    rosdistro: str = "noetic"

    @property
    def environment_file(self) -> str:
        pass


#        return os.path.join(self.full_path, ENVIRONMENT_FILE)
