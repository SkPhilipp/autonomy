# mcp-server

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and associated sample code.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```bash
docker run --rm -i mcp-server
```

## Tools

This project provides the following tools:

- `add(a, b)` - Add two numbers
- `format_with_black(project_name, target_path=None, line_length=88, skip_string_normalization=False, verbose=False)` - Format Python code in a directory using Black
- `check_with_black(project_name, target_path=None, line_length=88, skip_string_normalization=False)` - Check Python code in a directory using Black without modifying files
