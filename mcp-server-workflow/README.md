# mcp-server-workflow

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and integrates GitHub workflow functionality with MCP. It provides a set of tools for managing GitHub issues and pull requests directly from Python.

> **Warning**: This project only works with repositories that use SSH remotes (git@github.com). HTTPS remotes are not supported.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-workflow`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```
docker run \
  -v ~/.ssh:/root/.ssh:ro
  -v ~/.gitconfig:/etc/gitconfig:ro
  -v {PROJECT_HOME}:/project
  -e GH_TOKEN={GITHUB_TOKEN}
  --rm -i mcp-server-workflow
```

## Tools

This project integrates the following Git and GitHub development flow commands as MCP tools:

- `list_issues()` - List open issues sorted by priority and creation date
- `start_issue(issue_number)` - Start work on an issue
- `change_summary()` - Show summary of current changes
- `commit_and_push(commit_message)` - Commit, push changes and monitor CI/CD
- `complete_issue()` - Complete work on an issue

## Example Rules

```
When instructed "auto push":
1. Get a summary of current changes using `mcp__change_summary`
2. Commit and push using `mcp__commit_and_push` with a short conventional commit message

When instructed "next issue":
1. List and select first unblocked issue using `mcp__list_issues`
2. Start work using `mcp__start_issue` with the selected issue number
3. Work on the issue, keep changes focused to only the issue at hand:
   - Implement changes
   - Run tests locally
   - Update documentation
4. Get a summary of changes using `mcp__change_summary`
5. Commit and push using `mcp__commit_and_push` with a short conventional commit message
6. Complete issue using `mcp__complete_issue`
```
