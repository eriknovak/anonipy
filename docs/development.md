---
title: Development
---

# Development

This section is for developers only. It describes the requirements, the setup process, how to run tests, and how to deploy.

## ✅ Requirements
Before starting the project make sure these requirements are available:

- [python][python]. The python programming language (v3.8 or higher).

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

## 📦️ Build package

To build the package, run:

```bash
# upgrade the build package
python -m pip install --upgrade build

# build the datachart package
python -m build
```

## 🚀 Deploy package

### Test PyPI

To deploy the package, run:

```bash
# upgrade the twine package
python -m pip install --upgrade twine

# deploy the datachart package to testpypi
python -m twine upload --repository testpypi dist/*
```

Next, to test the package published on testpypi, run:

```bash
# install a virtual environment
python -m venv venv

# activate the environment
. ./venv/bin/activate

# install the datachart package
pip install \
    --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    datachart
```
This way you can test the package without publishing it.

### Production PyPI

```bash
# upgrade the twine package
python -m pip install --upgrade twine

# deploy the datachart package to pypi
python -m twine upload dist/*
```

[python]: https://www.python.org/
[git]: https://git-scm.com/
[Material for MkDocs]: https://squidfunk.github.io/mkdocs-material/getting-started/