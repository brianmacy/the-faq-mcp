# Why FAQ MCPs

FAQ MCPs solve several critical problems when working with LLMs on codebases:

## LLM Training Data Is Stale and Wrong

LLM training cutoffs mean they guess at build commands, API signatures, and architecture patterns — and often guess wrong. A FAQ MCP gives them a queryable, authoritative source of truth that's version-controlled alongside the code. This is especially critical for private repositories whose code and documentation will never appear in any LLM's training data.

## LLMs Forget What They've Done Before

The most maddening failure mode: an LLM that has successfully built, tested, and deployed your project hundreds of times will, after a context reset, forget the exact commands and fumble through it like it's the first time. Environment setup, build procedures, test execution, result evaluation — these are rote, repeatable tasks that should never require re-discovery. A FAQ MCP makes these procedures queryable so the LLM gets the right answer on the first try, every session.

## Institutional Memory

When a session ends or a developer switches projects, hard-won context evaporates. FAQs persist that knowledge — "we tried X, it didn't work because Y, do Z instead" — so the next session or person doesn't repeat the same mistakes. This solves the "hit by a bus" problem: design decisions, architectural rationale, current project status, and the _why_ behind choices are captured in a searchable, durable form.

## Rapid Onboarding

The FAQ captures not just _what_ the project does but _why_ — current status, future TODOs, reasons why certain approaches were rejected. A new team member (human or LLM) can get productive quickly by querying the FAQ instead of reverse-engineering decisions from code or waiting for a knowledge transfer meeting.

## Token-Efficient Context

Instead of stuffing everything into CLAUDE.md (which is always loaded into the LLM context), the FAQ MCP lets the LLM pull specific knowledge on demand via tool calls. Keeps the context window lean while making deep knowledge accessible.

## Zero External Dependencies

BM25 search is built into the server (~40 lines of Python). No Elasticsearch, no vector DB, no API keys. Just the `mcp` package and markdown files.
