from pydantic import BaseModel, ValidationError, validator
from typing import Optional


class BaseGitHubConfig(BaseModel):
    github_url_path: str
    clone_path: str

    @validator('github_url_path')
    def github_url_path__must_end_with_dot_git(cls, v):
        if not v.endswith(".git"):
            raise ValueError(f'github_url_path "{v}" must end with ".git", like: {v}.git')
        return v


class BaseTelegramConfig(BaseModel):
    report_chat_id: str
    token: str


class BaseConfig(BaseModel):
    project_name: str 
    github: BaseGitHubConfig
    telegram: BaseTelegramConfig
