# Project Status

**Last updated:** 2026-05-10
**Latest commit:** ready to push (pending)

## Current State

README rewrite and CLAUDE.md restructure complete. The repo now has full educational documentation in README.md as the single source of truth, with CLAUDE.md referencing it instead of duplicating content.

## What Exists

- `README.md` — Full educational documentation: problem, solution, setup prompt, keeping it alive, architecture, design decisions, data format, MCP configuration, repo structure
- `CLAUDE.md` — References README for context, contains FAQ directive and maintenance workflow
- `.claude/faq_server.py` — Working FAQ MCP server (Python 3.10+, FastMCP, BM25 search)
- `.mcp.json` — MCP server registration with launcher chain (venv -> uv -> system python)
- `.claude/faqs/` — 6 categories, 12 FAQ entries covering architecture, configuration, design decisions, getting started, maintenance, and project status
- `.github/workflows/ci.yml` — CI: ruff, mypy, py_compile, server load test (Python 3.10/3.12/3.13), prettier
- `.github/dependabot.yml` — github-actions + pip ecosystems
- `.gitignore`, `CHANGELOG.md`
- `LICENSE` — Apache 2.0

## What Needs Work

- Test suite — no tests yet (P0)
- Test and document support for other LLM tools (Cursor, Copilot, Windsurf) (P1)
- Standalone examples — showing how to adapt the pattern for other projects (P1)

## No Background Processes

No background processes are running.
