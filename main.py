from core.config import load_config

config = load_config()

from mcp.server.fastmcp import FastMCP
import tool.math as math_tools
import tool.jira as jira_tools
import tool.browse as browse_tools
import tool.formatter as formatter_tools
import tool.workflow as workflow_tools

mcp = FastMCP("MCP")

@mcp.tool()
def math__add(a: int, b: int) -> int:
    """Add two numbers."""
    return math_tools.add(a, b)

@mcp.tool()
def math__subtract(a: int, b: int) -> int:
    """Subtract one number from another."""
    return math_tools.subtract(a, b)

@mcp.tool()
def jira__get_base_issue() -> dict:
    """Retrieve the base JIRA issue configuration."""
    return jira_tools.get_base_jira_issue(config)

@mcp.tool()
def jira__create_issue_from_base(title: str, description: str) -> dict:
    """Create a new JIRA issue with the given title and description."""
    return jira_tools.create_jira_issue_from_base(title, description, config)

@mcp.tool()
def browse__web_search(term: str) -> str:
    """Search the web for the given term."""
    return browse_tools.web_search(term, config)

@mcp.tool()
def browse__browse_url(url: str) -> str:
    """Fetch and return the contents of a URL."""
    return browse_tools.browse_url(url, config)

@mcp.tool()
def formatter__format_with_black(project_name: str) -> str:
    """Format the specified project using Black."""
    return formatter_tools.format_with_black(project_name, config)

@mcp.tool()
def workflow__list_issues() -> str:
    """List all current issues."""
    return workflow_tools.list_issues(config)

@mcp.tool()
def workflow__start_issue(issue_number: int) -> str:
    """Start work on the specified issue."""
    return workflow_tools.start_issue(issue_number, config)

@mcp.tool()
def workflow__change_summary() -> str:
    """Get a summary of recent changes."""
    return workflow_tools.change_summary(config)

@mcp.tool()
def workflow__commit_and_push(commit_message: str) -> str:
    """Commit changes and push to the repository."""
    return workflow_tools.commit_and_push(commit_message, config)

@mcp.tool()
def workflow__complete_issue() -> str:
    """Mark the current issue as complete."""
    return workflow_tools.complete_issue(config)

if __name__ == "__main__":
    mcp.run()
