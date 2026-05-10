# Keeping FAQs Updated

The FAQ is only as good as the discipline of keeping it current. A stale FAQ is worse than no FAQ — it gives the LLM confident wrong answers.

## Before Making Changes

Before acting on assumptions or training data, query the FAQ MCP first:

```
search_faqs("topic relevant to the task")
get_faq("specific FAQ title if known")
```

This applies to:

- **Environment setup** — how to configure the dev environment, required env vars, dependency installation
- **Build procedures** — exact commands, flags, build systems, platform-specific notes
- **Test execution and evaluation** — how to run tests, what passing/failing looks like, how to interpret results
- **Architecture and design** — why the code is structured the way it is, what patterns to follow
- **Prior decisions** — what was tried before, what was rejected and why

Do NOT guess at procedures the project has already documented. Query first, act second.

## After Making Changes

Before committing, review whether any FAQ entries need updating:

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
4. Write changes directly to the FAQ markdown files
5. If new topic areas were added, update the server's `instructions` parameter and any CLAUDE.md directive
6. Stage FAQ changes alongside code changes

If you learned something non-obvious that would help the next developer or the next LLM session, it belongs in a FAQ. Write the entry directly.
