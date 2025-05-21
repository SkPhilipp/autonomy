from core.config import load_config

config = load_config()

from mcp.server.fastmcp import FastMCP
import tool.jira as jira_tools
import tool.browse as browse_tools
import tool.formatter as formatter_tools
import tool.workflow as workflow_tools

mcp = FastMCP("MCP")


@mcp.tool()
def jira__get_base_issue() -> dict:
    """Retrieve the base JIRA issue configuration."""
    return jira_tools.get_base_jira_issue(config)


@mcp.tool()
def jira__create_issue_from_base(title: str, description: str) -> dict:
    """Create a new JIRA issue with the given title and description."""
    return jira_tools.create_jira_issue_from_base(title, description, config)


@mcp.tool()
def browse__search(term: str) -> str:
    """Search the web for the given term."""
    return browse_tools.web_search(term)


@mcp.tool()
def browse__fetch(url: str) -> str:
    """Fetch and return the contents of a URL."""
    return browse_tools.browse_url(url)


@mcp.tool()
def formatter__black() -> str:
    """Format the specified project using Black."""
    return formatter_tools.format_with_black(config)


@mcp.tool()
def workflow__list() -> str:
    """List all current issues."""
    return workflow_tools.list_issues(config)


@mcp.tool()
def workflow__start(issue_number: int) -> str:
    """Start work on the specified issue."""
    return workflow_tools.start_issue(issue_number, config)


@mcp.tool()
def workflow__change_summary() -> str:
    """Get a summary of recent changes."""
    return workflow_tools.change_summary(config)


@mcp.tool()
def workflow__commit(commit_message: str) -> str:
    """Commit changes and push to the repository."""
    return workflow_tools.commit_and_push(commit_message, config)


@mcp.tool()
def workflow__complete() -> str:
    """Mark the current issue as complete."""
    return workflow_tools.complete_issue(config)


if __name__ == "__main__":
    mcp.run()
