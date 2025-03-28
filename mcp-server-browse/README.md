# mcp-server-browse

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and provides web browsing functionality with MCP. It enables AI assistants to search and retrieve information from the internet in real-time.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-browse`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```bash
docker run --rm -i mcp-server-browse
```

## Tools

This project provides the following tools for web browsing:

- `web_search(search_term)` - Search the web for real-time information about any topic
- `browse_url(url)` - Retrieve and parse content from a specific URL

### Parameters Explained

- `search_term`: The search query to look up on the web
- `url`: The full URL to browse and retrieve content from
