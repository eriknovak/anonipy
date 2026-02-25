# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Uses uv for package management. Python >=3.10.

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[all]"
```

## Testing

```bash
# All tests
pytest

# Skip slow/integration tests
pytest -m "not slow and not integration"

# Single test file
pytest test/test_extractors.py

# Single test
pytest test/test_extractors.py::TestNERExtractor::test_ner_extractor_extract_default_params_input

# With coverage (CI threshold: 70%)
pytest --cov=anonipy --cov-report=term-missing --cov-fail-under=70
```
