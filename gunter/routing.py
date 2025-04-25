from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.requests import Request

from gunter import git_bridge, validator
from gunter.schemas import Repositories

gunter_router = APIRouter(
    prefix="/gunter",
    tags=["gunter"],
    dependencies=[],
    responses={404: {"warning": "Not found"}}
)


@gunter_router.get("/")
async def gunter_index(request: Request):
    return {
        "app": "gunter",
        "version": "0.0",
        "status": "omfg this uses shell commands. dont test it PLEASE... at least tell me what u find ._.",
        "contact": "TS3: vrbqt.de, matrix: @vrbqt:vrbqt.de, email: buq@vrbqt.de",
        "author": "verbuqqt",
    }


# crate a repository
@gunter_router.get("/create_repository")
async def create_repo(request: Request, repository_name: str):
    validator.validate(repository_name, extended=True)
    if git_bridge.exists(repository_name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="repository already exists")
    if not repository_name.endswith(".git"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid parameter")
    # raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="unsecured service has been disabled")
    return git_bridge.create_repo(repository_name)


# List of repositories
# TODO differentiate between public/private access
@gunter_router.get("/r", response_model=Repositories)
async def repo_list(request: Request):
    return Repositories(repositories=git_bridge.get_repositories())


@gunter_router.get("/r/{repository_name}")
async def get_repository(request: Request, repository_name: str, branch: str = "master"):
    validator.validate(repository_name, extended=True)
    validator.validate(branch)
    if not git_bridge.exists(repository_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="repo not found")
    if git_bridge.is_empty(repository_name):
        return None
    return {
        "files": git_bridge.get_files(repository_name, branch),
        "commits": git_bridge.get_commits(repository_name)
    }


@gunter_router.get("/r/{repository_name}/commits")
async def get_commits(request: Request, repository_name: str):
    validator.validate(repository_name, extended=True)
    if not git_bridge.exists(repository_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="repo not found")
    if git_bridge.is_empty(repository_name):
        return None
    return git_bridge.get_commits(repository_name)


@gunter_router.get("/r/{repository_name}/files")
async def get_files(request: Request, repository_name: str, branch: str = "HEAD"):
    validator.validate(repository_name, extended=True)
    validator.validate(branch)
    if not git_bridge.exists(repository_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="repo not found")
    if git_bridge.is_empty(repository_name):
        return None
    return git_bridge.get_files(repository_name, branch)
