---
date: 2024-07-16
authors: [eriknovak]
description: >
  Anonipy can be used to anonymize a document such as PDF and word documents.
categories:
  - Tutorial
---

# Anonymizing documents

The [anonipy][anonipy] package was designed for anonymizing text. However, a lot of text data can be found in document form, such as PDFs, word documents, and other. Copying the text from the documents  to be anonymized can be cumbersome. The `anonipy` package provides utility functions that extracts the text from the documents.


In this blog post, we explain how `anonipy` can be used to anonymize texts in document form.

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

## Document anonymization

### Extracting the text from the document

Next, we will use the `anonipy` package to anonymize the text in the document. First, we must extract the text. This can be done using the package's utility function [open_file][anonipy.utils.file_system.open_file]. The function supports extraction of text from `doc`, `docx`, `pdf` and `txt` files.

To extract the text, using the following code:

```python
from anonipy.utils.file_system import open_file

file_path = "path/to/file.txt"
file_text = open_file(file_path)
```

where `file_path` is the path to the document we want to anonymize. The [open_file][anonipy.utils.file_system.open_file] will open the document, extract the content, and return it as a string.

Once this is done, we can start anonymizing the text, in a regular way.

### Extracting personal information from the text

Now we can identify and extract personal information from the text. We do this by using [NERExtractor][anonipy.anonymize.extractors.NERExtractor], an extractor that leverages the [GLiNER](https://github.com/urchade/GLiNER) span-based NER models.

It returns the text and the extracted entities.

```python
from anonipy.constants import LANGUAGES
from anonipy.anonymize.extractors import NERExtractor

# define the labels to be extracted and their types
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# initialize the entity extractor
extractor = NERExtractor(
    labels, lang=LANGUAGES.ENGLISH, score_th=0.5
)
# extract the entities from the original text
doc, entities = extractor(file_text)
```

To display the entities in the original text, we can use the  [display][anonipy.anonymize.extractors.NERExtractor.display] method:

```python
extractor.display(doc)
```


### Preparing the anonymization mapping

Next, we prepare the anonymization mapping. We do this by using the generators module part of the `anonipy` package. The generators are used to generate substitutes for the entities.

For example, we can use [MaskLabelGenerator][anonipy.anonymize.generators.MaskLabelGenerator] to generate substitutes using the language models to solve a `mask-filling` problem, i.e. finding the words that would be probabilistically suitable to replace the entity in the text.

The full list of available generators can be found in the [generators][anonipy.anonymize.generators] submodule.

Furthermore, we use the [PseudonymizationStrategy][anonipy.anonymize.strategies.PseudonymizationStrategy] to anonymize the text. More on anonymization strategies can be found in the [strategies][anonipy.anonymize.strategies] submodule.


```python
from anonipy.anonymize.generators import (
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)
from anonipy.anonymize.strategies import PseudonymizationStrategy

# initialize the generators
mask_generator = MaskLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()

# prepare the anonymization mapping
def anonymization_mapping(text, entity):
    if entity.type == "string":
        return mask_generator.generate(entity, text)
    if entity.label == "date":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_MONTH")
    if entity.label == "date of birth":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_YEAR")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"

# initialize the pseudonymization strategy
pseudo_strategy = PseudonymizationStrategy(mapping=anonymization_mapping)
```

### Anonymizing the text

Once we prepare the anonymization strategy, we can use it to anonymize the text.

```python
# anonymize the original text
anonymized_text, replacements = pseudo_strategy.anonymize(file_text, entities)
```

### Saving the anonymized text

Finally, we can save the anonymized text to a file. This can be done using the [write_file][anonipy.utils.file_system.write_file] function from the [file_system][anonipy.utils.file_system] submodule.

```python
from anonipy.utils.file_system import write_file

output_file = "path/to/output_file.txt"
write_file(anonymized_text, output_file, encode="utf-8")
```

Where `output_file` is the path to the file where the anonymized text will be saved.


## Conclusion

In this blog post, we show how one can anonymize a document using the `anonipy` package. We first used the [open_file][anonipy.utils.file_system.open_file] utility function to extract the content of the document and store it as a string. We then used the [NERExtractor][anonipy.anonymize.extractors.NERExtractor] to identify and extract personal information form the text, and the [PseudonymizationStrategy][anonipy.anonymize.strategies.PseudonymizationStrategy] in combination with various [generators][anonipy.anonymize.generators] to anonymize the text. Finally, we used the [write_file][anonipy.utils.file_system.write_file] utility function to save the anonymized text to a file.

This process is very straightforward and can be applied to almost any document type. Furthermore, it can be expanded to process multiple documents written in the same language at once. Stay tuned to see how this can be done in the future!

## Full code

```python
from anonipy.anonymize.extractors import NERExtractor
from anonipy.anonymize.generators import (
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)
from anonipy.anonymize.strategies import PseudonymizationStrategy

from anonipy.utils.file_system import open_file, write_file
from anonipy.constants import LANGUAGES

# =====================================
# Read the file content
# =====================================

# load the file content
file_path = "path/to/file.txt"
file_text = open_file(file_path)

# =====================================
# Extract the entities
# =====================================

# define the labels to be extracted and their types
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# initialize the entity extractor
extractor = NERExtractor(
    labels, lang=LANGUAGES.ENGLISH, score_th=0.5
)

# extract the entities from the original text
doc, entities = extractor(file_text)

# =====================================
# Prepare the anonymization strategy
#   and anonymize the text
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
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_MONTH")
    if entity.label == "date of birth":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_YEAR")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"

# initialize the pseudonymization strategy
pseudo_strategy = PseudonymizationStrategy(mapping=anonymization_mapping)

# anonymize the original text
anonymized_text, replacements = pseudo_strategy.anonymize(file_text, entities)

# =====================================
# Save the anonymized text
# =====================================

# save the anonymized text to a file
output_file = "path/to/output_file.txt"
write_file(anonymized_text, output_file, encode="utf-8")
```
