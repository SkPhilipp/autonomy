# MCP Server (Merged)

This project merges all MCP (Model Context Protocol) servers into a single server, providing a unified set of tools for AI assistants.

## Structure
- `launch.sh`: Entrypoint that registers all tools.
- `src/`: Contains one file per tool group.
- `pyproject.toml`: Combined dependencies for all tools

## Build

```
uv sync
```

## Run

```
uv run mcp run main.py
```

## Usage in Cursor

```json
{
    "mcpServers": {
        "tools": {
            "command": "/.../autonomy/launch.sh",
            "args": [
                "browse|jira|workflow",
                "--env",
                "/.../.env",
                "--project-path",
                "/.../project/"
            ]
        }
    }
}
```
