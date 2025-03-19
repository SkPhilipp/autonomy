# mcp-server-formatter

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and integrates Black Python code formatting functionality with MCP. It provides a simple tool for formatting Python code in your projects using the Black formatter.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-formatter`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```bash
docker run \
  -v {PROJECTS_HOME}:/projects \
  --rm -i mcp-server-formatter
```

## Tools

This project provides the following tool for code formatting using Black:

- `format_with_black(project_name)` - Format Python code in a project directory using Black with default settings

### Parameters Explained

- `project_name`: The basename of the project's root directory.
