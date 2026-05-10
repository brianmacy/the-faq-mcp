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

`.github/dependabot.yml` is configured for two ecosystems:

- **github-actions** — keeps action pins up to date (weekly check)
- **pip** — watches the `mcp` dependency in `.claude/` (weekly check)
