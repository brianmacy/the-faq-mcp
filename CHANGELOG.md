# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed

- **`.claude/requirements.txt` pins `mcp==1.30.0`.** It said only `mcp`, so every install resolved to whatever was current that day — 2.3.0 by now — while `ci.yml` has always installed `mcp<2`, because mcp 2.0 renamed `FastMCP` to `MCPServer` and removed `mcp.server.fastmcp`, so the server does not import under 2.x. The unpinned file also left the Dependabot `pip` entry with no version to bump and `pip-audit` with nothing stable to audit. Verified under the pin: the server imports and loads its FAQs, and `pip-audit --strict` is clean. Moving to 2.x is a code change, not a version bump.

### Changed

- **The hourly reminder now asks the model to CONSULT the FAQ as well as update it.** It only covered the write half, which let the expensive failure through: acting on training data for a procedure the project has already documented. `keeping-faqs-updated.md` leads with "Before acting on assumptions or training data, query the FAQ MCP first", and the reminder now does too — `search_faqs()` / `get_faq()` for whatever is about to be done, read half first, before the write half. The `PreCompact` reminder is unchanged in intent and still asks only for the write: at compaction there is no next thing to look up, only knowledge about to be lost.

### Added

- **FAQ reminder hooks (`hooks/faq-reminder.sh`, `hooks/README.md`).** A `CLAUDE.md` line saying "keep the FAQ updated" is read once, at the start of a session, and then competes with everything after it. These fire at the two moments the knowledge is actually about to be lost: a **`PreCompact`** hook just before the conversation is compacted (nothing else in the prompt fires there, and compaction is exactly when unwritten learnings get summarised away), and a **`UserPromptSubmit`** hook at most once an hour (`FAQ_REMINDER_INTERVAL_MINUTES`, `0` disables). Silent when the project has no FAQ tree, silent on the first prompt of a session, one stamp per project so two open repos do not silence each other, and the reminder states that "nothing to add" is a correct answer so it cannot pressure the model into inventing entries.

### Security

- **`pip-audit` gate added (`.github/workflows/security.yml`).** Nothing here checked a dependency against an advisory database — the counterpart to `cargo audit` / `cargo vet` in the Rust repos. It audits both places packages are declared: `.claude/requirements.txt`, and the `ruff` / `mypy` / `mcp` pins that live only in `ci.yml`'s `pip install` line, where Dependabot cannot see them either. Runs on PRs, on pushes to main and daily, because advisories get published against versions already pinned. Both sets are clean today.

### Added

- FAQ MCP server (`faq_server.py`) with BM25 search, three tools (`get_faq_categories`, `search_faqs`, `get_faq`), PEP 723 inline metadata for `uv run --script` execution
- MCP configuration (`.mcp.json`) with multi-interpreter launcher chain (venv, uv, system python)
- Local activation config (`.claude/settings.local.json`)
- 12 FAQ entries across 6 categories:
  - `architecture/` — BM25 search, FAQ data format, server structure
  - `configuration/` — MCP JSON setup, server instructions, CI and linting
  - `design-decisions/` — why BM25 over vectors, why FAQ MCPs, why markdown files
  - `getting-started/` — setup guide
  - `maintenance/` — keeping FAQs updated
  - `project-status/` — current state
- GitHub Actions CI (`.github/workflows/ci.yml`) with two jobs:
  - `lint-and-test` — ruff lint + format, mypy, py_compile, server load test across Python 3.10/3.12/3.13
  - `markdown` — prettier check on all markdown files
  - All `uses:` references hash-pinned with tag comments (actions/checkout v4, actions/setup-python v5)
- `.gitignore` excluding `__pycache__/`, `*.pyc`, `.claude/.faq-venv/`, `.claude/settings.local.json`, `.DS_Store`
- Dependabot configuration (`.github/dependabot.yml`) for github-actions and pip ecosystems with daily interval and 21-day cooldown
- `.claude/requirements.txt` — mirrors PEP 723 `mcp` dependency for Dependabot pip scanning (Dependabot cannot read PEP 723 inline script metadata)
- LICENSE file (Apache 2.0)
- README.md — full educational documentation: problem, solution, setup prompt, keeping it alive, architecture, design decisions, data format, MCP configuration, repo structure

### Changed

- CLAUDE.md — restructured to reference README instead of duplicating content; now contains only README reference, FAQ directive, and maintenance workflow
- Setup FAQ — replaced manual steps with the setup prompt approach matching README
- Dependabot — changed to daily interval with 21-day cooldown (catches CVEs fast, gates routine bumps); security updates bypass cooldown

### Fixed

- Live reindex now runs **before** serving each tool response instead of after. `_refresh_if_stale()` is called at the start of `get_faq_categories`/`search_faqs`/`get_faq`, replacing the prior refresh-**after**-serve background thread (`_schedule_refresh`). Previously a just-created or just-edited FAQ was invisible to the **first** query that touched it (the reindex was scheduled on a daemon thread only after the response returned) and appeared only on a subsequent call; it is now visible immediately. The reindex lock is now blocking, so concurrent callers wait for an in-flight reload rather than serve stale data.
- Reindex is now **incremental** so before-serve refresh stays fast at any corpus size. The BM25 index is keyed by file path with `upsert`/`remove` that maintain `df`/`avgdl`/token-length-sum in step; `_refresh_if_stale` re-reads only the added/modified/removed files (diffed via the fingerprint) instead of rebuilding the whole corpus. Refresh after a one-file edit drops from O(corpus) (~100 ms at ~170 files) to sub-millisecond; a no-change call is just the cheap `stat` scan. The staleness fingerprint now pairs `st_size` with `st_mtime_ns` (both free from the existing `stat`) to catch same-mtime-tick edits that change length, and `search()` breaks score ties by `(category, title)` so results are deterministic regardless of whether the index was built incrementally or from scratch. Verified with a 300-op randomized fuzz: the incremental index is identical to a full rebuild (df, avgdl, length-sum, FAQ map, and search results) at every step.
- Markdown formatting — all 8 files that failed prettier check now pass
- Python formatting — `faq_server.py` now passes `ruff format --check`
