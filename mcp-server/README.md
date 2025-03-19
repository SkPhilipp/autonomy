# mcp-server

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and associated sample code.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

### Option 1: Local Installation

1. Add new MCP Server
2. Command `uv --directory /{PATH_TO_REPO}/mcp-server run mcp run main.py`

Alternatively, run it locally with:

```bash
source .venv/bin/activate
mcp run main.py
```

### Option 2: Docker Installation

1. Build the Docker image with `docker build . -t mcp-server`.
2. Add new MCP Server
3. Run the Docker image with:

```bash
docker run \
  -v {PROJECT_PATH}:/project \
  --rm -i mcp-server
```

## Tools

This server provides the following tools:

- `add(a, b)` - Add two numbers
