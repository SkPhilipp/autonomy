# mcp-server

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and associated sample code.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server`.
2. Add new MCP Server
3. Run the Docker image with:

```bash
docker run --rm -i mcp-server
```

## Tools

This project provides the following tools:

- `add(a, b)` - Add two numbers
