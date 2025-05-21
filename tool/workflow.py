import os
import sys
import json
import subprocess
import re
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("workflow")


class Workflow:
    def __init__(self, working_dir):
        self.working_dir = working_dir
        if not self._command_exists("gh"):
            logger.error("GitHub CLI (gh) is not installed. Please install it first:")
            logger.error("https://cli.github.com/manual/installation")
            sys.exit(1)
        try:
            self.run(["gh", "auth", "status"])
        except subprocess.CalledProcessError:
            logger.error("Please authenticate with GitHub first using: gh auth login")
            sys.exit(1)

    def _command_exists(self, cmd):
        return (
            subprocess.call(
                ["which", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            == 0
        )

    def run(self, cmd, check=True):
        logger.info(f"Running: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
            cwd=self.working_dir,
        )
        output_stdout = result.stdout.strip()
        output_stderr = result.stderr.strip()
        logger.info(f"Output: {output_stdout}")
        logger.info(f"Error: {output_stderr}")
        if check and result.returncode != 0:
            logger.error(f"Command failed with exit code {result.returncode}")
            raise subprocess.CalledProcessError(
                result.returncode, cmd, output_stdout, output_stderr
            )
        output = (output_stdout + "\n" + output_stderr).strip()
        max_output_length = 50000
        if len(output) > max_output_length:
            truncated = output[:max_output_length]
            logger.info(
                f"Output truncated from {len(output)} to {max_output_length} characters"
            )
            return truncated + "\n... [output truncated]"
        return output


def list_issues(config) -> str:
    workflow_dir = config.project_dir
    workflow_obj = Workflow(workflow_dir)
    issues_json = workflow_obj.run(
        [
            "gh",
            "issue",
            "list",
            "--state",
            "open",
            "--json",
            "number,title,labels,createdAt",
            "--limit",
            "100",
        ]
    )
    return issues_json


def start_issue(issue_number: int, config) -> str:
    workflow_dir = config.project_dir
    workflow_obj = Workflow(workflow_dir)
    issue_json = workflow_obj.run(
        ["gh", "issue", "view", str(issue_number), "--json", "number,title,body"]
    )
    issue_title = json.loads(issue_json).get("title", "")
    branch_type = "feature" if issue_title.startswith("[feature]") else "fix"
    workflow_obj.run(["git", "fetch", "origin"])
    workflow_obj.run(["git", "reset", "--hard", "origin/master"])
    workflow_obj.run(["git", "clean", "-fd"])
    branch_name = f"{branch_type}/issue-{issue_number}"
    workflow_obj.run(["git", "checkout", "-b", branch_name])
    workflow_obj.run(["git", "push", "-u", "origin", branch_name])
    return issue_json


def change_summary(config) -> str:
    workflow_dir = config.project_dir
    workflow_obj = Workflow(workflow_dir)
    status = workflow_obj.run(["git", "status", "--short"])
    diff_stat = workflow_obj.run(["git", "diff", "--stat"])
    result = {
        "status": status,
        "diff_stat": diff_stat,
        "diff": diff_stat,
    }
    return json.dumps(result)


def commit_and_push(commit_message: str, config) -> str:
    workflow_dir = config.project_dir
    workflow_obj = Workflow(workflow_dir)
    branch_name = workflow_obj.run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    workflow_obj.run(["git", "add", "."])
    workflow_obj.run(["git", "commit", "-m", commit_message], check=False)
    workflow_obj.run(["git", "push", "-u", "origin", branch_name])
    try:
        pr_json = workflow_obj.run(["gh", "pr", "view", "--json", "number"])
        pr_data = json.loads(pr_json)
        pr_number = pr_data.get("number")
        if pr_number:
            try:
                workflow_obj.run(["gh", "pr", "checks", str(pr_number), "--watch"])
            except:
                pass
    except:
        pass
    commit_info = workflow_obj.run(["git", "log", "-1", "--pretty=format:%h %s"])
    result = {"branch": branch_name, "commit": commit_info, "message": commit_message}
    return json.dumps(result)


def complete_issue(config) -> str:
    workflow_dir = config.project_dir
    workflow_obj = Workflow(workflow_dir)
    branch_name = workflow_obj.run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    issue_match = re.search(r"issue-(\d+)", branch_name)
    issue_number = issue_match.group(1) if issue_match else "unknown"
    try:
        pr_json = workflow_obj.run(["gh", "pr", "view", "--json", "number"])
        pr_data = json.loads(pr_json)
        pr_number = pr_data.get("number")
    except:
        workflow_obj.run(
            [
                "gh",
                "pr",
                "create",
                "--title",
                f"Fix #{issue_number}",
                "--body",
                f"Closes #{issue_number}",
                "--head",
                branch_name,
            ]
        )
        pr_json = workflow_obj.run(["gh", "pr", "view", "--json", "number"])
        pr_data = json.loads(pr_json)
        pr_number = pr_data.get("number")
    try:
        workflow_obj.run(["gh", "pr", "checks", str(pr_number), "--watch"])
    except:
        pass
    workflow_obj.run(["gh", "pr", "merge", str(pr_number), "--merge"])
    workflow_obj.run(["git", "checkout", "master"])
    workflow_obj.run(["git", "pull"])
    result = {
        "branch": branch_name,
        "issue_number": issue_number,
        "status": "completed",
    }
    return json.dumps(result)
