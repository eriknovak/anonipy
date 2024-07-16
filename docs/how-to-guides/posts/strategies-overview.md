---
date: 2024-07-15
authors: [eriknovak]
description: >
  The overview of the implemented strategies.
categories:
  - Overview
---

# Strategies overview

In this post, we will show an overview of the implemented  strategies. The strategies delegate how the original text will be anonymized given the extracted `named entities`. They output the anonymized text and the list of replacements that were made to the original text.

All strategies and their API references are available in the  [strategies][anonipy.anonymize.strategies] module. What follows is the presentation of the different strategies `anonipy` provides.

<!-- more -->




## Pre-requisites

Let us first define the text we want to anonymiyze.

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

Normally, the entities would be extracted using an [extractor][anonipy.anonymize.extractors]. For this example, we manually define the entities.

```python
from anonipy.definitions import Entity

entities = [
    Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
    ),
    Entity(
        text="15-01-1985",
        label="date of birth",
        start_index=54,
        end_index=64,
        type="date",
    ),
    Entity(
        text="20-05-2024",
        label="date",
        start_index=86,
        end_index=96,
        type="date",
    ),
    Entity(
        text="123-45-6789",
        label="social security number",
        start_index=121,
        end_index=132,
        type="custom",
        regex="[0-9]{3}-[0-9]{2}-[0-9]{4}",
    ),
    Entity(
        text="John Doe",
        label="name",
        start_index=157,
        end_index=165,
        type="string",
    ),
    Entity(
        text="15-11-2024",
        label="date",
        start_index=717,
        end_index=727,
        type="date",
    ),
]
```


## Strategies

All following strategies are available in the [strategies][anonipy.anonymize.strategies] module.


### Redacted Strategy

Data redaction is the process of obscuring information that’s personally identifiable, confidential, classified or sensitive.

The [RedactionStrategy][anonipy.anonymize.strategies.RedactionStrategy] anonymizes the original text by replacing the entities in the text with a predefined substitute label, which defaults to `[REDACTED]`.

!!! info "Anonymization details"
    The redaction strategy hides sensitive information by replacing the original entities with a string that does not reveal any information about the original. While this is useful for obscuring information, it does change the text's distribution, which can effect the training of machine learning models.

```python
from anonipy.anonymize.strategies import RedactionStrategy
```


The `RedactionStrategy` requires the following input parameters at initialization:

::: anonipy.anonymize.strategies.RedactionStrategy.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Let us now initialize the redaction strategy.

```python
redaction_strategy = RedactionStrategy()
```

To use the strategy, we can call the `anonymize` method to anonymize the text given the `entities`. The `anonymize` method receives the following parameters:

::: anonipy.anonymize.strategies.RedactionStrategy.anonymize
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Using the `RedactionStrategy`, we can now anonymize the text.

```python
anonymized_text, replacements = redaction_strategy.anonymize(
    original_text,
    entities
)
```

Which returns the anonymized text and the list of replacements made.

```python
print(anonymized_text)
```
```text
Medical Record

Patient Name: [REDACTED]
Date of Birth: [REDACTED]
Date of Examination: [REDACTED]
Social Security Number: [REDACTED]

Examination Procedure:
[REDACTED] underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.

Medication Prescribed:

Ibuprofen 200 mg: Take one tablet every 6-8 hours as needed for headache and pain relief.
Lisinopril 10 mg: Take one tablet daily to manage high blood pressure.
Next Examination Date:
[REDACTED]
```

And the associated replacements are:

```python
print(replacements)
```
```json
[
    {
        "original_text": "John Doe",
        "label": "name",
        "start_index": 30,
        "end_index": 38,
        "anonymized_text": "[REDACTED]"
    },
    {
        "original_text": "15-01-1985",
        "label": "date of birth",
        "start_index": 54,
        "end_index": 64,
        "anonymized_text": "[REDACTED]"
    },
    {
        "original_text": "20-05-2024",
        "label": "date",
        "start_index": 86,
        "end_index": 96,
        "anonymized_text": "[REDACTED]"
    },
    {
        "original_text": "123-45-6789",
        "label": "social security number",
        "start_index": 121,
        "end_index": 132,
        "anonymized_text": "[REDACTED]"
    },
    {
        "original_text": "John Doe",
        "label": "name",
        "start_index": 157,
        "end_index": 165,
        "anonymized_text": "[REDACTED]"
    },
    {
        "original_text": "15-11-2024",
        "label": "date",
        "start_index": 717,
        "end_index": 727,
        "anonymized_text": "[REDACTED]"
    }
]
```




### Masking Strategy

Data masking refers to the disclosure of data with modified values. Data anonymization is done by creating a mirror image of a database and implementing alteration strategies, such as character shuffling, encryption, term, or character substitution. For example, a value character may be replaced by a symbol such as “*” or “x.” It makes identification or reverse engineering difficult.

The [MaskingStrategy][anonipy.anonymize.strategies.MaskingStrategy] anonymizes the original text by replacing the entities with masks, which are created using the subsitute label, which defaults to `*`.

!!! info "Anonymization details"
    The masking strategy is useful as it hides the original sensitive values and retains the original text's length. However, it also changes the original text's meaning and distribution, as the replacement values are not the same as the original values.

```python
from anonipy.anonymize.strategies import MaskingStrategy
```


The `MaskingStrategy` requires the following input parameters at initialization:

::: anonipy.anonymize.strategies.MaskingStrategy.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Let us now initialize the masking strategy.

```python
masking_strategy = MaskingStrategy()
```

To use the strategy, we can call the `anonymize` method to anonymize the text given the `entities`. The `anonymize` method receives the following parameters:

::: anonipy.anonymize.strategies.MaskingStrategy.anonymize
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Using the `MaskingStrategy`, we can now anonymize the text.

```python
anonymized_text, replacements = masking_strategy.anonymize(
    original_text,
    entities
)
```

Which returns the anonymized text and the list of replacements made.

```python
print(anonymized_text)
```
```text
Patient Name: **** ***
Date of Birth: **********
Date of Examination: **********
Social Security Number: ***********

Examination Procedure:
**** *** underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.

Medication Prescribed:

Ibuprofen 200 mg: Take one tablet every 6-8 hours as needed for headache and pain relief.
Lisinopril 10 mg: Take one tablet daily to manage high blood pressure.
Next Examination Date:
**********
```

And the associated replacements are:

```python
print(replacements)
```
```json
[
    {
        "original_text": "John Doe",
        "label": "name",
        "start_index": 30,
        "end_index": 38,
        "anonymized_text": "**** ***"
    },
    {
        "original_text": "15-01-1985",
        "label": "date of birth",
        "start_index": 54,
        "end_index": 64,
        "anonymized_text": "**********"
    },
    {
        "original_text": "20-05-2024",
        "label": "date",
        "start_index": 86,
        "end_index": 96,
        "anonymized_text": "**********"
    },
    {
        "original_text": "123-45-6789",
        "label": "social security number",
        "start_index": 121,
        "end_index": 132,
        "anonymized_text": "***********"
    },
    {
        "original_text": "John Doe",
        "label": "name",
        "start_index": 157,
        "end_index": 165,
        "anonymized_text": "**** ***"
    },
    {
        "original_text": "15-11-2024",
        "label": "date",
        "start_index": 717,
        "end_index": 727,
        "anonymized_text": "**********"
    }
]
```




### Pseudonymization Strategy

Pseudonymization is a data de-identification tool that substitutes private identifiers with false identifiers or pseudonyms, such as swapping the “John Smith” identifier with the “Mark Spencer” identifier. It maintains statistical precision and data confidentiality, allowing changed data to be used for creation, training, testing, and analysis, while at the same time maintaining data privacy.

The [PseudonymizationStrategy][anonipy.anonymize.strategies.PseudonymizationStrategy] anonymizes the original text by replacing the entities with fake ones, which are created using the generators (see [generators][anonipy.anonymize.generators]).

!!! info "Anonymization details"
    The pseudonymization strategy is the most useful in terms of retaining the statistical distributions of the text. However, it is also most technical, as the user must define a function for mapping true entities to fake ones. Furthermore, if an entity appears multiple times the pseudonymization strategy will retain the same mapping between the true and fake entities.


The `PseudonymizationStrategy` requires a function for mapping entities. In our example, we will define a function using the generators. To make the example accessible as possible, we will use the [MaskLabelGenerator][anonipy.anonymize.generators.MaskLabelGenerator] instead of the [LLMLabelGenerator][anonipy.anonymize.generators.LLMLabelGenerator] for generating string entities.

First, let us define the mapping function. We will import the required generators and initialize them.

```python
from anonipy.anonymize.generators import (
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)

# initialize the generators
mask_generator = MaskLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()
```

Next, we will define the anonymization mapping function. This function receives two inputs: `text` and the `entity`. The `text` is the original text, and the `entity` is the current entity. The anonymization mapping will create a replacement for the given `entity` based on it's information and context within the `text`.

```python
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
```


Let us now initialize the pseudonymization strategy.

```python
from anonipy.anonymize.strategies import PseudonymizationStrategy
```


The `PseudonymizationStrategy` requires the following input parameters at initialization:

::: anonipy.anonymize.strategies.PseudonymizationStrategy.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Let us now initialize the pseudonymization strategy.

```python
pseudo_strategy = PseudonymizationStrategy(
    mapping=anonymization_mapping
)
```

To use the strategy, we can call the `anonymize` method to anonymize the text given the `entities`. The `anonymize` method receives the following parameters:

::: anonipy.anonymize.strategies.PseudonymizationStrategy.anonymize
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Using the `PseudonymizationStrategy`, we can now anonymize the text.

```python
anonymized_text, replacements = pseudo_strategy.anonymize(
    original_text,
    entities
)
```

Which returns the anonymized text and the list of replacements made.

!!! note "Generator performance"
    While `MaskLabelGenerator` is faster and less resource intensive than `LLMLabelGenerator`, it sometimes does not provide a meaningful replacement. In the example below, the patient name `John Doe` is replaced with `first Professor`, which is not meaningful. Therefore, when possible, we advise using the `LLMLabelGenerator` instead.

```python
print(anonymized_text)
```
```text
Medical Record

Patient Name: first Professor
Date of Birth: 01-07-1985
Date of Examination: 15-05-2024
Social Security Number: 724-78-8182

Examination Procedure:
first Professor underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.

Medication Prescribed:

Ibuprofen 200 mg: Take one tablet every 6-8 hours as needed for headache and pain relief.
Lisinopril 10 mg: Take one tablet daily to manage high blood pressure.
Next Examination Date:
15-11-2024
```

And the associated replacements are:

```python
print(replacements)
```
```json
[
    {
        "original_text": "John Doe",
        "label": "name",
        "start_index": 30,
        "end_index": 38,
        "anonymized_text": "first Professor"
    },
    {
        "original_text": "15-01-1985",
        "label": "date of birth",
        "start_index": 54,
        "end_index": 64,
        "anonymized_text": "01-07-1985"
    },
    {
        "original_text": "20-05-2024",
        "label": "date",
        "start_index": 86,
        "end_index": 96,
        "anonymized_text": "15-05-2024"
    },
    {
        "original_text": "123-45-6789",
        "label": "social security number",
        "start_index": 121,
        "end_index": 132,
        "anonymized_text": "724-78-8182"
    },
    {
        "original_text": "John Doe",
        "label": "name",
        "start_index": 157,
        "end_index": 165,
        "anonymized_text": "first Professor"
    },
    {
        "original_text": "15-11-2024",
        "label": "date",
        "start_index": 717,
        "end_index": 727,
        "anonymized_text": "15-11-2024"
    }
]
```



## Conclusion

The strategies are used to anonymize the text in combination with the extracted `named entities`. The strategies are used to replace and anonymize the text as well as provide the list of replacements that were made to the original text.
