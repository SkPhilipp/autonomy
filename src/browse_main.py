from core.config import load_config
from mcp.server.fastmcp import FastMCP
import tool.browse as browse_tools


def setup_mcp(config=None):
    if config is None:
        config = load_config()
    mcp = FastMCP("BrowseMCP")

    @mcp.tool()
    def browse__search(term: str) -> str:
        """Search the web for the given term."""
        return browse_tools.search(term)

    @mcp.tool()
    def browse__fetch(url: str) -> str:
        """Fetch and return the contents of a URL."""
        return browse_tools.fetch(url)

    return mcp


if __name__ == "__main__":
    mcp = setup_mcp()
    mcp.run()
