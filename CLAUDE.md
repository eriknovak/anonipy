# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Uses uv for package management. Python >=3.10.

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[all]"
```

## Linting

Ruff lints and formats; config in `pyproject.toml`. CI and the pre-commit hook run both checks.

```bash
ruff check --fix .
ruff format .
```

## Testing

`pytest` runs only the fast tests (`addopts` deselects `slow` and `integration`). They use fake models from `test/conftest.py` and `test/test_generators.py`, so model-backed code is tested without downloads.

```bash
# Fast tests (default)
pytest

# Tests with real models (downloads several GB)
pytest -m "slow or integration"

# All tests
pytest -m ""

# Single test file
pytest test/test_extractors.py

# Single test
pytest test/test_extractors.py::test_ner_extractor_fake_returns_tagged_entities

# With coverage (CI threshold: 90%)
pytest --cov=anonipy --cov-report=term-missing --cov-fail-under=90
```

## Agent skills

### Issue tracker

Issues live in this repo's GitHub Issues, managed with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`) plus the `dev`/`lab` kind labels. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
