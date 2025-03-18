#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import re
from datetime import datetime
from mcp.server.fastmcp import FastMCP
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("workflow")

class GitHubWorkflow:
    def __init__(self):
        # Check if gh CLI is installed
        if not self._command_exists("gh"):
            logger.error("GitHub CLI (gh) is not installed. Please install it first:")
            logger.error("https://cli.github.com/manual/installation")
            sys.exit(1)
        
        # Check if user is authenticated with GitHub
        try:
            self._run_command(["gh", "auth", "status"], silent=True)
        except subprocess.CalledProcessError:
            logger.error("Please authenticate with GitHub first using: gh auth login")
            sys.exit(1)
    
    def _command_exists(self, cmd):
        """Check if a command exists in the system PATH"""
        return subprocess.call(
            ["which", cmd], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        ) == 0
    
    def _run_command(self, cmd, silent=False):
        """Run a command and return its output"""
        if not silent:
            logger.info(f"Running: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    
    def list_issues(self):
        """List open issues sorted by priority and creation date"""
        logger.info("Listing open issues...")
        
        # Get open issues with basic information
        issues_json = self._run_command([
            "gh", "issue", "list", 
            "--state", "open", 
            "--json", "number,title,labels,createdAt", 
            "--limit", "100"
        ])
        
        issues = json.loads(issues_json)
        
        # Process and filter issues
        filtered_issues = []
        for issue in issues:
            # Extract label names
            label_names = [label["name"] for label in issue.get("labels", [])]
            
            # Determine priority
            priority = 4  # Default priority
            if "bug" in label_names:
                priority = 1
            elif "documentation" in label_names:
                priority = 2
            elif "enhancement" in label_names:
                priority = 3
            
            # Check if issue is blocked or needs discussion
            is_blocked = "blocked" in label_names
            needs_discussion = "needs discussion" in label_names
            
            # Skip blocked or needs discussion issues
            if is_blocked or needs_discussion:
                continue
            
            filtered_issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "priority": priority,
                "created": issue["createdAt"],
            })
        
        # Sort issues by priority and then by creation date
        filtered_issues.sort(key=lambda x: (x["priority"], x["created"]))
        
        # Print sorted issues
        for issue in filtered_issues:
            print(f"{issue['number']} - {issue['title']}")
        
        return filtered_issues
    
    def start_issue(self, issue_number):
        """Start work on an issue"""
        if not issue_number:
            logger.error("Usage: ./workflow.py start-issue <issue-number>")
            sys.exit(1)
        
        logger.info(f"Starting work on issue #{issue_number}")
        
        # Get issue details
        print(f"Issue #{issue_number} details:")
        print("------------------------")
        issue_details = self._run_command(["gh", "issue", "view", str(issue_number)])
        print(issue_details)
        print("------------------------")
        
        # Get issue title for branch naming
        issue_json = self._run_command([
            "gh", "issue", "view", str(issue_number),
            "--json", "title",
        ])
        issue_title = json.loads(issue_json).get("title", "")
        
        # Determine branch type
        branch_type = "fix"
        if issue_title.startswith("[feature]"):
            branch_type = "feature"
        
        # Reset to clean state from origin/master
        self._run_command(["git", "fetch", "origin"])
        self._run_command(["git", "reset", "--hard", "origin/master"])
        self._run_command(["git", "clean", "-fd"])
        
        # Create and push branch
        branch_name = f"{branch_type}/issue-{issue_number}"
        self._run_command(["git", "checkout", "-b", branch_name])
        self._run_command(["git", "push", "-u", "origin", branch_name])
        
        logger.info(f"Created and pushed branch: {branch_name}")
    
    def change_summary(self):
        """Show summary of current changes"""
        logger.info("Generating change summary...")
        
        print("Current changes:")
        print("---------------")
        status = self._run_command(["git", "status", "--short"])
        print(status)
        
        print("\nDetailed changes:")
        print("----------------")
        diff = self._run_command(["git", "diff"])
        print(diff)
        
        print("\nSuggested commit message format:")
        print("type(scope): description")
        print("Types: feat, fix, docs, style, refactor, test, chore")
        print("Example: feat(workflow): add prepare-commit command")
    
    def commit_and_push(self, commit_message):
        """Commit, push changes and monitor CI/CD"""
        if not commit_message:
            logger.error("Usage: ./workflow.py commit-and-push <commit-message>")
            sys.exit(1)
        
        logger.info(f"Committing with message: {commit_message}")
        
        # Get current branch name
        branch_name = self._run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        
        # Commit and push changes
        self._run_command(["git", "add", "."])
        self._run_command(["git", "commit", "-m", commit_message])
        self._run_command(["git", "push", "-u", "origin", branch_name])
        
        # Check if PR exists
        try:
            pr_json = self._run_command(["gh", "pr", "view", "--json", "number"], silent=True)
            pr_data = json.loads(pr_json)
            pr_number = pr_data.get("number")
            
            if pr_number:
                logger.info(f"Monitoring CI/CD for PR #{pr_number}...")
                try:
                    self._run_command(["gh", "pr", "checks", str(pr_number), "--watch"])
                except subprocess.CalledProcessError:
                    logger.warning("Failed to monitor CI/CD checks, they may not be configured")
        except subprocess.CalledProcessError:
            logger.info("No PR found for current branch, skipping CI/CD monitoring")
    
    def complete_issue(self):
        """Complete work on an issue"""
        logger.info("Completing issue...")
        
        # Get current branch name
        branch_name = self._run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        
        # Extract issue number from branch name
        issue_match = re.search(r'issue-(\d+)', branch_name)
        if not issue_match:
            logger.error(f"Error: Could not extract issue number from branch name '{branch_name}'")
            logger.error("Branch name should be in format: fix/issue-<number> or feature/issue-<number>")
            sys.exit(1)
        
        issue_number = issue_match.group(1)
        
        # Check if PR exists, create one if it doesn't
        try:
            pr_json = self._run_command(["gh", "pr", "view", "--json", "number"], silent=True)
            pr_data = json.loads(pr_json)
            pr_number = pr_data.get("number")
        except subprocess.CalledProcessError:
            # Create PR
            self._run_command([
                "gh", "pr", "create", 
                "--title", f"Fix #{issue_number}", 
                "--body", f"Closes #{issue_number}", 
                "--head", branch_name
            ])
            
            pr_json = self._run_command(["gh", "pr", "view", "--json", "number"])
            pr_data = json.loads(pr_json)
            pr_number = pr_data.get("number")
        
        # Monitor CI/CD if checks exist
        try:
            self._run_command(["gh", "pr", "checks", str(pr_number), "--watch"])
            logger.info("CI checks passed")
        except subprocess.CalledProcessError:
            logger.info("No CI checks configured, proceeding with merge")
        
        # Merge PR and pull changes
        self._run_command(["gh", "pr", "merge", str(pr_number), "--merge"])
        self._run_command(["git", "pull"])
        self._run_command(["git", "checkout", "master"])
        
        logger.info(f"Successfully completed issue #{issue_number}")

# Create MCP wrapper for workflow
mcp = FastMCP("WorkflowMCP")

@mcp.tool()
def list_issues() -> str:
    """List open issues sorted by priority and creation date"""
    workflow = GitHubWorkflow()
    issues = workflow.list_issues()
    return "Listed issues successfully"

@mcp.tool()
def start_issue(issue_number: int) -> str:
    """Start work on an issue"""
    workflow = GitHubWorkflow()
    workflow.start_issue(issue_number)
    return f"Started work on issue #{issue_number}"

@mcp.tool()
def change_summary() -> str:
    """Show summary of current changes"""
    workflow = GitHubWorkflow()
    workflow.change_summary()
    return "Generated change summary successfully"

@mcp.tool()
def commit_and_push(commit_message: str) -> str:
    """Commit, push changes and monitor CI/CD"""
    workflow = GitHubWorkflow()
    workflow.commit_and_push(commit_message)
    return f"Committed and pushed changes with message: {commit_message}"

@mcp.tool()
def complete_issue() -> str:
    """Complete work on an issue"""
    workflow = GitHubWorkflow()
    workflow.complete_issue()
    return "Completed issue successfully"

# Keep the original add function
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    workflow = GitHubWorkflow()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./workflow.py list-issues              # List open issues")
        print("  ./workflow.py start-issue <number>     # Start work on an issue")
        print("  ./workflow.py change-summary           # Show changes and prepare commit message")
        print("  ./workflow.py commit-and-push <message> # Commit, push changes and monitor CI/CD")
        print("  ./workflow.py complete-issue           # Complete work on an issue")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list-issues":
        workflow.list_issues()
    elif command == "start-issue":
        if len(sys.argv) < 3:
            logger.error("Usage: ./workflow.py start-issue <issue-number>")
            sys.exit(1)
        workflow.start_issue(sys.argv[2])
    elif command == "change-summary":
        workflow.change_summary()
    elif command == "commit-and-push":
        if len(sys.argv) < 3:
            logger.error("Usage: ./workflow.py commit-and-push <commit-message>")
            sys.exit(1)
        workflow.commit_and_push(sys.argv[2])
    elif command == "complete-issue":
        workflow.complete_issue()
    else:
        logger.error(f"Unknown command: {command}")
        sys.exit(1)
