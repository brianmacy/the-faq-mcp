# CI and Linting

## GitHub Actions CI

The project has CI via `.github/workflows/ci.yml` with two jobs:

### lint-and-test

Runs on Python 3.10, 3.12, and 3.13. Steps:

1. **ruff check** — lint `faq_server.py`
2. **ruff format --check** — verify formatting
3. **mypy --ignore-missing-imports** — type checking
4. **python -m py_compile** — syntax validation
5. **Server load test** — imports the server module and verifies FAQs are loaded and indexed

### markdown

Runs `npx prettier --check "**/*.md"` to validate markdown formatting across all `.md` files in the repo.

## Running Checks Locally

```bash
# Python linting and formatting
ruff check .claude/faq_server.py
ruff format --check .claude/faq_server.py
mypy --ignore-missing-imports .claude/faq_server.py
python3 -m py_compile .claude/faq_server.py

# Markdown formatting
npx prettier --check "**/*.md"

# Fix markdown formatting
npx prettier --write "**/*.md"

# Fix Python formatting
ruff format .claude/faq_server.py
```

## Action Pinning Policy

All GitHub Actions `uses:` references must be hash-pinned with a tag comment for security and reproducibility:

```yaml
# Good — hash-pinned with tag comment
- uses: actions/checkout@34e114876b0b11c390a56381ad16ebd13914f8d5 # v4

# Bad — tag reference (mutable, can be moved)
- uses: actions/checkout@v4
```

## Dependabot

`.github/dependabot.yml` is configured for two ecosystems, both on a **daily** interval with a **21-day cooldown**:

- **github-actions** — keeps action hash pins up to date
- **pip** — watches the `mcp` dependency via `.claude/requirements.txt`

The daily interval catches CVEs fast (security updates bypass the cooldown). The 21-day cooldown gates routine version bumps so they don't flood the repo with PRs.

**Why requirements.txt?** Dependabot cannot scan PEP 723 inline script metadata (the `# /// script` block in `faq_server.py`). We added `.claude/requirements.txt` as a parallel declaration so Dependabot can detect CVEs in the `mcp` dependency. The `requirements.txt` must be kept in sync with the PEP 723 metadata in `faq_server.py`.
