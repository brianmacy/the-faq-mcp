# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp"]
# ///
"""FAQ MCP Server — queryable project FAQ with BM25 search.

Uses BM25 (Okapi BM25) ranking for search relevance. No external
dependencies beyond the `mcp` package.
"""

import math
import os
import re
import sys
import threading
from pathlib import Path

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print(
        "ERROR: The 'mcp' package is not installed.\n"
        "\n"
        "This script is designed to be run via uv with PEP 723 inline metadata:\n"
        "    uv run --script .claude/faq_server.py\n"
        "\n"
        "If you don't have uv installed:\n"
        "    pip install uv   # or: brew install uv\n"
        "\n"
        "Alternatively, install the dependency manually:\n"
        "    pip install mcp\n"
        "    python .claude/faq_server.py",
        file=sys.stderr,
    )
    sys.exit(1)

FAQ_DIR = Path(__file__).parent / "faqs"

_K1 = 1.2
_B = 0.75

_TOKEN_RE = re.compile(r"[a-z0-9_]+")


def _tokenize(text: str) -> list[str]:
    return _TOKEN_RE.findall(text.lower())


class _Document:
    __slots__ = ("category", "title", "content", "tokens", "tf", "length")

    def __init__(self, category: str, title: str, content: str) -> None:
        self.category = category
        self.title = title
        self.content = content
        self.tokens = _tokenize(title + " " + content)
        self.length = len(self.tokens)
        self.tf: dict[str, int] = {}
        for tok in self.tokens:
            self.tf[tok] = self.tf.get(tok, 0) + 1


class _BM25Index:
    def __init__(self) -> None:
        self.docs: list[_Document] = []
        self.df: dict[str, int] = {}
        self.avgdl: float = 0.0

    def add(self, doc: _Document) -> None:
        self.docs.append(doc)
        for term in set(doc.tf):
            self.df[term] = self.df.get(term, 0) + 1

    def finalize(self) -> None:
        if self.docs:
            self.avgdl = sum(d.length for d in self.docs) / len(self.docs)

    def search(
        self,
        query: str,
        category: str | None = None,
        max_results: int = 5,
    ) -> list[tuple[_Document, float]]:
        terms = _tokenize(query)
        if not terms:
            return []
        n = len(self.docs)
        scores: list[tuple[_Document, float]] = []
        for doc in self.docs:
            if category and doc.category != category:
                continue
            score = 0.0
            for t in terms:
                df = self.df.get(t, 0)
                if df == 0:
                    continue
                idf = math.log((n - df + 0.5) / (df + 0.5) + 1.0)
                tf = doc.tf.get(t, 0)
                if tf == 0:
                    continue
                numerator = tf * (_K1 + 1.0)
                denominator = tf + _K1 * (
                    1.0 - _B + _B * doc.length / max(self.avgdl, 1.0)
                )
                score += idf * numerator / denominator
            if score > 0:
                scores.append((doc, score))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:max_results]


_faqs: dict[str, dict[str, str]] = {}
_index = _BM25Index()
_fingerprint: tuple[tuple[str, int], ...] = ()
_reindex_lock = threading.Lock()


def _compute_fingerprint() -> tuple[tuple[str, int], ...]:
    """Fast FAQ directory fingerprint from file paths and mtimes."""
    if not FAQ_DIR.is_dir():
        return ()
    entries: list[tuple[str, int]] = []
    for cat_entry in os.scandir(FAQ_DIR):
        if not cat_entry.is_dir(follow_symlinks=False):
            continue
        for file_entry in os.scandir(cat_entry.path):
            if file_entry.name.endswith(".md") and file_entry.is_file(
                follow_symlinks=False
            ):
                entries.append((file_entry.path, file_entry.stat().st_mtime_ns))
    entries.sort()
    return tuple(entries)


def _load_faqs() -> None:
    global _faqs, _index, _fingerprint
    new_faqs: dict[str, dict[str, str]] = {}
    new_index = _BM25Index()
    if FAQ_DIR.is_dir():
        for cat_dir in sorted(FAQ_DIR.iterdir()):
            if not cat_dir.is_dir():
                continue
            category = cat_dir.name
            new_faqs[category] = {}
            for md in sorted(cat_dir.glob("*.md")):
                title = md.stem.replace("-", " ")
                content = md.read_text(encoding="utf-8")
                new_faqs[category][title] = content
                new_index.add(_Document(category, title, content))
        new_index.finalize()
    _faqs = new_faqs
    _index = new_index
    _fingerprint = _compute_fingerprint()


def _refresh_if_stale() -> None:
    if not _reindex_lock.acquire(blocking=False):
        return
    try:
        if _compute_fingerprint() != _fingerprint:
            _load_faqs()
    finally:
        _reindex_lock.release()


def _schedule_refresh() -> None:
    """Trigger a background reindex check after serving the response."""
    threading.Thread(target=_refresh_if_stale, daemon=True).start()


_load_faqs()

_IMPROVEMENT_FOOTER = (
    "\n\n---\n"
    "*If this FAQ is incomplete, unclear, outdated, or could be improved, "
    "please suggest specific improvements to the user (e.g., missing details, "
    "better examples, corrections). Help keep these FAQs accurate and useful.*"
)


mcp = FastMCP(
    "the-faq-mcp",
    instructions=(
        "MANDATORY: You MUST use this FAQ server for ALL questions about FAQ MCP "
        "design, architecture, implementation, configuration, and maintenance. "
        "Do NOT guess or rely on training data — query these tools FIRST. "
        "Topics covered: why FAQ MCPs exist, server architecture, BM25 search, "
        "FAQ data format, MCP configuration, server instructions, CI and linting, "
        "getting started and setup, keeping FAQs updated, project status, and "
        "design decisions (BM25 vs vectors, markdown files). "
        "When in doubt, search_faqs() before exploring the codebase."
    ),
)


@mcp.tool()
def get_faq_categories() -> str:
    """List all FAQ categories with the number of articles in each."""
    if not _faqs:
        return "No FAQ categories found. Ensure .claude/faqs/ contains category directories with .md files."
    lines = []
    for cat in sorted(_faqs):
        count = len(_faqs[cat])
        titles = ", ".join(sorted(_faqs[cat]))
        lines.append(f"**{cat}** ({count}): {titles}")
    result = "\n".join(lines)
    _schedule_refresh()
    return result


@mcp.tool()
def search_faqs(query: str, category: str | None = None, max_results: int = 5) -> str:
    """Search FAQs using BM25 ranking. Returns titles + matching excerpts.

    Args:
        query: keyword(s) to search for
        category: optional category filter
        max_results: max results to return (default 5)
    """
    results = _index.search(query, category=category, max_results=max_results)
    if not results:
        _schedule_refresh()
        return f"No results for '{query}'."

    lines = []
    for doc, score in results:
        query_lower = query.lower()
        content_lower = doc.content.lower()
        idx = content_lower.find(query_lower)
        matched_len = len(query)
        if idx < 0:
            for term in _tokenize(query):
                idx = content_lower.find(term)
                if idx >= 0:
                    matched_len = len(term)
                    break
        if idx >= 0:
            start = max(0, idx - 80)
            end = min(len(doc.content), idx + matched_len + 120)
            excerpt = (
                ("..." if start > 0 else "")
                + doc.content[start:end].strip()
                + ("..." if end < len(doc.content) else "")
            )
        else:
            excerpt = doc.content[:200].strip() + (
                "..." if len(doc.content) > 200 else ""
            )
        lines.append(
            f"### [{doc.category}] {doc.title} (score: {score:.2f})\n{excerpt}\n"
        )
    result = "\n".join(lines) + _IMPROVEMENT_FOOTER
    _schedule_refresh()
    return result


@mcp.tool()
def get_faq(title: str, category: str | None = None) -> str:
    """Get full content of a specific FAQ by title.

    Args:
        title: FAQ title (use dashes or spaces, case-insensitive)
        category: optional category to narrow the search
    """
    title_normalized = title.lower().replace("-", " ")

    cats = [category] if category and category in _faqs else sorted(_faqs)
    for cat in cats:
        for faq_title, content in _faqs.get(cat, {}).items():
            if faq_title.lower() == title_normalized:
                _schedule_refresh()
                return f"# [{cat}] {faq_title}\n\n{content}" + _IMPROVEMENT_FOOTER

    for cat in cats:
        for faq_title, content in _faqs.get(cat, {}).items():
            if (
                title_normalized in faq_title.lower()
                or faq_title.lower() in title_normalized
            ):
                _schedule_refresh()
                return f"# [{cat}] {faq_title}\n\n{content}" + _IMPROVEMENT_FOOTER

    _schedule_refresh()
    return f"FAQ '{title}' not found. Use get_faq_categories() to see available FAQs."


if __name__ == "__main__":
    mcp.run()
