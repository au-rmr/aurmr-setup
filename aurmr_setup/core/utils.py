import os
import subprocess
from aurmr_setup.core.workspace import Workspace

def get_sys_distributor():
    cmd = 'lsb_release -i -s'

def get_sys_codename(): 
    cmd = 'lsb_release -c -s'

def get_packages(workspace: Workspace):
    """
    get list of packages

    we have to manually set the operating system as robostack overwrites it
    """
    packages = []
    cmd = f'rosdep install --ignore-src --from-paths {workspace.full_path} -r -s --os="ubuntu:focal"'
    c = subprocess.run(cmd, check=True, shell=True, capture_output=True)
    s = c.stdout
    lines = s.decode('utf8').split('\n')
    PATTERN = 'sudo -H apt-get install '
    for l in lines:
        if PATTERN in l:
            l = l.rsplit(PATTERN)[-1]
            packages.append(l)
    return packages

