# BM25 Search

The FAQ MCP server uses Okapi BM25 for search ranking. This is a proven information retrieval algorithm that requires zero external dependencies — the entire implementation is ~40 lines of Python.

## Why BM25 Over Simple Keyword Matching

BM25 accounts for:

- **Term frequency (tf)** — how often a term appears in a document
- **Inverse document frequency (idf)** — rare terms are weighted higher than common ones
- **Document length normalization** — penalizes long documents to favor dense, relevant matches

Simple keyword matching (substring search) returns everything that contains the word, with no ranking. BM25 ranks results by relevance.

## Why BM25 Over Vector/Embedding Search

- Zero dependencies — no embedding model, no vector database, no API keys
- Deterministic — same query always returns same results
- Transparent — you can reason about why a result ranked where it did
- Fast — no model inference, just arithmetic over precomputed term frequencies
- Good enough — for FAQ collections of tens to hundreds of documents, BM25 is more than adequate

## Tuning Parameters

```python
K1 = 1.2  # Term frequency saturation — higher values give more weight to repeated terms
B = 0.75  # Document length normalization — 0 ignores length, 1 fully normalizes
```

These are the standard BM25 parameters used in most production search systems. There is rarely a reason to change them for FAQ-sized collections.

## Implementation Pattern

```python
# Tokenize: lowercase, split on non-alphanumeric
tokens = re.compile(r"[a-z0-9_]+").findall(text.lower())

# Score: for each query term, compute idf * tf_component
idf = log((N - df + 0.5) / (df + 0.5) + 1.0)
tf_score = (tf * (K1 + 1)) / (tf + K1 * (1 - B + B * doc_len / avg_doc_len))
score += idf * tf_score
```
