import os
import logging
from functools import lru_cache
from typing import List

import subprocess


from importlib.resources import contents as files
from importlib.resources import path

import system_scripts
import user_scripts

logger = logging.getLogger(__name__)


class Recipe:

    def __init__(self, category, script_name: str):
        self.category = category
        self.script_name = script_name

    @classmethod
    @lru_cache(2)
    def list_all(cls, category) -> List['Recipe']:
        scripts = [os.path.splitext(s)[0]
                   for s in files(category)
                   if s.endswith('.sh')]
        scripts = [Recipe(category, s) for s in scripts]
        return sorted(scripts)

    def execute(self, workspace=None):
        script = f'{self.script_name}.sh'
        my_env = os.environ.copy()
        if workspace:
            my_env['WORKSPACE_NAME'] = workspace.workspace_name
        with path(self.category, script) as script_full_path:
            logger.info('Running %s', script_full_path)
            return subprocess.run(str(script_full_path), check=True, env=my_env)

    def __str__(self):
        return f'{self.script_name}'


class UserRecipe(Recipe):

    @classmethod
    def all_user_scripts(cls):
        return Recipe.list_all(user_scripts)

    @classmethod
    def all_user_scripts_str(cls):
        return [str(r)
                for r in UserRecipe.all_user_scripts()]

class SystemRecipe(Recipe):

    @classmethod
    def all_system_scripts(cls):
        return Recipe.list_all(system_scripts)


    @classmethod
    def all_system_scripts_str(cls):
        return [str(r) 
                for r in SystemRecipe.all_system_scripts()]
