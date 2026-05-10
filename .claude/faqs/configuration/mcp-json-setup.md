# MCP JSON Setup

The FAQ MCP server is registered with Claude Code via a `.mcp.json` file at the repository root.

## Launcher Chain

The `.mcp.json` uses a shell command that tries multiple Python interpreters in order:

1. **Virtual environment** — `.claude/.faq-venv/bin/python` (or `Scripts/python.exe` on Windows)
2. **uv run** — `uv run --script .claude/faq_server.py` (uses PEP 723 inline metadata)
3. **System Python** — `python .claude/faq_server.py` (requires `mcp` package installed)

This fallback chain means the server works across different development environments without requiring a specific setup.

## Example .mcp.json

```json
{
  "mcpServers": {
    "my-project-faq": {
      "command": "sh",
      "args": [
        "-c",
        "ROOT=$(git rev-parse --show-toplevel) && VENV=\"$ROOT/.claude/.faq-venv/bin/python\" && VENV_WIN=\"$ROOT/.claude/.faq-venv/Scripts/python.exe\" && if [ -x \"$VENV\" ]; then exec \"$VENV\" \"$ROOT/.claude/faq_server.py\"; elif [ -x \"$VENV_WIN\" ]; then exec \"$VENV_WIN\" \"$ROOT/.claude/faq_server.py\"; elif command -v uv >/dev/null 2>&1; then exec uv run --script \"$ROOT/.claude/faq_server.py\"; else exec python \"$ROOT/.claude/faq_server.py\"; fi"
      ]
    }
  }
}
```

## Activation

The `.mcp.json` file alone is sufficient. Claude Code discovers MCP servers from `.mcp.json` and prompts the user to approve them on first use.

To skip the approval prompt, optionally create `.claude/settings.local.json`:

```json
{
  "enabledMcpjsonServers": ["my-project-faq"],
  "enableAllProjectMcpServers": true
}
```

Note: `settings.local.json` is typically gitignored since it contains local preferences. The `.mcp.json` file is committed to the repo so all team members get the server definition.
