# Next Steps

**Priority-ordered actionable items for the next session.**

## P0 — Must Do

1. **Add a test suite** — At minimum:
   - Unit tests for the BM25 index (tokenization, scoring, ranking order)
   - Unit tests for FAQ loading (category discovery, file parsing)
   - Integration test: load real FAQs, run search queries, verify results

## P1 — Should Do

2. **Test and document support for other LLM tools** — Cursor, Copilot, Windsurf, and other MCP-capable tools. Verify the `.mcp.json` launcher works, document any tool-specific configuration, and provide setup prompts for non-Claude tools.
3. **Add standalone examples** — Show how to adapt the FAQ MCP pattern for other project types
