import argparse
import os
from dotenv import load_dotenv
from typing import List, Optional


def get_required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} must be set in the environment or .env file.")
    return value


class Config:
    def __init__(
        self,
        jira_url: str,
        jira_username: Optional[str],
        jira_api_token: str,
        jira_is_cloud: Optional[str],
        gh_token: str,
        project_dir: str,
        jira_base_issue: str,
    ):
        self.jira_url = jira_url
        self.jira_username = jira_username
        self.jira_api_token = jira_api_token
        self.jira_is_cloud = jira_is_cloud
        self.gh_token = gh_token
        self.project_dir = project_dir
        self.jira_base_issue = jira_base_issue

    @staticmethod
    def from_env(args):
        if args.env:
            for env_file in args.env:
                load_dotenv(env_file)
        else:
            load_dotenv()
        project_dir = args.project_path or get_required_env("PROJECT_DIR")
        return Config(
            jira_url=get_required_env("JIRA_URL"),
            jira_username=os.getenv("JIRA_USERNAME"),
            jira_api_token=get_required_env("JIRA_API_TOKEN"),
            jira_is_cloud=os.getenv("JIRA_IS_CLOUD"),
            gh_token=get_required_env("GH_TOKEN"),
            project_dir=project_dir,
            jira_base_issue=get_required_env("JIRA_BASE_ISSUE"),
        )


def load_config(argv=None) -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, nargs="*", help="Path(s) to .env file(s)")
    parser.add_argument("--project-path", type=str, help="Path to project root")
    args = parser.parse_args(argv) if argv is not None else parser.parse_args()
    return Config.from_env(args)
