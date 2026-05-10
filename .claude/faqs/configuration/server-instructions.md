# Server Instructions

The `instructions` parameter in the FastMCP constructor is critical — it tells the LLM when and why to use the FAQ MCP.

## How Instructions Work

When the MCP server is registered with Claude Code, the `instructions` string is presented to the LLM as part of the server's metadata. This is the LLM's first (and sometimes only) signal about what the FAQ covers and when to query it.

## Writing Effective Instructions

The instructions should:

1. **State that usage is mandatory** — LLMs will skip tool calls if they think they already know the answer. Be explicit that querying the FAQ comes before guessing.
2. **List the topic areas covered** — The LLM can only query for topics it knows exist. If you add FAQs about a new topic and don't update the instructions, the LLM won't know to look.
3. **Clarify the boundary with CLAUDE.md** — CLAUDE.md handles coding conventions and rules that should always be in context. The FAQ handles everything else: procedures, architecture, decisions, status.

## Example

```python
mcp = FastMCP(
    "my-project-faq",
    instructions=(
        "MANDATORY: You MUST use this FAQ server for ALL questions about "
        "build procedures, test execution, architecture, environment setup, "
        "and project decisions. Do NOT guess or rely on training data — "
        "query these tools FIRST. Topics covered: building, testing, "
        "deployment, architecture, design decisions, troubleshooting, "
        "project status, and environment setup. When in doubt, "
        "search_faqs() before exploring the codebase."
    ),
)
```

## Keeping Instructions Current

When new FAQ categories or topic areas are added, the `instructions` string must be updated to include them. This is part of the FAQ maintenance workflow — if you add a FAQ and don't update the instructions, the LLM won't know to query for that topic.

A matching directive in the project's CLAUDE.md reinforces the instructions from the other side:

```markdown
> **MANDATORY: You MUST use the `my-project-faq` MCP tools for ALL build, test,
> architecture, and planning tasks. Do NOT guess or use training data — query
> `search_faqs(query)` or `get_faq(title)` FIRST.**
```

Belt and suspenders — the MCP server tells the LLM "use me," and CLAUDE.md tells the LLM "use the FAQ server."
