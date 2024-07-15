---
draft: true
date: 2024-07-15
authors: [eriknovak]
description: >
  The overview of the implemented generators.
categories:
  - Overview
---

# Generators Overview

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




### MaskLabelGenerator




### NumberGenerator




### DateGenerator




## Conclusion

The generators are used to create new texts that would serve as substitutes to the extracted `named entities`. The substitutes can be then used to replace and anonymize the text.


!!! info "Under construction"