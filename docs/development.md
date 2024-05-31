---
title: Development
---

# Development

This section is for developers only. It describes the requirements, the setup process, how to run tests, and how to deploy.

## ✅ Requirements
Before starting the project make sure these requirements are available:

- [python][python]. The python programming language (v3.8, v3.9, v3.10, v3.11).

- [git][git]. For versioning your code.


## 🛠️ Setup

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

**Githooks.** Githooks enable automatic commit and push hooks. The project is configured to run tests on each commit and to run tests and format the code on each push. See the configuration in `.githooks.ini`. To enable git hooks, run:

```bash
githooks
```

## 🧪 Tests

To run existing tests, simply run:

```bash
python -m unittest discover test
```

## 📝 Documentation

To start live-reloading the documentation, run:

```bash
mkdocs serve
```

When suggesting changes, please refer to the [Material for MkDocs] documentation.

### Deployment

Once the changes are accepted into the project, the GitHub Actions automatically
deploy the documentation to the `gh-pages` branch.


[python]: https://www.python.org/
[git]: https://git-scm.com/
[Material for MkDocs]: https://squidfunk.github.io/mkdocs-material/getting-started/