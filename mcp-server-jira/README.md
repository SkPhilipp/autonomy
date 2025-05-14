# mcp-server-jira

This project is based on the [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) and associated sample code.

## Installation

Add to Cursor via Cursor Settings -> MCP Servers:

1. Build the Docker image with `docker build . -t mcp-server-jira`.
2. Add new MCP Server
3. Add the Docker image to your AI tooling as a command MCP server:

```bash
docker run --rm -i -e JIRA_URL=https://your-domain.atlassian.net/jira -e JIRA_API_TOKEN=your-api-token -e JIRA_BASE_ISSUE=KEY-123 mcp-server-jira
```

## Required Environment Variables

- `JIRA_URL`: Your Jira instance URL (e.g., https://your-domain.atlassian.net/jira)
- `JIRA_API_TOKEN`: Your Jira API token
- `JIRA_BASE_ISSUE`: The key of the Jira issue to be cloned

## Tools

This project provides the following tools:

- `get_base_jira_issue()` - Get a Jira issue title and description
- `create_jira_issue_from_base(new_title, new_description)` - Creates a new issue with a given title and description, maintaining required fields from base issue
