from dataclasses import dataclass


@dataclass
class WorkspaceConfig:

    rosdistro: str = 'noetic'

