# the-faq-mcp

A working reference implementation and educational guide for building FAQ MCP servers — queryable knowledge bases that give LLMs (and humans) accurate, project-specific answers instead of stale training data.

## The Problem

LLMs working on your codebase will confidently guess at build commands, API signatures, and architecture patterns — and get them wrong. They forget procedures they've executed hundreds of times after a context reset. Hard-won knowledge about why decisions were made, what was tried and rejected, and how things actually work disappears when a session ends or a team member moves on.

This is especially painful for **private repositories** whose code and documentation will never appear in any LLM's training data.

## The Solution

A FAQ MCP server gives LLMs a queryable, authoritative source of truth that lives in the repo alongside the code. Instead of guessing, the LLM queries the FAQ and gets the right answer on the first try.

**What it captures:**

- Build procedures, environment setup, test execution — the rote stuff that should never require re-discovery
- Architecture decisions and their rationale — not just _what_ but _why_
- Rejected approaches — "we tried X, it didn't work because Y" so nobody repeats the mistake
- Current project status and future TODOs
- Anything non-obvious that would help the next developer or the next LLM session

**What makes it work:**

- Version-controlled alongside the code — stays in sync, goes through code review
- Self-improving — every session that learns something new writes it back to the FAQ
- Token-efficient — LLMs pull specific knowledge on demand instead of loading everything into context
- Zero external dependencies — BM25 search built in, just the `mcp` package and markdown files

In practice, this mechanism dramatically reduces the frequency of wrong-headed LLM behavior and helps bring new team members (human or AI) onto projects rapidly.

## Add a FAQ MCP to Your Project

Paste this prompt into Claude Code in your project's directory:

> Look at https://github.com/brianmacy/the-faq-mcp for the reference implementation of a FAQ MCP server. Copy .claude/faq_server.py and .mcp.json into this project, update the server name and instructions to match this project, and seed initial FAQ entries covering: how to build, how to run tests, environment setup, architecture overview, and any non-obvious project knowledge. Add a CLAUDE.md directive telling the LLM to query the FAQ before guessing. The FAQ entries should be specific to THIS project — exact commands, real procedures, actual architecture decisions.

The LLM will set up the server, configuration, FAQ entries, and CLAUDE.md directive — all tailored to your project.

## Keeping It Alive

The FAQ is only as good as the discipline of keeping it current.

**Before making changes**, the LLM should query the FAQ MCP first for:

- Environment setup, build procedures, test execution
- Architecture and design rationale
- Prior decisions — what was tried before, what was rejected and why

**After making changes**, before committing, the LLM should update FAQ entries for:

- Changed environment setup, build/test/deploy procedures
- New architecture and design decisions and their rationale
- Rejected approaches — what was tried, why it didn't work
- Current project status — what's done, what's in progress, what's blocked
- Future TODOs and planned work
- New tooling or commands, corrections to existing FAQs

When new topic areas are added, the server's `instructions` string must be updated so the LLM knows to query for those topics.

**If a session learned something non-obvious that would help the next developer or the next LLM session, it belongs in a FAQ.**

Add this to your project's CLAUDE.md to enforce the discipline:

```markdown
## Keeping FAQs Updated

Before acting on assumptions or training data, query the FAQ MCP first. Do NOT
guess at procedures the project has already documented. Query first, act second.

Before committing, review whether any FAQ entries need updating based on the
session's work. If you learned something non-obvious, write a FAQ entry directly.
If new topic areas were added, update the server's `instructions` parameter so
the LLM knows to query for those topics.
```

## How It Works

The server is a single Python file (~200 lines) using [FastMCP](https://github.com/modelcontextprotocol/python-sdk). It exposes three tools:

| Tool                                          | Purpose                                            |
| --------------------------------------------- | -------------------------------------------------- |
| `get_faq_categories()`                        | List all categories with article counts and titles |
| `search_faqs(query, category?, max_results?)` | BM25-ranked search with excerpts                   |
| `get_faq(title, category?)`                   | Full content by title with fuzzy fallback          |

At startup, the server walks `.claude/faqs/`, tokenizes every markdown file, and builds a BM25 index (Okapi BM25, K1=1.2, B=0.75). Search queries are scored against pre-computed term frequencies — no external search engine, no API calls, no network required.

### Key Design Decisions

- **BM25 over vector search** — zero dependencies, deterministic, transparent scoring, good enough for FAQ-sized collections (see the [design-decisions FAQs](.claude/faqs/design-decisions/) for full rationale)
- **Markdown files over databases** — human-readable, git-friendly diffs, no schema to maintain, renders natively on GitHub
- **Single dependency** — just the `mcp` package; search is built-in (~40 lines)
- **PEP 723 inline metadata** — runs via `uv run --script` without virtualenv setup
- **Slots-based document class** — memory-efficient for large FAQ collections
- **Pre-tokenized index** — tokenize at load time, instant search at query time

### FAQ Data Format

Each category is a directory under `.claude/faqs/`. Each FAQ is a markdown file:

```
.claude/faqs/
├── building/
│   └── how-to-build.md
├── architecture/
│   └── project-structure.md
└── testing/
    └── running-tests.md
```

- File naming: `kebab-case-title.md` (normalized to title case for display)
- Content: plain markdown with `# Title` heading, sections, code blocks
- Adding a category = creating a directory. Adding a FAQ = creating a file. No configuration needed.

### MCP Configuration

The server is registered via `.mcp.json` at the repo root with a launcher chain that tries: venv Python → Windows venv → `uv run --script` → system Python. Claude Code discovers the server from `.mcp.json` and prompts to approve it on first use — no other setup required.

The server's `instructions` parameter tells the LLM what topics the FAQ covers and when to query it. This is what makes the LLM actually use the FAQ instead of guessing. A matching directive in CLAUDE.md reinforces it from the other side — belt and suspenders.

### Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) (recommended) or `pip install mcp`

### Running the server manually

```bash
uv run --script .claude/faq_server.py
```

In normal use, the LLM tool launches the server automatically via `.mcp.json`.

## Repository Structure

This repo is self-documenting — the FAQ MCP serves its own documentation:

```
.claude/
├── faq_server.py              # The reference implementation
├── faqs/
│   ├── architecture/          # BM25 search, server structure, data format
│   ├── configuration/         # MCP setup, server instructions, CI/linting
│   ├── design-decisions/      # Why BM25, why markdown, why FAQ MCPs
│   ├── getting-started/       # Setup guide
│   ├── maintenance/           # Keeping FAQs updated
│   └── project-status/        # Current state of this repo
├── STATUS.md                  # Current project state (session handoff)
└── NEXT_STEPS.md              # Priority-ordered next actions
.mcp.json                      # MCP server registration
CLAUDE.md                      # LLM guidance (architecture + FAQ maintenance workflow)
.github/
├── workflows/ci.yml           # Ruff, mypy, prettier, server load test
└── dependabot.yml             # 21-day cooldown for dependency updates
```
