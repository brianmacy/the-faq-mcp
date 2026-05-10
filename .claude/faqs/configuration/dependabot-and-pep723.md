# Dependabot and PEP 723

## The Problem

The FAQ MCP server (`faq_server.py`) declares its `mcp` dependency using PEP 723 inline script metadata:

```python
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp"]
# ///
```

This allows `uv run --script faq_server.py` to work without a virtualenv or `requirements.txt`. However, **Dependabot cannot scan PEP 723 inline metadata** — it only knows how to read `requirements.txt`, `setup.py`, `pyproject.toml`, and similar standard pip ecosystem files.

## The Workaround

We added `.claude/requirements.txt` containing just `mcp` as a parallel dependency declaration. Dependabot's pip ecosystem scanner is configured with `directory: "/.claude"` in `.github/dependabot.yml` so it finds this file.

This means the `mcp` dependency is declared in two places:

1. PEP 723 metadata in `faq_server.py` (used by `uv run --script`)
2. `.claude/requirements.txt` (used by Dependabot for CVE scanning)

**These must be kept in sync.** If a new dependency is added to the PEP 723 block, add it to `requirements.txt` too.

## Why Not Just Use requirements.txt?

The PEP 723 metadata is what makes the zero-setup experience work — `uv run --script` reads it and handles dependency installation automatically. The `requirements.txt` is only there because Dependabot needs it. If Dependabot adds PEP 723 support in the future, the `requirements.txt` can be removed.

## Dependabot Schedule

Both ecosystems (github-actions and pip) use:

- **Daily interval** — catches CVEs fast
- **21-day cooldown** — gates routine version bumps so they don't flood the repo
- Security-only updates bypass the cooldown
