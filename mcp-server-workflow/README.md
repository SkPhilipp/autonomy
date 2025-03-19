# mcp-server-workflow

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and integrates GitHub workflow functionality with MCP. It provides a set of tools for managing GitHub issues and pull requests directly from Python.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-workflow`.
2. Add new MCP Server
3. Run the Docker image with `docker run -e GH_TOKEN={GITHUB_PAT} -v {PATH_TO_YOUR_PROJECT}:/project --rm -i mcp-server-workflow`

## GitHub Workflow Tools

This project integrates the following GitHub workflow commands as MCP tools:

- `list_issues()` - List open issues sorted by priority and creation date
- `start_issue(issue_number)` - Start work on an issue
- `change_summary()` - Show summary of current changes
- `commit_and_push(commit_message)` - Commit, push changes and monitor CI/CD
- `complete_issue()` - Complete work on an issue

## Requirements

- Python 3.12+
- GitHub CLI (`gh`) installed and authenticated
- Git installed and configured
