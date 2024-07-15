---
date: 2024-07-15
authors: [eriknovak]
description: >
  The overview of the implemented extractors.
categories:
  - Overview
---

# Extractors Overview

In this post, we will show an overview of the implemented extractors. The extractors are used to extract relevant `named entities` from text. These entities can be people names, organizations, addresses, social security numbers, etc. The entities are then used to anonymize the text.

All extractors and their API references are available in the  [extractors][anonipy.anonymize.extractors] module. What follows is the presentation of the different extractors `anonipy` provides.

<!-- more -->

## Pre-requisites

Let us first define the text, from which we want to extract the entities.

```python
original_text = """\
Medical Record

Patient Name: John Doe
Date of Birth: 15-01-1985
Date of Examination: 20-05-2024
Social Security Number: 123-45-6789

Examination Procedure:
John Doe underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.

Medication Prescribed:

Ibuprofen 200 mg: Take one tablet every 6-8 hours as needed for headache and pain relief.
Lisinopril 10 mg: Take one tablet daily to manage high blood pressure.
Next Examination Date:
15-11-2024
"""
```

## Language configuration

Each extractor requires a language to be configured. The language is used to determine how to process the text. If the language is not specified, the extractor will use the default language. The default language is `ENGLISH`.

To make it easier to switch languages, we can use the [LANGUAGES][anonipy.constants.LANGUAGES] constant.

```python
from anonipy.constants import LANGUAGES

LANGUAGE.ENGLISH# (1)!
```

1. The `LANGUAGE.ENGLISH` return the `("en", "English")` literal tuple, which is the format required by the extractors.

### Using the language detector

An alternative is to use a language detector available in the [language_detector][anonipy.utils.language_detector] module. The detector utilizes the [lingua](https://github.com/pemistahl/lingua-py) python package, and allows automatic detection of the language of the text.

```python
from anonipy.utils.language_detector import LanguageDetector

# initialize the language detector and detect the language
language_detector = LanguageDetector()
language_detector(original_text)# (1)!
```

1. The `language_detector` returns the literal tuple `("en", "English")`, similar to the `LANGUAGE.ENGLISH`, making it compatible with the extractors.

## Named Entity

Each extractor will extract the `named entities` from the text. The entities can be people names, organizations, addresses, social security numbers, etc. The entities are represented using the [Entity][anonipy.definitions.Entity] dataclass, which consists of the following parameters:

::: anonipy.definitions.Entity
    options:
      show_root_heading: False
      show_docstring_description: False
      show_source: False



## Extractors

All following extractors are available in the [extractors][anonipy.anonymize.extractors] module.

### Named entity recognition (NER) extractor

The [NERExtractor][anonipy.anonymize.extractors.NERExtractor] extractor uses a span-based NER model to identify the relevant entities in the text. Furthermore, it uses the [GLiNER](https://github.com/urchade/GLiNER) span-based NER model, specifically the model finetuned for recognizing Personal Identifiable Information (PII) within text. The model has been finetuned on six languages (English, French, German, Spanish, Italian, and Portuguese), but can be applied also to other languages.

```python
from anonipy.anonymize.extractors import NERExtractor
```

The `NERExtractor` takes the following input parameters:

::: anonipy.anonymize.extractors.NERExtractor.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_source: False

We must define the labels to be extracted and their types. In this example, we will extract the following entities:

```python
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom", "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]
```

Let us now initialize the entity extractor.

```python
ner_extractor = NERExtractor(labels, lang=LANGUAGES.ENGLISH, score_th=0.5)
```

!!! info "Initialization warnings"
    The initialization of `NERExtractor` will throw some warnings. Ignore them. These are expected due to the use of package dependencies.


The `NERExtractor` receives the text to be anonymized and returns the enriched text document and the extracted entities.

```python
doc, entities = ner_extractor(original_text)
```

The entities extracted within the input text are:

```python
ner_extractor.display(doc)
```

<div class="md-typeset admonition tip" style="line-height: 2.5; direction: ltr; padding: .6rem;">Medical Record<br><br>Patient Name:
    <mark class="entity"
        style="background: #308774; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        John Doe
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">name</span>
    </mark>
    <br>Date of Birth:
    <mark class="entity"
        style="background: #6706D7; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        15-01-1985
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">date
            of birth</span>
    </mark>
    <br>Date of Examination:
    <mark class="entity"
        style="background: #E805DA; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        20-05-2024
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">date</span>
    </mark>
    <br>Social Security Number:
    <mark class="entity"
        style="background: #32D102; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        123-45-6789
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">social
            security number</span>
    </mark>
    <br><br>Examination Procedure:<br>
    <mark class="entity"
        style="background: #308774; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        John Doe
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">name</span>
    </mark>
    underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart
    rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported
    occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any
    underlying issues.<br><br>Medication Prescribed:<br><br>Ibuprofen 200 mg: Take one tablet every 6-8 hours as
    needed for headache and pain relief.<br>Lisinopril 10 mg: Take one tablet daily to manage high blood
    pressure.<br>Next Examination Date:<br>
    <mark class="entity"
        style="background: #E805DA; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        15-11-2024
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">date</span>
    </mark>
</div>

**Advices and suggestions**

**Use specific label names.**
In the above example, we used specific label names to extract the entities. If we use a less specific name, the entity extractor might not find any relevant entity.

For instance, when using `social security number` as the label name, the entity extractor is able to extract the social security number from the text. However, if we use `ssn` or just `number` as the label name, the entity extractor might not find any relevant entity.

!!! tip
    Using more specific label names is better.


**Use custom regex patterns.**
In the `anonipy` package, we provide some predefined [ENTITY_TYPES][anonipy.constants.ENTITY_TYPES], which are:

::: anonipy.constants.ENTITY_TYPES
    options:
      show_root_heading: False
      show_docstring_description: False
      show_source: False

These entity types also have a corresponding regex pattern, as defined in the [regex][anonipy.utils.regex] submodule.


If the user wants to use a custom regex pattern, they can define it in the `labels`  variable list. Using a custom regex pattern allows the user to specify a more strict pattern that the entity must match.



### Pattern extractor


The [PatternExtractor][anonipy.anonymize.extractors.PatternExtractor] is an extractor that uses a custom spacy and regex pattern to extract entities. When documents have a consistent format and structure, the
pattern extractor can be useful, as it can extract entities in a consistent way.

```python
from anonipy.anonymize.extractors import PatternExtractor
```

The `PatternExtractor` takes the following parameters:

::: anonipy.anonymize.extractors.PatternExtractor.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_source: False

We must define the labels and their patterns used to extract the
relevant entities. The patterns are defined using [spacy patterns](https://spacy.io/usage/rule-based-matching/) or [regex patterns](https://docs.python.org/3/library/re.html).

In this example, we will use the following labels and patterns:

```python
labels = [
    # the pattern is defined using regex patterns, where the paranthesis are used to indicate core entity values
    {"label": "symptoms", "regex": r"\((.*)\)"},
    # the pattern is defined using spacy patterns
    {
        "label": "medicine",
        "pattern": [[{"IS_ALPHA": True}, {"LIKE_NUM": True}, {"LOWER": "mg"}]],
    },
    # the pattern is defined using spacy patterns
    {
        "label": "date",
        "pattern": [
            [
                {"SHAPE": "dd"},
                {"TEXT": "-"},
                {"SHAPE": "dd"},
                {"TEXT": "-"},
                {"SHAPE": "dddd"},
            ]
        ],
    },
]
```

Let us now initialize the pattern extractor.

```python
pattern_extractor = PatternExtractor(labels, lang=LANGUAGES.ENGLISH)
```

The `PatternExtractor` receives the original text and returns the enriched text document and the extracted entities.

```python
doc, entities = pattern_extractor(original_text)
```

The entities extracted within the input text are:

```python
pattern_extractor.display(doc)
```

<div class="md-typeset admonition tip" style="line-height: 2.5; direction: ltr; padding: .6rem;">Medical Record<br><br>Patient Name: John Doe<br>Date of
    Birth:
    <mark class="entity"
        style="background: #E805DA; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        15-01-1985
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">date</span>
    </mark>
    <br>Date of Examination:
    <mark class="entity"
        style="background: #E805DA; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        20-05-2024
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">date</span>
    </mark>
    <br>Social Security Number: 123-45-6789<br><br>Examination Procedure:<br>John Doe underwent a routine physical
    examination. The procedure included measuring vital signs (
    <mark class="entity"
        style="background: #846A32; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        blood pressure, heart rate, temperature
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">symptoms</span>
    </mark>
    ), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and
    dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.<br><br>Medication
    Prescribed:<br><br>
    <mark class="entity"
        style="background: #C3BB81; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        Ibuprofen 200 mg
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">medicine</span>
    </mark>
    : Take one tablet every 6-8 hours as needed for headache and pain relief.<br>
    <mark class="entity"
        style="background: #C3BB81; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        Lisinopril 10 mg
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">medicine</span>
    </mark>
    : Take one tablet daily to manage high blood pressure.<br>Next Examination Date:<br>
    <mark class="entity"
        style="background: #E805DA; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em;">
        15-11-2024
        <span
            style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-left: 0.5rem">date</span>
    </mark>
    <br>
</div>


### Multi extractor

The [MultiExtractor][anonipy.anonymize.extractors.MultiExtractor] is a extractor that can be used to extract entities using multiple extractors.

The motivation behind the multi extractor is the following: depending on the document format, personal information can be located in different locations; some of them can be found at similar places, while others can be found in different places and formats. Because of this, we would need to use the [NERExtractor][anonipy.anonymize.extractors.NERExtractor] to automatically identify the entities at different locations and the [PatternExtractor][anonipy.anonymize.extractors.PatternExtractor] to extract the entities that appear at the same location.

```python
from anonipy.anonymize.extractors import MultiExtractor
```

The `MultiExtractor` takes the following parameters:

::: anonipy.anonymize.extractors.MultiExtractor.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_source: False

In this example, we will use the previously initialized NER and pattern extractors.

```python
multi_extractor = MultiExtractor(
  extractors=[ner_extractor, pattern_extractor],
)
```

Similar as before, the `MultiExtractor` receives the original text, but returns the outputs of all the extractors, as well as the joint entities from all the extractors.

```python
extractor_outputs, joint_entities = multi_extractor(original_text)
```

## Conclusion

The extractors are used to extract entities from the text. The `anonipy` package supports both machine learning-based and pattern-based entity extraction, enabling information identification and extraction from different textual formats.