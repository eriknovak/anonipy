# Annonymizer

This is a template repository for creating an experiment environment in Python. It intends to speed up the research process - reducing the repository structure design - and to have it clean and concise through multiple experiments.

Inspired by the [cookiecutter] folder structure.

**Instructions:**

- Search for all TODOs in the project and add the appropriate values
- Rename this README title and description

## ☑️ Requirements

Before starting the project make sure these requirements are available:

- [python]. For setting up the environment and Python dependencies (version 3.8 or higher).
- [git]. For versioning your code.

## 🛠️ Setup

### Create a python environment

First, create a virtual environment where all the modules will be stored.

#### Using venv

Using the `venv` command, run the following commands:

```bash
# create a new virtual environment
python -m venv venv

# activate the environment (UNIX)
source ./venv/bin/activate

# activate the environment (WINDOWS)
./venv/Scripts/activate

# deactivate the environment (UNIX & WINDOWS)
deactivate
```

### Install

Check the `requirements.txt` file. If you have any additional requirements, add them here.

To install the requirements run:

```bash
pip install -e .
```

## 🗃️ Data

TODO: Provide information about the data used in the experiments

- Where is the data found
- How is the data structured

## ⚗️ Experiments

To run the experiments, run the following commands:

```bash
TODO: Provide scripts for the experiments
```

### Results

The results folder contains the experiment

TODO: Provide a list/table of experiment results

## 📦️ Available models

This project produced the following models:

- TODO: Name and the link to the model

## 🚀 Using the trained model

When the model is trained, the following script shows how one can use the model:

```python
TODO: Provide an example of how to use the model
```

## 📚 Papers

In case you use any of the components for your research, please refer to (and cite) the papers:

TODO: Paper

### 📓 Related work

TODO: Related work

## 🚧 Work In Progress

- [ ] Setup script
- [ ] Code for data preparation
- [ ] Code for model training
- [ ] Code for model validation
- [ ] Code for model evaluation

## 📣 Acknowledgments

TODO: Acknowledgements

[cookiecutter]: https://drivendata.github.io/cookiecutter-data-science/
[python]: https://www.python.org/
[git]: https://git-scm.com/
