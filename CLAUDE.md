# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Purpose

This is an educational repository that teaches people (and LLMs) how to build FAQ MCP servers and why they are useful. The repo contains a working FAQ MCP of its own as a reference implementation. All content is non-proprietary and intended for public consumption.

This is a **working documentation archive** — the FAQ content is living documentation that gets maintained as part of the development workflow, not a static snapshot.

## Why FAQ MCPs

**LLM training data is stale and wrong.** LLM training cutoffs mean they will guess at build commands, API signatures, and architecture patterns — and often guess wrong. A FAQ MCP gives them a queryable, authoritative source of truth that's version-controlled alongside the code. This is especially critical for private repositories whose code and documentation will never appear in any LLM's training data.

**LLMs forget what they've done before.** The most maddening failure mode: an LLM that has successfully built, tested, and deployed your project hundreds of times will, after a context reset, forget the exact commands and fumble through it like it's the first time. Environment setup, build procedures, test execution, result evaluation — these are rote, repeatable tasks that should never require re-discovery. A FAQ MCP makes these procedures queryable so the LLM gets the right answer on the first try, every session, regardless of context history.

**Institutional memory that survives context loss.** When a Claude Code session ends, gets compacted, or a developer switches projects, hard-won context evaporates. FAQs persist that knowledge — "we tried X, it didn't work because Y, do Z instead" — so the next session (or person) doesn't repeat the same mistakes. This solves the "hit by a bus" problem: design decisions, architectural rationale, current project status, and the _why_ behind choices are captured in a searchable, durable form that doesn't depend on any one person being available.

**Dramatically reduces LLM frustration.** In practice, this mechanism dramatically reduces the frequency of wrong-headed LLM behavior. Without it, Claude confidently generates plausible-but-wrong code based on stale training data, requiring constant correction. With the FAQ MCP, it queries first and gets current, project-specific answers.

**Rapid onboarding for new team members.** The FAQ MCP captures not just _what_ the project does but _why_ — current status, future TODOs, reasons why certain approaches were rejected, and the rationale behind architectural choices. A new team member (human or LLM) can get productive quickly by querying the FAQ instead of reverse-engineering decisions from code archaeology or waiting for a knowledge transfer meeting that may never happen.

**Shared understanding across the team.** The FAQ MCP makes up-to-date design, architectural, status, and decision information available to everyone on the project — humans and LLMs alike. Instead of knowledge living in one person's head or buried in Slack threads, it's queryable on demand by anyone with repo access.

**Self-improving documentation.** When the development workflow includes mandatory FAQ review before committing, every session that learns something new writes it back. This creates a positive feedback loop where the FAQ gets better with use, unlike static docs that rot.

**Token-efficient context.** Instead of stuffing everything into CLAUDE.md (which is always loaded into the LLM context), the FAQ MCP lets Claude pull specific knowledge on demand via tool calls. Keeps the context window lean while making deep knowledge accessible.

**Zero external dependencies.** BM25 search is built into the server (~40 lines of Python). No Elasticsearch, no vector DB, no API keys. Just the `mcp` package and markdown files.

## Architecture

The project serves two roles:

1. **Tutorial/documentation** — explains the what, why, and how of FAQ MCPs
2. **Reference implementation** — a working FAQ MCP server that demonstrates the patterns described in the documentation

### FAQ MCP Server Pattern

The reference implementation follows this structure:

```
.claude/
├── faq_server.py          # MCP server (Python 3.10+, FastMCP)
├── faqs/                  # Category directories with .md files
│   ├── <category>/        # One directory per topic area
│   │   ├── <title>.md     # One markdown file per FAQ entry
│   │   └── ...
│   └── ...
```

**Key design decisions:**

- **BM25 search** (Okapi BM25, K1=1.2, B=0.75) — no external search dependencies
- **Single dependency** — just the `mcp` package; search is built-in
- **PEP 723 inline metadata** — runs via `uv run --script` without virtualenv setup
- **Slots-based document class** — memory-efficient for large FAQ collections
- **Pre-tokenized index** — tokenize at load time, O(1) lookup at search time
- **Three tools**: `get_faq_categories()`, `search_faqs(query)`, `get_faq(title)`

### FAQ Data Format

- Each category is a directory under `.claude/faqs/`
- File naming: `kebab-case-title.md` (normalized to title case for display)
- Content: plain markdown with `# Title` heading, sections, code blocks
- The server adds an improvement footer encouraging feedback

### MCP Configuration

The server is registered via `.mcp.json` at the repo root with a launcher chain that tries: venv Python → Windows venv → `uv run --script` → system Python.

The `.mcp.json` alone is sufficient — Claude Code will discover the server and prompt the user to approve it on first use. To skip the approval prompt, create `.claude/settings.local.json` (typically gitignored since it's a local preference):

```json
{
  "enabledMcpjsonServers": ["<server-name>"],
  "enableAllProjectMcpServers": true
}
```

## Keeping FAQs Updated

FAQs are the project's institutional memory. They must be maintained as a living archive, not left to rot. The FAQ is only as good as the discipline of keeping it current.

### Before Making Changes

Before acting on assumptions or training data, query the FAQ MCP first. This applies to:

- **Environment setup** — how to configure the dev environment, required env vars, dependency installation
- **Build procedures** — exact commands, flags, build systems, platform-specific notes
- **Test execution and evaluation** — how to run tests, what passing/failing looks like, how to interpret results
- **Architecture and design** — why the code is structured the way it is, what patterns to follow
- **Prior decisions** — what was tried before, what was rejected and why, so you don't re-propose a dead end

```
search_faqs("topic relevant to the task")
get_faq("specific FAQ title if known")
```

Do NOT guess at procedures the project has already documented. Query first, act second.

### After Making Changes

Before committing, review whether any FAQ entries need updating based on the session's work:

1. Use `search_faqs(query)` to find FAQs potentially affected by the changes
2. Read affected FAQ markdown files directly from `.claude/faqs/`
3. Update or create FAQ entries for:
   - **Environment setup** — new dependencies, changed env vars, platform-specific gotchas
   - **Build/test/deploy procedures** — changed commands, new flags, updated steps
   - **Architecture and design decisions** — why a structure was chosen, what patterns to follow
   - **Rejected approaches** — what was tried, why it didn't work, so the next person doesn't repeat it
   - **Current project status** — what's done, what's in progress, what's blocked
   - **Future TODOs and planned work** — what comes next, in what order, with enough context to act on it
   - **New tooling or commands** introduced during the session
   - **Corrections to existing FAQs** — fix inaccuracies discovered during work
   - **Performance findings** — what worked, what didn't, with data
4. Write changes directly to the FAQ markdown files
5. **If new topic areas were added**, update the MCP server's `instructions` parameter (in the FastMCP constructor) and any corresponding CLAUDE.md directive so the LLM knows to query the FAQ for those topics. The instructions string is what tells the LLM when to use the FAQ — if a topic isn't listed there, the LLM won't know to ask.
6. Stage FAQ changes (including any server updates) alongside code changes

**If you learned something non-obvious during a session that would help the next developer (or the next Claude session), it belongs in a FAQ.** Write the entry directly — don't just mention it to the user and hope they do it.
