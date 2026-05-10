# Project Status

**Last updated:** 2026-05-10

## Current State

All infrastructure for the FAQ MCP reference implementation has been created from scratch in a single session. Nothing beyond the initial commit (README.md stub) has been committed or pushed yet.

## What Exists

- `.claude/faq_server.py` — Working FAQ MCP server (Python 3.10+, FastMCP, BM25 search)
- `.mcp.json` — MCP server registration with launcher chain (venv -> uv -> system python)
- `.claude/settings.local.json` — Local activation config
- `.claude/faqs/` — 6 categories, 11 FAQ entries covering architecture, configuration, design decisions, getting started, maintenance, and project status
- `CLAUDE.md` — Full project guidance (purpose, architecture, design decisions, FAQ maintenance workflow)
- `README.md` — Stub only (single heading)
- `.github/workflows/ci.yml` — GitHub Actions CI with two jobs:
  - `lint-and-test`: ruff lint + format, mypy, py_compile, server load test (Python 3.10/3.12/3.13 matrix)
  - `markdown`: prettier check on all markdown files
  - All `uses:` references hash-pinned with tag comments
- `.gitignore` — Excludes `__pycache__/`, `*.pyc`, `.claude/.faq-venv/`, `.claude/settings.local.json`, `.DS_Store`
- `CHANGELOG.md` — Unreleased entries for all work

## Working Tree State

All files except README.md are untracked (not yet committed). The working tree is:

```
 M README.md
?? .claude/
?? .github/
?? .gitignore
?? .mcp.json
?? CHANGELOG.md
?? CLAUDE.md
```

## Formatting

- All markdown files pass `npx prettier --check`
- All Python files pass `ruff check` and `ruff format --check`

## No Background Processes

No background processes are running.
