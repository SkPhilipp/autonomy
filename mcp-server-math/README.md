# mcp-server

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and associated sample code.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-math`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```bash
docker run --rm -i mcp-server-math
```

## Tools

This project provides the following tools:

- `add(a, b)` - Add two numbers
