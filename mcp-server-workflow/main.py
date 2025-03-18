from mcp.server.fastmcp import FastMCP
import workflow
import io
import sys
from contextlib import redirect_stdout

# Create MCP instance
mcp = FastMCP("WorkflowMCP")

# Keep the original add function
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Helper function to capture printed output
def capture_output(func, *args, **kwargs):
    f = io.StringIO()
    with redirect_stdout(f):
        result = func(*args, **kwargs)
    output = f.getvalue()
    return output or str(result)

# Register workflow tools
@mcp.tool()
def list_issues() -> str:
    """List open issues sorted by priority and creation date"""
    wf = workflow.GitHubWorkflow()
    issues = wf.list_issues()
    # Return the formatted issues list or details of what was returned
    return capture_output(print, f"Found {len(issues)} issues:\n" + "\n".join([f"#{i['number']} - {i['title']}" for i in issues]))

@mcp.tool()
def start_issue(issue_number: int) -> str:
    """Start work on an issue"""
    wf = workflow.GitHubWorkflow()
    f = io.StringIO()
    with redirect_stdout(f):
        wf.start_issue(issue_number)
    return f.getvalue() or f"Started work on issue #{issue_number}"

@mcp.tool()
def change_summary() -> str:
    """Show summary of current changes"""
    wf = workflow.GitHubWorkflow()
    f = io.StringIO()
    with redirect_stdout(f):
        wf.change_summary()
    return f.getvalue() or "Generated change summary successfully"

@mcp.tool()
def commit_and_push(commit_message: str) -> str:
    """Commit, push changes and monitor CI/CD"""
    wf = workflow.GitHubWorkflow()
    f = io.StringIO()
    with redirect_stdout(f):
        wf.commit_and_push(commit_message)
    return f.getvalue() or f"Committed and pushed changes with message: {commit_message}"

@mcp.tool()
def complete_issue() -> str:
    """Complete work on an issue"""
    wf = workflow.GitHubWorkflow()
    f = io.StringIO()
    with redirect_stdout(f):
        wf.complete_issue()
    return f.getvalue() or "Completed issue successfully"
