from core.config import load_config
from mcp.server.fastmcp import FastMCP
import tool.jira as jira_tools


def setup_mcp(config=None):
    if config is None:
        config = load_config()
    mcp = FastMCP("JiraMCP")

    @mcp.tool()
    def jira__get_base_issue() -> dict:
        """Retrieve the base JIRA issue configuration."""
        return jira_tools.get_base_issue(config)

    @mcp.tool()
    def jira__create_issue_from_base(title: str, description: str) -> dict:
        """Create a new JIRA issue with the given title and description."""
        return jira_tools.create_issue_from_base(title, description, config)

    @mcp.tool()
    def jira__get_epic_stories(epic_key: str) -> dict:
        """Retrieve all Issues in an Epic."""
        return jira_tools.get_epic_stories(epic_key, config)

    @mcp.tool()
    def jira__get_story_content(story_key: str) -> dict:
        """Retrieve the description, title and comments for a story."""
        return jira_tools.get_story_content(story_key, config)

    return mcp


if __name__ == "__main__":
    mcp = setup_mcp()
    mcp.run()
