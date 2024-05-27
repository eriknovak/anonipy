import re
import unittest

import torch

from anonipy.definitions import Entity
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)

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

test_entities = {
    "name": Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
        regex=".*",
    ),
    "date": Entity(
        text="20-05-2024",
        label="date",
        start_index=86,
        end_index=96,
        type="date",
        regex="(\\d{1,2}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{2,4})|(\\d{2,4}[\\/\\-\\.]\\d{1,2}[\\/\\-\\.]\\d{1,2})",
    ),
    "integer": Entity(
        text="123456789",
        label="integer",
        start_index=121,
        end_index=132,
        type="integer",
        regex="\d+",
    ),
    "float": Entity(
        text="123,456,789.000",
        label="float",
        start_index=121,
        end_index=132,
        type="float",
        regex="[\d\.,]+",
    ),
    "custom": Entity(
        text="123-45-6789",
        label="custom",
        start_index=121,
        end_index=132,
        type="custom",
        regex="\\d{3}-\\d{2}-\\d{4}",
    ),
}


# =====================================
# Test LLM Label Generator
# =====================================

if torch.cuda.is_available():
    # ! THESE TESTS REQUIRE GPU/CUDA !
    # ! THIS WILL FAIL IF YOU DON'T HAVE GPU/CUDA !

    class TestLLMLabelGenerator(unittest.TestCase):

        @classmethod
        def setUpClass(self):
            self.generator = LLMLabelGenerator()

        def test_has_methods(self):
            self.assertEqual(hasattr(self.generator, "generate"), True)

        def test_generate_default(self):
            entity = test_entities["name"]
            generated_text = self.generator.generate(entity)
            match = re.match(entity.regex, generated_text)
            self.assertNotEqual(match, None)
            self.assertEqual(match.group(0), generated_text)

        def test_generate_custom(self):
            entity = test_entities["name"]
            generated_text = self.generator.generate(
                entity, entity_prefix="Spanish", temperature=0.5
            )
            match = re.match(entity.regex, generated_text)
            self.assertNotEqual(match, None)
            self.assertEqual(match.group(0), generated_text)


# =====================================
# Test Mask Label Generator
# =====================================


class TestMaskLabelGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.generator = MaskLabelGenerator()

    def test_has_methods(self):
        self.assertEqual(hasattr(self.generator, "generate"), True)

    def test_generate_default(self):
        entity = test_entities["name"]
        generated_text = self.generator.generate(entity, text=original_text)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)


# =====================================
# Test Date Generator
# =====================================


class TestDateGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.generator = DateGenerator()

    def test_has_methods(self):
        self.assertEqual(hasattr(self.generator, "generate"), True)

    def test_generate_default(self):
        entity = test_entities["date"]
        generated_text = self.generator.generate(entity)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def test_generate_first_day_of_the_month(self):
        entity = test_entities["date"]
        generated_text = self.generator.generate(
            entity, output_gen="first_day_of_the_month"
        )
        self.assertEqual(generated_text, "01-05-2024")

    def test_generate_last_day_of_the_month(self):
        entity = test_entities["date"]
        generated_text = self.generator.generate(
            entity, output_gen="last_day_of_the_month"
        )
        self.assertEqual(generated_text, "31-05-2024")

    def test_generate_middle_of_the_month(self):
        entity = test_entities["date"]
        generated_text = self.generator.generate(
            entity, output_gen="middle_of_the_month"
        )
        self.assertEqual(generated_text, "15-05-2024")

    def test_generate_middle_of_the_year(self):
        entity = test_entities["date"]
        generated_text = self.generator.generate(
            entity, output_gen="middle_of_the_year"
        )
        self.assertEqual(generated_text, "01-07-2024")

    def test_generate_random(self):
        entity = test_entities["date"]
        generated_text = self.generator.generate(entity, output_gen="random")
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def test_generate_uncorrect_type(self):
        entity = test_entities["name"]
        try:
            self.generator.generate(entity)
        except Exception as e:
            self.assertEqual(type(e), ValueError)


# =====================================
# Test Number Generator
# =====================================


class TestNumberGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.generator = NumberGenerator()

    def test_has_methods(self):
        self.assertEqual(hasattr(self.generator, "generate"), True)

    def test_generate_integer(self):
        entity = test_entities["integer"]
        generated_text = self.generator.generate(entity)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def test_generate_float(self):
        entity = test_entities["float"]
        generated_text = self.generator.generate(entity)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def test_generate_custom(self):
        entity = test_entities["custom"]
        generated_text = self.generator.generate(entity)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def test_generate_uncorrect_type(self):
        entity = test_entities["name"]
        try:
            self.generator.generate(entity)
        except Exception as e:
            self.assertEqual(type(e), ValueError)


if __name__ == "__main__":
    unittest.main()
