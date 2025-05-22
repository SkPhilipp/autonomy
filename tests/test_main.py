import main
from mcp.server.fastmcp import FastMCP


class DummyConfig:
    pass


def test_mcp_instance():
    mcp = main.setup_mcp(config=DummyConfig())
    assert isinstance(mcp, FastMCP)
