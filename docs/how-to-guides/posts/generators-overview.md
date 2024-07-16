---
date: 2024-07-15
authors: [eriknovak]
description: >
  The overview of the implemented generators.
categories:
  - Overview
---

# Generators overview

In this post, we will show an overview of the implemented  generators. The generators are used to create new texts that would serve as substitutes to the extracted `named entities`. The substitutes can be then used to replace and anonymize the text.

All generators and their API references are available in the  [generators][anonipy.anonymize.generators] module. What follows is the presentation of the different generators `anonipy` provides.

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
        regex="\d{3}-\d{2}-\d{4}",
    ),
]
```



## Generators

All following generators are available in the [generators][anonipy.anonymize.generators] module.




### LLMLabelGenerator

The [LLMLabelGenerator][anonipy.anonymize.generators.LLMLabelGenerator] is a one-stop-shop generator that utilizes LLMs to generate replacements for entities. It is implemented to support any entity type.

!!! info "GPU Requirements"
    The `LLMLabelGenerator` utilizes the open source LLMs,     specifically the [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) model. Because the model is quite large, we utilize quantization using the `bitsandbytes` package to reduce its size. Therefore, the `LLMLabelGenerator` requires at least 8GB GPU and CUDA drivers to be available. If these resources are not available on your machine, consider using the `MaskLabelGenerator` instead.

```python
from anonipy.anonymize.generators import LLMLabelGenerator
```

The `LLMLabelGenerator` currently does not require any input parameters at initialization.

Let us now initialize the LLM label generator.

```python
llm_generator = LLMLabelGenerator()
```

!!! info "Initialization warnings"
    The initialization of `LLMLabelGenerator` will throw some warnings. Ignore them. These are expected due to the use of package dependencies.

To use the generator, we can call the `generate` method. The `generate` method receives the following parameters:

::: anonipy.anonymize.generators.LLMLabelGenerator.generate
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Let us generate the replacement for the first entity from `entities` using the default parameters.

```python
llm_generator.generate(entities[0])# (1)!
```

1. The generator receives the `John Doe` name entity and might return the replacement: `Ethan Thomson`


Let us now change the label prefix and generate the replacement using a higher temperature.

```python
llm_generator.generate(
    entities[0],
    entity_prefix="Spanish",
    temperature=0.7
)# (1)!
```

1. The generator receives the `John Doe` name entity and under the different generation parameters might return the replacement: `Juan Rodrigez`

Going through the whole `entities` list, the `LLMLabelGenerator`, using the default parameters, might generate the following replacements:

| Entity        | Type     | Label                    | Replacement     |
| ------------- | -------- | ------------------------ | --------------- |
| `John Doe`    | `string` | `name`                   | `Ethan Thomson` |
| `20-05-2024`  | `date`   | `date`                   | `23-07-2027`    |
| `123-45-6789` | `custom` | `social security number` | `987-65-4321`   |


**Advices and suggestions**

**Using LLMLabelGenerator only for string and custom types.**
While the `LLMLabelGenerator` is able to generate alternatives for different entity types, we suggest using it only for string and custom entity types. The reason is that the LLMs can be quite slow for generating replacements.

In addition, `anonipy` has other generators that can be used for other entity types, such as dates, numbers, etc.

**Restricting with regex.**
Using LLMs to generate text is best when the generation is restricted to a specific pattern. The [Entity][anonipy.definitions.Entity] object already contains a `regex` field that can be used to restrict the generation
to a specific pattern. However, it is recommended to specify to have as specific and restrictive regex expressions as possible.

This will help the `LLMLabelGenerator` to generate more accurate replacements.




### MaskLabelGenerator

The [MaskLabelGenerator][anonipy.anonymize.generators.MaskLabelGenerator] is a generator that uses smaller language models, such as [XLM-RoBERTa](https://huggingface.co/FacebookAI/xlm-roberta-large), to generate replacements for entities. It is implemented to support any entity type, but we suggest using it only with string entities. For other entity types, please use other available [generators][anonipy.anonymize.generators].

```python
from anonipy.anonymize.generators import MaskLabelGenerator
```

The `MaskLabelGenerator` requires the following input parameters at initialization:

::: anonipy.anonymize.generators.MaskLabelGenerator.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Let us now initialize the mask label generator.

```python
mask_generator = MaskLabelGenerator()
```

!!! info "Initialization warnings"
    The initialization of `LLMLabelGenerator` will throw some warnings. Ignore them. These are expected due to the use of package dependencies.

To use the generator, we can call the `generate` method. The `generate` method receives the following parameters:

::: anonipy.anonymize.generators.MaskLabelGenerator.generate
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

This generator will create a list of suggestions from which it will select one at random. Therefore, the generator will return different suggestions every time it is called.

```python
mask_generator.generate(entities[0], text=original_text)# (1)!
mask_generator.generate(entities[0], text=original_text)# (2)!
mask_generator.generate(entities[0], text=original_text)# (3)!
```

1. The first generation for the `John Doe` name entity might return the replacement: `James Smith`
2. The second generation might return the replacement: `Michael Smith`
3. The third generation might return the replacement: `David Blane`

**Advices and suggestions**

**Using only for string entities.**
As seen from the above examples, the `MaskLabelGenerator` is best used with string entities. For number and date entities, it is best to use other generators, such as `NumberGenerator` and `DateGenerator`.




### NumberGenerator

The [NumberGenerator][anonipy.anonymize.generators.NumberGenerator] is a generator for generating random numbers. It is implemented to support integers, floats, and phone numbers, but it can be used to generate values for custom types which include numbers.

```python
from anonipy.anonymize.generators import NumberGenerator
```

The `NumberGenerator` currently does not require any input parameters at initialization.

```python
number_generator = NumberGenerator()
```

To use the generator, we can call the `generate` method. The `generate` method receives the following parameters:

::: anonipy.anonymize.generators.NumberGenerator.generate
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

This generator will create a suggestion by replacing numeric values in the entity text at random. Therefore, the generator will return different suggestions every time it is called.

```python
number_generator.generate(entities[2])# (1)!
```

1. For the `social security number` entity, the generator will return a replacement, such as: `143-46-4915`.

Furthermore, it will throw an error if the entity type is not `integer`, `float`, `phone_number` or `custom`.

```python
try:
    number_generator.generate(entities[0])# (1)!
except Exception as e:
    print(e)# (2)!
```

1. The provided entity is a `string`, therefore it will raise an error.
2. The exception will state `The entity type must be 'integer', 'float', 'phone_number' or 'custom' to generate numbers.`




### DateGenerator

The [DateGenerator][anonipy.anonymize.generators.DateGenerator] is a generator for generating dates. It is implemented to support date entities.

```python
from anonipy.anonymize.generators import DateGenerator
```

The `DateGenerator` requires the following input parameters at initialization:

::: anonipy.anonymize.generators.DateGenerator.__init__
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_source: False

Let us now initialize the date generator.

```python
date_generator = DateGenerator()
```

To use the generator, we can call the `generate` method. The `generate` method receives the following parameters:

::: anonipy.anonymize.generators.DateGenerator.generate
    options:
      show_root_heading: False
      show_docstring_description: False
      show_docstring_examples: False
      show_docstring_returns: False
      show_docstring_raises: False
      show_source: False

Using the above parameters, this generator will create the appropriate date suggestions:

```python

entities[1]# (1)!
date_generator.generate(entities[1], sub_variant="RANDOM")# (2)!
date_generator.generate(entities[1], sub_variant="FIRST_DAY_OF_THE_MONTH")# (3)!
date_generator.generate(entities[1], sub_variant="LAST_DAY_OF_THE_MONTH")# (4)!
date_generator.generate(entities[1], sub_variant="MIDDLE_OF_THE_MONTH")# (5)!
date_generator.generate(entities[1], sub_variant="MIDDLE_OF_THE_YEAR")# (6)!
```

1. The entity is a `date` entity with the text `20-05-2024`.
2. The `RANDOM` sub variant will return a random date within the given date range. A possible generation can be: `26-05-2024`
3. The `FIRST_DAY_OF_THE_MONTH` sub variant will return the first day of the month: `01-05-2024`
4. The `LAST_DAY_OF_THE_MONTH` sub variant will return the last day of the month: `31-05-2024`
5. The `MIDDLE_OF_THE_MONTH` sub variant will return the middle day of the month: `15-05-2024`
6. The `MIDDLE_OF_THE_YEAR` sub variant will return the middle day of the year: `01-07-2024`


Furthermore, it will throw an error if the entity type is not `date`.

```python
try:
    date_generator.generate(entities[0])# (1)!
except Exception as e:
    print(e)# (2)!
```

1. The provided entity is a `string`, therefore it will raise an error.
2. The exception will state `The entity type must be 'date' to generate dates.`




## Conclusion

The generators are used to create new texts that would serve as substitutes to the extracted `named entities`. The substitutes can be then used to replace and anonymize the text.
