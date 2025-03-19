# mcp-server-workflow

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and integrates GitHub workflow functionality with MCP. It provides a set of tools for managing GitHub issues and pull requests directly from Python.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-workflow`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```
docker run \
  -v ~/.ssh:/root/.ssh:ro
  -v ~/.gitconfig:/etc/gitconfig:ro
  -v {PROJECTS_HOME}:/projects
  -e GH_TOKEN={GITHUB_TOKEN}
  --rm -i mcp-server-workflow
```

## Tools

This project integrates the following Git and GitHub development flow commands as MCP tools:

- `list_issues(project_name=None)` - List open issues sorted by priority and creation date
- `start_issue(issue_number, project_name=None)` - Start work on an issue
- `change_summary(project_name=None)` - Show summary of current changes
- `commit_and_push(commit_message, project_name=None)` - Commit, push changes and monitor CI/CD
- `complete_issue(project_name=None)` - Complete work on an issue

### Project Name Parameter

All tools now accept an optional `project_name` parameter. When specified, operations will be performed on the project in the `/projects/{project_name}` directory. If no project name is provided, operations will default to the `/projects` directory.

For example, to list issues for a specific project:
```python
list_issues(project_name="my-repo")
```
