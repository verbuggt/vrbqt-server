import configparser
import os
import pathlib
import subprocess

from fastapi import HTTPException
from starlette import status

from gunter.schemas import Repositories

_vit_conf = configparser.ConfigParser()
_vit_conf.read('gunter/gunter_config.toml')

git_root: str = _vit_conf.get('gunter', 'git_root')
scripts_path = "gunter/git_scripts/{0}.tmpsh"


# TODO hack this for fun, fix later
def get_script(script_name: str, template_values: dict) -> list:
    # check if requested script exists
    if not pathlib.Path(scripts_path.format(script_name)).exists():
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal files missing")

    # read script and supply variables
    script_lines = open(scripts_path.format(script_name)).readlines()
    for i in range(len(script_lines)):
        for template_field in template_values.keys():
            script_lines[i] = script_lines[i].format(**{template_field: template_values.get(template_field)})

    return script_lines


def get_repositories() -> list:
    repos: [] = os.listdir(git_root)
    # TODO sort??!
    repos.sort()
    r_info = []
    for repo in repos:
        r_info.append(get_files(repo, "master"))
    return repos


def create_repo(repository_name: str):
    sh = get_script("create_repository", {"repository_name": repository_name})
    result = subprocess.run(sh,  shell=True, cwd=git_root, capture_output=True)
    return result.stdout


def get_files(repository_name: str, branch: str):
    working_directory = git_root + repository_name
    sh = get_script("get_files", {'branch': branch})
    result = subprocess.run(sh, shell=True, cwd=working_directory, capture_output=True)
    return str(result.stdout, "utf-8").strip().replace("\t", " ").split("\n")


def get_commits(repository_name: str) -> list:
    working_directory = git_root + repository_name
    result = subprocess.run(get_script("get_commits", {}), shell=True, cwd=working_directory, capture_output=True)
    return str(result.stdout, "utf-8").strip().split("\n")


def is_empty(repository_name: str) -> bool:
    working_directory = git_root + repository_name
    result = subprocess.run(get_script("get_branches", {}), shell=True, cwd=working_directory, capture_output=True, text=True)
    return len(result.stdout) == 0


def exists(repository_name: str) -> bool:
    return pathlib.Path(git_root, repository_name).exists()
