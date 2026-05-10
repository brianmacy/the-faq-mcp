# Setup

## Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip install mcp`

## Quick Start

Paste this prompt into Claude Code in your project's directory:

> Look at https://github.com/brianmacy/the-faq-mcp for the reference implementation of a FAQ MCP server. Copy .claude/faq_server.py and .mcp.json into this project, update the server name and instructions to match this project, and seed initial FAQ entries covering: how to build, how to run tests, environment setup, architecture overview, and any non-obvious project knowledge. Add a CLAUDE.md directive telling the LLM to query the FAQ before guessing. The FAQ entries should be specific to THIS project — exact commands, real procedures, actual architecture decisions.

The LLM will set up the server, configuration, FAQ entries, and CLAUDE.md directive — all tailored to your project.

## What Gets Created

The prompt sets up:

- `.claude/faq_server.py` — the MCP server
- `.claude/faqs/` — category directories with seed FAQ entries
- `.mcp.json` — MCP server registration (see the `mcp-json-setup` FAQ for details on the launcher chain)
- CLAUDE.md directive — tells the LLM to query the FAQ before guessing

## Manual Testing

To verify the server works:

```bash
uv run --script .claude/faq_server.py
# Or if mcp is installed:
python .claude/faq_server.py
```

The server runs on stdio — Claude Code launches it automatically via `.mcp.json`.

## What to Document First

Start with the things that cause the most pain when an LLM gets them wrong:

1. **How to build the project** — exact commands, prerequisites, platform-specific notes
2. **How to run tests** — commands, expected output, how to interpret results
3. **Environment setup** — required env vars, dependencies, configuration
4. **Architecture overview** — why the code is structured the way it is
