# mcp-server-workflow

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and integrates GitHub workflow functionality with MCP. It provides a set of tools for managing GitHub issues and pull requests directly from Python.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Add new MCP Server
2. Command `uv --directory /{PATH_TO_REPO}/mcp-server-workflow run mcp run main.py`

Alternatively, run it locally with:

```bash
source .venv/bin/activate
mcp run main.py
```

## GitHub Workflow Tools

This project integrates the following GitHub workflow commands as MCP tools:

- `list_issues()` - List open issues sorted by priority and creation date
- `start_issue(issue_number)` - Start work on an issue
- `change_summary()` - Show summary of current changes
- `commit_and_push(commit_message)` - Commit, push changes and monitor CI/CD
- `complete_issue()` - Complete work on an issue

## Command Line Usage

You can also use the workflow functionality directly from the command line:

```bash
# List open issues
python workflow.py list-issues

# Start work on an issue
python workflow.py start-issue <issue-number>

# Show changes and prepare commit message
python workflow.py change-summary

# Commit and push changes
python workflow.py commit-and-push "<commit-message>"

# Complete work on an issue
python workflow.py complete-issue
```

## Requirements

- Python 3.12+
- GitHub CLI (`gh`) installed and authenticated
- Git installed and configured
