from mcp.server.fastmcp import FastMCP
import workflow
import io
import sys
import json
import re
import os
from contextlib import redirect_stdout

mcp = FastMCP("WorkflowMCP")

def get_project_dir(project_name=None):
    """
    Get the project directory based on project name
    
    :param project_name: The basename of the project's root directory.
    """
    if not project_name:
        raise ValueError("Project name must be specified")
    
    # Use project_name as a subdirectory of /project
    return os.path.join("/project", project_name)

@mcp.tool()
def list_issues(project_name: str) -> str:
    """
    List open issues sorted by priority and creation date
    
    :param project_name: The basename of the project's root directory.
    """
    workflow_dir = get_project_dir(project_name)
    workflow_obj = workflow.Workflow(workflow_dir)
    issues_json = workflow_obj.run([
        "gh", "issue", "list",
        "--state", "open",
        "--json", "number,title,labels,createdAt",
        "--limit", "100"
    ])
    return issues_json

@mcp.tool()
def start_issue(issue_number: int, project_name: str) -> str:
    """
    Start work on an issue
    
    :param issue_number: The number of the issue to start work on.
    :param project_name: The basename of the project's root directory.
    """
    workflow_dir = get_project_dir(project_name)
    workflow_obj = workflow.Workflow(workflow_dir)
    
    # Get issue details
    issue_json = workflow_obj.run([
        "gh", "issue", "view", str(issue_number),
        "--json", "number,title,body"
    ])
    
    # Get issue title for branch type
    issue_title = json.loads(issue_json).get("title", "")
    branch_type = "feature" if issue_title.startswith("[feature]") else "fix"
    
    # Reset to clean state
    workflow_obj.run(["git", "fetch", "origin"])
    workflow_obj.run(["git", "reset", "--hard", "origin/master"])
    workflow_obj.run(["git", "clean", "-fd"])
    
    # Create and push branch
    branch_name = f"{branch_type}/issue-{issue_number}"
    workflow_obj.run(["git", "checkout", "-b", branch_name])
    workflow_obj.run(["git", "push", "-u", "origin", branch_name])
    
    return issue_json

@mcp.tool()
def change_summary(project_name: str) -> str:
    """
    Show summary of current changes
    
    :param project_name: The basename of the project's root directory.
    """
    workflow_dir = get_project_dir(project_name)
    workflow_obj = workflow.Workflow(workflow_dir)
    
    status = workflow_obj.run(["git", "status", "--short"])
    
    # Use --stat to get a more concise diff summary instead of the full diff
    diff_stat = workflow_obj.run(["git", "diff", "--stat"])
    
    result = {
        "status": status,
        "diff_stat": diff_stat,
        "diff": diff_stat  # For backward compatibility
    }
    
    return json.dumps(result)

@mcp.tool()
def commit_and_push(commit_message: str, project_name: str) -> str:
    """
    Commit, push changes and monitor CI/CD
    
    :param commit_message: The commit message.
    :param project_name: The basename of the project's root directory.
    """
    workflow_dir = get_project_dir(project_name)
    workflow_obj = workflow.Workflow(workflow_dir)
    
    # Get branch name
    branch_name = workflow_obj.run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    
    # Commit and push
    workflow_obj.run(["git", "add", "."])
    workflow_obj.run(["git", "commit", "-m", commit_message])
    workflow_obj.run(["git", "push", "-u", "origin", branch_name])
    
    # Try to get PR number and monitor CI/CD
    try:
        pr_json = workflow_obj.run(["gh", "pr", "view", "--json", "number"], silent=True)
        pr_data = json.loads(pr_json)
        pr_number = pr_data.get("number")
        
        if pr_number:
            try:
                workflow_obj.run(["gh", "pr", "checks", str(pr_number), "--watch"])
            except:
                pass
    except:
        pass
    
    # Get commit info
    commit_info = workflow_obj.run(["git", "log", "-1", "--pretty=format:%h %s"])
    
    result = {
        "branch": branch_name,
        "commit": commit_info,
        "message": commit_message
    }
    
    return json.dumps(result)

@mcp.tool()
def complete_issue(project_name: str) -> str:
    """
    Complete work on an issue
    
    :param project_name: The basename of the project's root directory.
    """
    workflow_dir = get_project_dir(project_name)
    workflow_obj = workflow.Workflow(workflow_dir)
    
    # Get branch name
    branch_name = workflow_obj.run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    
    # Extract issue number
    issue_match = re.search(r'issue-(\d+)', branch_name)
    issue_number = issue_match.group(1) if issue_match else "unknown"
    
    # Get PR number or create PR
    try:
        pr_json = workflow_obj.run(["gh", "pr", "view", "--json", "number"], silent=True)
        pr_data = json.loads(pr_json)
        pr_number = pr_data.get("number")
    except:
        workflow_obj.run([
            "gh", "pr", "create",
            "--title", f"Fix #{issue_number}",
            "--body", f"Closes #{issue_number}",
            "--head", branch_name
        ])
        pr_json = workflow_obj.run(["gh", "pr", "view", "--json", "number"])
        pr_data = json.loads(pr_json)
        pr_number = pr_data.get("number")
    
    # Monitor CI/CD and merge
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
        "status": "completed"
    }
    
    return json.dumps(result)
