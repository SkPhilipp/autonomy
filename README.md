# MCP Server (Merged)

This project merges all MCP (Model Context Protocol) servers into a single server, providing a unified set of tools for AI assistants.

## Structure
- `main.py`: Entrypoint that registers all tools.
- `tool/`: Contains one file per tool group.
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
        "mcp-server-all": {
        "command": "/.../autonomy/.venv/bin/python3",
        "args": [
            "/.../autonomy/main.py",
            "--env",
            "/.../.env",
            "--project-path",
            "/.../project/"
        ]
        }
    }
}
```
