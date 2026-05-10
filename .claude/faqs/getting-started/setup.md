# Setup

## Prerequisites

- Python 3.10+
- `uv` (recommended) or `pip`

## Quick Start

1. **Copy the server and directory structure** into your project:

```
.claude/
├── faq_server.py
├── faqs/
│   └── (your categories and FAQ files)
```

2. **Create `.mcp.json`** at your repo root (see the `mcp-json-setup` FAQ for the full launcher chain).

3. **(Optional) Create `.claude/settings.local.json`** to skip the approval prompt — Claude Code will discover the server from `.mcp.json` and prompt on first use even without this:

```json
{
  "enabledMcpjsonServers": ["your-server-name"],
  "enableAllProjectMcpServers": true
}
```

4. **Add a directive to your CLAUDE.md** telling the LLM to use the FAQ:

```markdown
> **MANDATORY: You MUST use the `your-server-name` MCP tools for ALL build,
> test, architecture, and planning tasks. Do NOT guess or use training data —
> query `search_faqs(query)` or `get_faq(title)` FIRST.**
```

5. **Create your first FAQ category and entry:**

```bash
mkdir -p .claude/faqs/getting-started
# Write a markdown file covering your project's build procedure, for example
```

6. **Test the server:**

```bash
uv run --script .claude/faq_server.py
# Or if mcp is installed:
python .claude/faq_server.py
```

The server runs on stdio — Claude Code will launch it automatically via `.mcp.json`.

## What to Document First

Start with the things that cause the most pain when an LLM gets them wrong:

1. **How to build the project** — exact commands, prerequisites, platform-specific notes
2. **How to run tests** — commands, expected output, how to interpret results
3. **Environment setup** — required env vars, dependencies, configuration
4. **Architecture overview** — why the code is structured the way it is
