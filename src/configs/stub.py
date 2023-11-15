from pydantic import BaseModel
from .base import BaseConfig, BaseGitHubConfig
from .telegram import TelegramGeneralBot


class StubProject(BaseConfig):
    project_name = "stub_project"
    github = BaseGitHubConfig(github_url_path="stub.git", pat_token="stub", clone_path="./")
    telegram = TelegramGeneralBot()
