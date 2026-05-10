# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Read [README.md](README.md) for the full project context: what FAQ MCPs are, why they exist, how this reference implementation works, and how to adapt it for other projects.

## FAQ MCP Directive

> **MANDATORY: You MUST use the `the-faq-mcp` MCP tools for ALL questions about FAQ MCP design, architecture, implementation, configuration, and maintenance. Do NOT guess or rely on training data — query `search_faqs(query)` or `get_faq(title)` FIRST.**

## Keeping FAQs Updated

FAQs are the project's institutional memory. They must be maintained as a living archive, not left to rot.

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
5. **If new topic areas were added**, update the MCP server's `instructions` parameter (in the FastMCP constructor) and this directive so the LLM knows to query the FAQ for those topics.
6. Stage FAQ changes (including any server updates) alongside code changes

**If you learned something non-obvious during a session that would help the next developer (or the next Claude session), it belongs in a FAQ.** Write the entry directly — don't just mention it to the user and hope they do it.
