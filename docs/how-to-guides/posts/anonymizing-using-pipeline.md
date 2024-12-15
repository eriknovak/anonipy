---
date: 2024-12-11
authors: [eriknovak]
description: >
  Anonipy now has a pipeline for streamlining text anonymization.
categories:
  - Tutorial
---

# Document anonymization using pipeline

In this blog post, we show how one can anonymize documents using the new `Pipeline`
module. The module allows for a streamlined process of anonymizing documents, where
the user defines how the anonymization should be performed and the locations, where
the documents to be anonymized are located and where the anonymized documents should
be stored.

The pipeline will automatically extract the text from the documents, anonymize
the text, and store the anonymized text in the output folder.

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
from anonipy.anonymize.extractors import NERExtractor
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    DateGenerator,
    NumberGenerator,
)
from anonipy.anonymize.strategies import PseudonymizationStrategy
from anonipy.constants import LANGUAGES

# =====================================
# Prepare the entity extractors
# =====================================

# define the NER labels to be extracted and their types
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# initialize the extractor
extractor = NERExtractor(
    labels, lang=LANGUAGES.ENGLISH, score_th=0.5
)

# =====================================
# Prepare the anonymization strategy
# =====================================

# initialize the generators
llm_generator = LLMLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()

# prepare the anonymization mapping
def anonymization_mapping(text, entity):
    if entity.type == "string":
        return llm_generator.generate(entity, text)
    if entity.label == "date":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_MONTH")
    if entity.label == "date of birth":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_YEAR")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"

# initialize the pseudonymization strategy
strategy = PseudonymizationStrategy(mapping=anonymization_mapping)
```

### Anonymizing the documents using the pipeline

Now, let prepare the pipeline for anonymizing the documents. The pipeline is
available in the [anonipy.anonymize.pipeline] module. We will use the pipeline
to anonymize all of the documents in a folder.

```python
from anonipy.anonymize.pipeline import Pipeline

pipeline = Pipeline(extractor, strategy)
```

Let us now assume that the documents are stored in a folder called `path/to/input/folder`.
We want to anonymize all of the documents in the folder and store the anonymized
documents in another folder called `path/to/output/folder`.

```python
input_folder = "path/to/input/folder"
output_folder = "path/to/output/folder"
file_mapping = pipeline.anonymize(input_folder, output_folder, flatten=True)# (1)!
```

1. The `flatten` parameter specifies whether the pipeline should flatten the
   output folder structure. If `True`, the pipeline will store all of the anonymized
   documents in the output folder. If `False`, the pipeline will store the anonymized
   documents in the same folder structure as the input folder.

The `anonymize` method will extract the text from each document in the input folder and subfolders,
anonymize the text, and store the anonymized text in the output folder. The method
returns a dictionary where the keys are the file paths of the original documents
and the values are the file paths of the anonymized documents.

## Conclusion

In this blog post, we show how one can anonymize collections of documents using
the new `Pipeline` class. We first prepare the entity extractor, the anonymization
strategy, and the generators for the anonymization process. After that, we initialize
the `Pipeline` class and use it to anonymize all of the documents in the input folder,
and store the anonymized documents in the output folder.

## Full code

```python
from anonipy.anonymize.extractors import NERExtractor
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    DateGenerator,
    NumberGenerator,
)
from anonipy.anonymize.strategies import PseudonymizationStrategy
from anonipy.anonymize.pipeline import Pipeline
from anonipy.constants import LANGUAGES

# =====================================
# Prepare the entity extractors
# =====================================

# define the NER labels to be extracted and their types
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# initialize the extractor
extractor = NERExtractor(
    labels, lang=LANGUAGES.ENGLISH, score_th=0.5
)

# =====================================
# Prepare the anonymization strategy
# =====================================

# initialize the generators
llm_generator = LLMLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()

# prepare the anonymization mapping
def anonymization_mapping(text, entity):
    if entity.type == "string":
        return llm_generator.generate(entity, text)
    if entity.label == "date":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_MONTH")
    if entity.label == "date of birth":
        return date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_YEAR")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"

# initialize the pseudonymization strategy
strategy = PseudonymizationStrategy(mapping=anonymization_mapping)

# ===============================================
# Initialize the pipeline
# ===============================================

pipeline = Pipeline(extractor, strategy)

# ===============================================
# Anonymize the documents
# ===============================================

input_folder = "path/to/input/folder"
output_folder = "path/to/output/folder"
file_mapping = pipeline.anonymize(input_folder, output_folder, flatten=True)

```
