from dataclasses import dataclass


@dataclass
class WorkspaceConfig:

    ros_distro: str = 'noetic'

