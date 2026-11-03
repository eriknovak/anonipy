---
title: Development
---

# Development

This section is for developers only. It describes the requirements, the setup process, how to run tests, and how to deploy.

## Requirements

Before starting the project make sure these requirements are available:

- [python][python]. The python programming language (v3.10, v3.11, v3.12, v3.13).

- [git][git]. For versioning your code.

## Setup

### Create the python environment

To create a python virtual environment using `venv`, simply run the following
commands:

```bash
# create a new virtual environment
python -m venv venv

# activate the environment (UNIX)
. ./venv/bin/activate

# activate the environment (WINDOWS)
./venv/Scripts/activate

# deactivate the environment (UNIX & WINDOWS)
deactivate
```

### Install

To install the requirements run:

```bash
pip install -e .[all]
```

**Githooks.** Githooks enable automatic commit and push hooks. The project is configured to check linting and formatting on each commit and to run the fast tests on each push. See the configuration in `.githooks.ini`. To enable git hooks, run:

```bash
githooks
```

## Linting

The code is linted and formatted with [ruff], configured in `pyproject.toml`. CI fails when either check fails. To fix the code before committing, run:

```bash
ruff check --fix .
ruff format .
```

## Tests

To run the fast tests, simply run:

```bash
pytest
```

They replace the GLiNER and Hugging Face models with small fakes, so they run offline in a few seconds. CI runs them on every push and pull request and requires 90% coverage.

Tests marked `slow` or `integration` load the real models, which downloads several GB on the first run. They are skipped by default; CI runs them weekly. To run them, or the whole suite, run:

```bash
# only the tests with real models
pytest -m "slow or integration"

# all tests
pytest -m ""
```

## Documentation

To start live-reloading the documentation, run:

```bash
mkdocs serve -a localhost:9999
```

When suggesting changes, please refer to the [Material for MkDocs] documentation.

### Deployment

Once the changes are accepted into the project, the GitHub Actions automatically
deploy the documentation to the `gh-pages` branch.

[python]: https://www.python.org/
[git]: https://git-scm.com/
[Material for MkDocs]: https://squidfunk.github.io/mkdocs-material/getting-started/
[ruff]: https://docs.astral.sh/ruff/
