# Why BM25 Over Vectors

We chose BM25 (Okapi BM25) over vector/embedding-based search for the FAQ MCP. This was a deliberate decision, not a limitation.

## Reasons

1. **Zero dependencies** — No embedding model to download, no vector database to run, no API keys for an embedding service. The entire search implementation is ~40 lines of Python with only the `mcp` package as a dependency.

2. **Deterministic** — The same query always returns the same results. No model temperature, no embedding drift across versions, no surprises.

3. **Transparent** — You can reason about why a result ranked where it did. BM25 scores are a function of term frequency, document frequency, and document length — all inspectable.

4. **Good enough** — FAQ collections are typically tens to hundreds of documents. At this scale, BM25 provides excellent relevance. Vector search shines when you need semantic similarity across millions of documents; it's overkill here.

5. **No network required** — Works entirely offline. No API calls to embedding services, no latency from network round-trips.

6. **Instant startup** — Tokenizing and indexing hundreds of FAQ documents takes milliseconds. No model loading, no warmup.

## When Vectors Would Make Sense

If a project's FAQ collection grew to thousands of documents covering highly overlapping semantic territory (where keyword matching genuinely fails), vector search would be worth the dependency cost. For the typical FAQ MCP use case, that threshold is unlikely to be reached.
