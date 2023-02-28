import questionary

from aurmr_setup.core.workspace import Workspace

from aurmr_setup.cli.main_cli import console

from aurmr_setup.utils.environemnt_utils import find_required_dependencies
from aurmr_setup.utils.environemnt_utils import filter_packages

def find_and_install_missing_packages(workspace: Workspace):
    required_packages = find_required_dependencies(workspace)
    installable_packages, missing_packages = filter_packages(required_packages)
    if required_packages:
        console.print(f'Found {len(required_packages)} required packages')
        console.print('Found required packages on robostack')
        for p in installable_packages:
            console.print(f' - {p}')
        console.print('Unable to find the following packages')
        for p in missing_packages:
            console.print(f' - {p}')
        if installable_packages and questionary.confirm(f'Do you want to install {len(installable_packages)} packages?').ask():
            workspace.install(' '.join(installable_packages))


