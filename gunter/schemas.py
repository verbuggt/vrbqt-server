
from pydantic import BaseModel


class Repository(BaseModel):
    name: str
    branches: list
    commits: list
    files: list


class Repositories(BaseModel):
    repositories: list
