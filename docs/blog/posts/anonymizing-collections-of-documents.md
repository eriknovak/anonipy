---
date: 2024-05-23
authors: [eriknovak]
description: >
  Our package can be used to anonymize collections of documents.
categories:
  - Tutorial
---

# Anonymizing collections of documents

In the previous blog post, we showed how one can anonymize text in document form.
While the code is useful for processing a single document, anonymizing a collection
of documents can take time if we run the script for each document separately.

In this blog post, we show how one can anonymize collections of documents. The
process is similar to the previous blog post, but loads all required components
only once, and anonymizes all documents in one go.

<!-- more -->

!!! info "Prerequisites"
    To use the `anonipy` package, we must have Python version 3.8 or higher
    installed on the machine.

## Installation

Before we start, we must first install the `anonipy` package. To do that, run the
following command in the terminal:

```bash
pip install anonipy
```

This will install the `anonipy` package, which contains all of the required modules.

If you already installed it and would like to update it, run the following command:

```bash
pip install anonipy --upgrade
```

## Preparing the components

First, let us prepare all of the components for the anonymization process. It
consists of preparing the entity extractor, the anonymization strategy, and the
generators for the anonymization process.

```python
from anonipy.anonymize.extractors import EntityExtractor
from anonipy.anonymize.generators import (
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)
from anonipy.anonymize.strategies import PseudonymizationStrategy
from anonipy.constants import LANGUAGES

# =====================================
# Prepare the entity extractor
# =====================================

# define the labels to be extracted and their types
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# initialize the entity extractor
entity_extractor = EntityExtractor(
    labels, lang=LANGUAGES.ENGLISH, score_th=0.5
)

# =====================================
# Prepare the anonymization strategy
# =====================================

# initialize the generators
mask_generator = MaskLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()

# prepare the anonymization mapping
def anonymization_mapping(text, entity):
    if entity.type == "string":
        return mask_generator.generate(entity, text)
    if entity.label == "date":
        return date_generator.generate(entity, output_gen="middle_of_the_month")
    if entity.label == "date of birth":
        return date_generator.generate(entity, output_gen="middle_of_the_year")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"

# initialize the pseudonymization strategy
pseudo_strategy = PseudonymizationStrategy(mapping=anonymization_mapping)
```

### Anonymizing the collection of documents

Now, let us anonymize all of the documents in the collection. We first prepare
a folder containing the documents, that we want to anonymize. The path to the
folder will be available via the `input_folder` variable.

We will, one-by-one, read all of the documents in the folder, extract the text
from each document, and anonymize the text.

Finally, we will store the anonymized text in another folder. The path to the
folder will be available via the `output_folder` variable.

```python
import os
from os.path import isfile, join
from anonipy.utils.file_system import open_file, write_file, write_json

# prepare the input and output folder paths
input_folder = "path/to/input/folder"
output_folder = "path/to/output/folder"

# prepare a list of file paths in the input folder
file_names = [
    f for f in os.listdir(input_folder) if isfile(join(input_folder, f))
]

# iterate through each file
for file_name in file_names:
    # extract the text from the document
    file_text = open_file(join(input_folder, file_name))
    # extract the entities from the text
    doc, entities = entity_extractor(file_text)
    # anonymize the text
    anonymized_text, replacements = pseudo_strategy.anonymize(file_text, entities)
    # write the anonymized text into the output folder
    output_file_name = ".".join(file_name.split(".")[:-1]) + "_anonymized"
    write_file(anonymized_text, join(output_folder, output_file_name) + ".txt")
    write_json(replacements, join(output_folder, output_file_name) + ".json")

```

Given the above code, we can anonymize all of the documents in the collection without
loading and preparing the extractor, generators and strategy every time.


## Conclusion

In this blog post, we show how one can anonymize collections of documents in out
go using the `anonipy` package. We first prepare the components for the anonymization
process. We then find all of the files we want to anonymize and anonymize them.
Each anonymized file is finally stored in a separate folder which contains the
anonymized text.

