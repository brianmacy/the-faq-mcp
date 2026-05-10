# FAQ Data Format

## Directory Structure

Each category is a directory under `.claude/faqs/`. Each FAQ entry is a single markdown file within a category directory.

```
.claude/faqs/
├── architecture/
│   ├── bm25-search.md
│   ├── server-structure.md
│   └── faq-data-format.md
├── getting-started/
│   └── setup.md
└── maintenance/
    └── keeping-faqs-updated.md
```

## File Naming

- Use `kebab-case-title.md` for filenames
- The server normalizes the filename stem to a display title: `bm25-search` becomes `bm25 search`
- Title matching is case-insensitive and dash/space-normalized, so queries work with either form

## Markdown Content

FAQ files are plain markdown. The recommended structure:

```markdown
# Title

Brief description of the topic.

## Section

Details, code examples, etc.
```

Use standard markdown features: headings, code blocks with language specifiers, tables, lists, emphasis. The server indexes the full text content for BM25 search.

## Adding a New Category

Create a new directory under `.claude/faqs/` with a descriptive kebab-case name. Add `.md` files inside it. The server discovers new categories automatically at startup — no configuration needed.

## Adding a New FAQ Entry

Create a new `.md` file in the appropriate category directory. The server picks it up on next restart. If the new entry covers a topic area not listed in the server's `instructions` string, update the instructions so the LLM knows to query for it.
