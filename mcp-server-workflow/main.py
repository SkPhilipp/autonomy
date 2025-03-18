from mcp.server.fastmcp import FastMCP
import workflow
import io
import sys
import json
import re
import os
from contextlib import redirect_stdout

# Ensure working directory is set from environment variable
if not os.getenv('WORKFLOW_DIR'):
    raise ValueError("WORKFLOW_DIR environment variable must be set")

mcp = FastMCP("WorkflowMCP")

@mcp.tool()
def list_issues() -> str:
    """List open issues sorted by priority and creation date"""
    workflow_obj = workflow.Workflow(os.getenv('WORKFLOW_DIR'))
    issues_json = workflow_obj.run([
        "gh", "issue", "list",
        "--state", "open",
        "--json", "number,title,labels,createdAt",
        "--limit", "100"
    ])
    return issues_json

@mcp.tool()
def start_issue(issue_number: int) -> str:
    """Start work on an issue"""
    workflow_obj = workflow.Workflow(os.getenv('WORKFLOW_DIR'))
    
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
def change_summary() -> str:
    """Show summary of current changes"""
    workflow_obj = workflow.Workflow(os.getenv('WORKFLOW_DIR'))
    
    status = workflow_obj.run(["git", "status", "--short"])
    diff = workflow_obj.run(["git", "diff"])
    
    result = {
        "status": status,
        "diff": diff
    }
    
    return json.dumps(result)

@mcp.tool()
def commit_and_push(commit_message: str) -> str:
    """Commit, push changes and monitor CI/CD"""
    workflow_obj = workflow.Workflow(os.getenv('WORKFLOW_DIR'))
    
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
def complete_issue() -> str:
    """Complete work on an issue"""
    workflow_obj = workflow.Workflow(os.getenv('WORKFLOW_DIR'))
    
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
    workflow_obj.run(["git", "pull"])
    workflow_obj.run(["git", "checkout", "master"])
    
    result = {
        "branch": branch_name,
        "issue_number": issue_number,
        "status": "completed"
    }
    
    return json.dumps(result)
