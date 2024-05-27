import unittest

from anonipy.definitions import Entity
from anonipy.anonymize.extractors import EntityExtractor
from anonipy.constants import LANGUAGES

# =====================================
# Helper functions
# =====================================

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

original_entities = [
    Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
        regex=".*",
    ),
    Entity(
        text="15-01-1985",
        label="date of birth",
        start_index=54,
        end_index=64,
        type="date",
        regex="(\\d{1,2}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{2,4})|(\\d{2,4}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{1,2})",
    ),
    Entity(
        text="20-05-2024",
        label="date",
        start_index=86,
        end_index=96,
        type="date",
        regex="(\\d{1,2}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{2,4})|(\\d{2,4}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{1,2})",
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
        regex=".*",
    ),
    Entity(
        text="15-11-2024",
        label="date",
        start_index=717,
        end_index=727,
        type="date",
        regex="(\\d{1,2}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{2,4})|(\\d{2,4}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{1,2})",
    ),
]

# define the labels to be extracted and anonymized
labels = [
    {"label": "name", "type": "string"},
    {
        "label": "social security number",
        "type": "custom",
        "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}",
    },
    {"label": "date of birth", "type": "date"},
    {"label": "date", "type": "date"},
]


# =====================================
# Test Entity Extractor
# =====================================


class TestEntityExtractor(unittest.TestCase):
    def test_init(self):
        try:
            EntityExtractor()
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_init_inputs(self):
        extractor = EntityExtractor(labels=labels, lang=LANGUAGES.ENGLISH, score_th=0.5)
        self.assertEqual(extractor.__class__, EntityExtractor)

    def test_methods(self):
        extractor = EntityExtractor(labels=labels, lang=LANGUAGES.ENGLISH, score_th=0.5)
        self.assertEqual(hasattr(extractor, "__call__"), True)
        self.assertEqual(hasattr(extractor, "display"), True)

    def test_extract_default(self):
        extractor = EntityExtractor(labels=labels, lang=LANGUAGES.ENGLISH, score_th=0.5)
        doc, entities = extractor(original_text)
        self.assertEqual(entities, original_entities)


if __name__ == "__main__":
    unittest.main()
