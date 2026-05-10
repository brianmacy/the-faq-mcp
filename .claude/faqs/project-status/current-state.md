# Current State

## What This Repo Is

An educational repository and working reference implementation for FAQ MCP servers. It teaches people (and LLMs) how to build FAQ MCPs and why they are useful.

## What Is Complete

- **README.md** — full educational documentation: problem, solution, setup prompt, keeping it alive, architecture, design decisions, data format, MCP configuration, repo structure
- **FAQ MCP server** (`faq_server.py`) — fully functional with BM25 search, three tools, PEP 723 inline metadata
- **MCP configuration** — `.mcp.json` with launcher chain (`.claude/settings.local.json` optional, for skipping approval prompt)
- **CLAUDE.md** — references README for project context, contains FAQ directive and maintenance workflow
- **FAQ content** — 12 entries across 6 categories: architecture, configuration, design-decisions, getting-started, maintenance, project-status
- **Self-documenting** — the FAQ MCP documents itself as its own reference implementation
- **GitHub Actions CI** (`.github/workflows/ci.yml`) — two jobs:
  - `lint-and-test`: ruff lint + format, mypy, py_compile, server load test across Python 3.10/3.12/3.13
  - `markdown`: prettier check on all markdown files
  - All action references are hash-pinned with tag comments
- **`.gitignore`** — excludes `__pycache__/`, `*.pyc`, `.claude/.faq-venv/`, `.claude/settings.local.json`, `.DS_Store`
- **Formatting** — all markdown files pass prettier, all Python passes ruff format
- **LICENSE** — Apache 2.0

## What Is Not Yet Done

- **Tests** — no dedicated test suite yet (CI validates syntax, types, and server loading but no unit tests)
- **Examples** — no standalone examples showing how to adapt the pattern for other projects
- **Other LLM tool support** — test and document Cursor, Copilot, Windsurf, and other MCP-capable tools

## Architecture Summary

Single-file Python server using FastMCP, BM25 search built in (~40 lines), markdown FAQ files organized by category directories under `.claude/faqs/`. Zero external dependencies beyond the `mcp` package. Runs via `uv run --script`.
