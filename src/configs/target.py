from pydantic import BaseModel
from .base import BaseConfig, BaseGitHubConfig
from .telegram import TelegramGeneralBot
import os


class TargetProject(BaseConfig):
    project_name = "target_test_project"
    version_file = f"version.json"
    pat_token = os.getenv("GITHUB_PAT_TOKEN")
    github = BaseGitHubConfig(github_url_path="nikitarub/automation_qa_target.git", pat_token=pat_token, clone_path=f"./{project_name}")
    telegram = TelegramGeneralBot()

