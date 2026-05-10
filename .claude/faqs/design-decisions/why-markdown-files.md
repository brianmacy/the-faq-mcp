# Why Markdown Files

FAQ content is stored as plain markdown files in a directory hierarchy, not in a database, YAML, JSON, or any other structured format.

## Reasons

1. **Human-readable and editable** — Any developer can read, write, and review FAQs with no special tooling. They render natively on GitHub, GitLab, and in any editor.

2. **Git-friendly** — Markdown diffs are clean and reviewable in pull requests. You can see exactly what changed in a FAQ entry, who changed it, and when.

3. **No schema to maintain** — Adding a new FAQ is creating a file. Adding a new category is creating a directory. No migrations, no schema updates, no configuration.

4. **Rich content support** — Code blocks with syntax highlighting, tables, links, emphasis, headings — all standard markdown that the LLM can parse and present.

5. **Version-controlled alongside code** — FAQs live in the same repo as the code they document. They're branched, merged, and reviewed together.

## Rejected Alternatives

- **YAML/JSON** — Adds a serialization layer with no benefit. Markdown content embedded in YAML is harder to read and edit. Escaping rules create friction.
- **Database (SQLite, etc.)** — Adds a runtime dependency and makes diffs opaque. The FAQ collection is small enough that file-based access is instant.
- **Single large file** — Doesn't scale. Hard to review diffs when unrelated FAQs change in the same file. Category organization is lost.
