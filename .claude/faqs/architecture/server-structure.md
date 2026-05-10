# Server Structure

The FAQ MCP server is a single Python file (`faq_server.py`) with no external dependencies beyond the `mcp` package.

## File Layout

```
.claude/
├── faq_server.py          # MCP server implementation
├── faqs/                  # FAQ content (markdown files)
│   ├── <category>/        # One directory per topic area
│   │   ├── <title>.md     # One markdown file per FAQ entry
│   │   └── ...
│   └── ...
```

## Components

1. **BM25 Index** — tokenizer, document class with precomputed term frequencies, and the BM25 scoring engine
2. **FAQ Loader** — walks `faqs/<category>/*.md` at startup and populates the index
3. **FastMCP Server** — registers three tools and runs the MCP protocol over stdio

## Three Tools

| Tool                                          | Purpose                                                      |
| --------------------------------------------- | ------------------------------------------------------------ |
| `get_faq_categories()`                        | Lists all categories with article counts and titles          |
| `search_faqs(query, category?, max_results?)` | BM25 search with optional category filter, returns excerpts  |
| `get_faq(title, category?)`                   | Exact title lookup with fuzzy fallback, returns full content |

## Startup Flow

1. Walk `faqs/` directory tree, load all `.md` files
2. Pre-tokenize each document, compute term frequencies
3. Finalize BM25 index (compute average document length)
4. Register tools with FastMCP
5. Run MCP server on stdio

The entire startup takes milliseconds for typical FAQ collections (tens to hundreds of documents).

## Memory Efficiency

The `_Document` class uses `__slots__` instead of a regular class dict. This saves ~40% memory per document — meaningful when scaling to large FAQ collections.
