# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- FAQ MCP server (`faq_server.py`) with BM25 search, three tools (`get_faq_categories`, `search_faqs`, `get_faq`), PEP 723 inline metadata for `uv run --script` execution
- MCP configuration (`.mcp.json`) with multi-interpreter launcher chain (venv, uv, system python)
- Local activation config (`.claude/settings.local.json`)
- CLAUDE.md with project purpose, architecture, design decisions, and FAQ maintenance workflow
- 11 FAQ entries across 6 categories:
  - `architecture/` — BM25 search, FAQ data format, server structure
  - `configuration/` — MCP JSON setup, server instructions
  - `design-decisions/` — why BM25 over vectors, why FAQ MCPs, why markdown files
  - `getting-started/` — setup guide
  - `maintenance/` — keeping FAQs updated
  - `project-status/` — current state
- GitHub Actions CI (`.github/workflows/ci.yml`) with two jobs:
  - `lint-and-test` — ruff lint + format, mypy, py_compile, server load test across Python 3.10/3.12/3.13
  - `markdown` — prettier check on all markdown files
  - All `uses:` references hash-pinned with tag comments (actions/checkout v4, actions/setup-python v5)
- `.gitignore` excluding `__pycache__/`, `*.pyc`, `.claude/.faq-venv/`, `.claude/settings.local.json`, `.DS_Store`
- Dependabot configuration (`.github/dependabot.yml`) for github-actions and pip ecosystems

### Fixed

- Markdown formatting — all 8 files that failed prettier check now pass
- Python formatting — `faq_server.py` now passes `ruff format --check`
