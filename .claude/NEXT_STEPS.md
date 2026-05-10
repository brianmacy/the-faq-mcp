# Next Steps

**Priority-ordered actionable items for the next session.**

## P0 — Must Do

1. **Commit all new files** — Everything is untracked. Stage and commit `.claude/`, `.github/`, `.gitignore`, `.mcp.json`, `CLAUDE.md`, `CHANGELOG.md`, and the updated `README.md`.
2. **Write a real README.md** — The current README is a stub (`# the-faq-mcp`). As an educational repo, the README is the primary entry point. It should cover:
   - What FAQ MCPs are and why they matter
   - How to use this repo as a reference implementation
   - How to adapt the pattern for your own project
   - Quick start guide
   - Link to the FAQ content for deeper reading

## P1 — Should Do

3. **Add a test suite** — At minimum:
   - Unit tests for the BM25 index (tokenization, scoring, ranking order)
   - Unit tests for FAQ loading (category discovery, file parsing)
   - Integration test: load real FAQs, run search queries, verify results
4. **Add standalone examples** — Show how to adapt the FAQ MCP pattern for other project types (Rust, TypeScript, multi-language)

## P2 — Nice to Have

5. **Add a contributing guide** — How to add new FAQ entries, naming conventions, review process
6. **Consider a `Makefile` or `justfile`** — Common commands (run server, run tests, lint)

## Done (completed this session)

- ~~Add CI with GitHub Actions~~ — Done. `.github/workflows/ci.yml` with lint-and-test (3 Python versions) + markdown prettier check. All actions hash-pinned.
- ~~Add a `.gitignore`~~ — Done. Excludes `__pycache__/`, `*.pyc`, `.claude/.faq-venv/`, `.claude/settings.local.json`, `.DS_Store`.
- ~~Prettier formatting~~ — Done. All 8 markdown files that had issues are now formatted correctly.
