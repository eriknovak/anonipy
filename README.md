
<p align="center">
  <img src="https://raw.githubusercontent.com/eriknovak/anonipy/main/docs/assets/imgs/logo.png" alt="logo" height="100" style="height: 100px;">
</p>

<p align="center">
  <i>Data anonymization package, supporting different anonymization strategies</i>
</p>

<p align="center">
  <a href="https://github.com/eriknovak/anonipy/actions/workflows/unittests.yaml" target="_blank">
    <img src="https://github.com/eriknovak/anonipy/actions/workflows/unittests.yaml/badge.svg" alt="Test" />
  </a>
  <a href="https://pypi.org/project/anonipy" target="_blank">
    <img src="https://img.shields.io/pypi/v/anonipy?color=%2334D058&amp;label=pypi%20package" alt="Package version" />
  </a>
  <a href="https://pypi.org/project/anonipy" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/anonipy.svg?color=%2334D058" alt="Supported Python versions" />
  </a>
</p>


---

**Documentation:** [https://eriknovak.github.io/anonipy](https://eriknovak.github.io/anonipy)

**Source code:** [https://github.com/eriknovak/anonipy](https://github.com/eriknovak/anonipy)

---

The anonipy package is a python package for data anonymization. It is designed to be simple to use and highly customizable, supporting different anonymization strategies. Powered by LLMs.

## ✅ Requirements
Before starting the project make sure these requirements are available:

- [python]. The python programming language (v3.8 or higher).

## 💾 Install

```bash
pip install anonipy
```

## 🔎 Example

The details of the example can be found in the [Overview](https://eriknovak.github.io/anonipy/documentation/notebooks/00-overview.ipynb).

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

Use the language detector to detect the language of the text:

```python
from anonipy.utils.language_detector import LanguageDetector

lang_detector = LanguageDetector()
language = lang_detector(original_text)
```

Prepare the entity extractor and extract the personal infomation from the original text:

```python
from anonipy.anonymize.extractors import EntityExtractor

# define the labels to be extracted and anonymized
labels = [
    {"label": "name", "type": "string"},
    {"label": "social security number", "type": "custom"},
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]

# language taken from the language detector
entity_extractor = EntityExtractor(labels, lang=language, score_th=0.5)

# extract the entities from the original text
doc, entities = entity_extractor(original_text)

# display the entities in the original text
entity_extractor.display(doc)
```

Use generators to create substitutes for the entities:

```python
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    DateGenerator,
    NumberGenerator,
)

# initialize the generators
llm_generator = LLMLabelGenerator()
date_generator = DateGenerator()
number_generator = NumberGenerator()

# prepare the anonymization mapping
def anonymization_mapping(text, entity):
    if entity.type == "string":
        return llm_generator.generate(entity, temperature=0.7)
    if entity.label == "date":
        return date_generator.generate(entity, output_gen="middle_of_the_month")
    if entity.label == "date of birth":
        return date_generator.generate(entity, output_gen="middle_of_the_year")
    if entity.label == "social security number":
        return number_generator.generate(entity)
    return "[REDACTED]"
```

Anonymize the text using the anonymization mapping:

```python
from anonipy.anonymize.strategies import PseudonymizationStrategy

# initialize the pseudonymization strategy
pseudo_strategy = PseudonymizationStrategy(mapping=anonymization_mapping)

# anonymize the original text
anonymized_text, replacements = pseudo_strategy.anonymize(original_text, entities)
```


[python]: https://www.python.org/