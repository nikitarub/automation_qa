from pydantic import BaseModel
from .base import BaseConfig, BaseGitHubConfig
from .telegram import TelegramGeneralBot


class TargetProject(BaseConfig):
    project_name = "target_test_project"
    version_file = f"version.json"
    github = BaseGitHubConfig(github_url_path="nikitarub/automation_qa_target.git", clone_path=f"./{project_name}")
    telegram = TelegramGeneralBot()

