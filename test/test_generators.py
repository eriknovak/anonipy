import re
import unittest
import warnings

import torch

from anonipy.definitions import Entity
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)
from anonipy.anonymize.regex import regex_map

# =====================================
# Test Cases
# =====================================

DATETIME_STRS = [
    "2023-06-17 14:30:00",
    "17-06-2023 14:30:00",
    "06-17-2023 14:30:00",
    "2023/06/17 14:30:00",
    "17/06/2023 14:30:00",
    "06/17/2023 14:30:00",
    "2023.06.17 14:30:00",
    "17.06.2023 14:30:00",
    "06.17.2023 14:30:00",
    "2023 06 17 14:30:00",
    "17 06 2023 14:30:00",
    "06 17 2023 14:30:00",
    "2023-06-17 14:30",
    "17-06-2023 14:30",
    "06-17-2023 14:30",
    "2023/06/17 14:30",
    "17/06/2023 14:30",
    "06/17/2023 14:30",
    "2023.06.17 14:30",
    "17.06.2023 14:30",
    "06.17.2023 14:30",
    "2023 06 17 14:30",
    "17 06 2023 14:30",
    "06 17 2023 14:30",
    "2023-06-17 02:30 PM",
    "17-06-2023 02:30 PM",
    "06-17-2023 02:30 PM",
    "2023/06/17 02:30 PM",
    "17/06/2023 02:30 PM",
    "06/17/2023 02:30 PM",
    "2023.06.17 02:30 PM",
    "17.06.2023 02:30 PM",
    "06.17.2023 02:30 PM",
    "2023 06 17 02:30 PM",
    "17 06 2023 02:30 PM",
    "06 17 2023 02:30 PM",
    "June 17, 2023 14:30:00",
    "17 June 2023 14:30:00",
    "Jun 17, 2023 14:30:00",
    "17 Jun 2023 14:30:00",
    "June 17, 2023 02:30 PM",
    "17 June 2023 02:30 PM",
    "Jun 17, 2023 02:30 PM",
    "17 Jun 2023 02:30 PM",
    "Saturday, 17 June 2023 14:30:00",
    "Saturday, June 17, 2023 14:30:00",
    "Saturday, 17 June 2023 02:30 PM",
    "Saturday, June 17, 2023 02:30 PM",
    "2023-06-17",
    "17-06-2023",
    "06-17-2023",
    "2023/06/17",
    "17/06/2023",
    "06/17/2023",
    "2023.06.17",
    "17.06.2023",
    "06.17.2023",
    "2023 06 17",
    "17 06 2023",
    "06 17 2023",
    "June 17, 2023",
    "17 June 2023",
    "Jun 17, 2023",
    "17 Jun 2023",
    "Saturday, 17 June 2023",
    "Saturday, June 17, 2023",
]

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
        score=1.0,
        type="string",
        regex=regex_map("string"),
    ),
    "date": [
        Entity(
            text="20-05-2024",
            label="date",
            start_index=86,
            end_index=96,
            score=1.0,
            type="date",
            regex=regex_map("date"),
        )
    ]
    + [
        Entity(
            text=str,
            label="date",
            start_index=86,
            end_index=86 + len(str),
            score=1.0,
            type="date",
            regex=regex_map("date"),
        )
        for str in DATETIME_STRS
    ],
    "integer": Entity(
        text="123456789",
        label="integer",
        start_index=121,
        end_index=132,
        score=1.0,
        type="integer",
        regex=regex_map("integer"),
    ),
    "float": Entity(
        text="123,456,789.000",
        label="float",
        start_index=121,
        end_index=132,
        score=1.0,
        type="float",
        regex=regex_map("float"),
    ),
    "custom": Entity(
        text="123-45-6789",
        label="custom",
        start_index=121,
        end_index=132,
        score=1.0,
        type="custom",
        regex="\\d{3}-\\d{2}-\\d{4}",
    ),
}


# =====================================
# Test LLM Label Generator
# =====================================

if torch.cuda.is_available():
    # ! THESE TESTS REQUIRE GPU/CUDA! THIS WILL FAIL IF YOU DON'T HAVE GPU/CUDA!

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

    def setUp(self):
        warnings.filterwarnings("ignore", category=ImportWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)

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
        entity = test_entities["date"][0]
        generated_text = self.generator.generate(entity)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def test_generate_custom_date_format(self):
        entity = test_entities["date"][0]
        generator = DateGenerator(date_format="%d-%m-%Y")
        generated_text = generator.generate(entity)
        match = re.match(entity.regex, generated_text)
        self.assertNotEqual(match, None)
        self.assertEqual(match.group(0), generated_text)

    def text_generate_uncorrect_date_format(self):
        entity = test_entities["date"][0]
        generator = DateGenerator(date_format="%Y-%m-%d")
        try:
            generator.generate(entity)
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_generate_first_day_of_the_month(self):
        entity = test_entities["date"][0]
        generated_text = self.generator.generate(
            entity, output_gen="first_day_of_the_month"
        )
        self.assertEqual(generated_text, "01-05-2024")

    def test_generate_last_day_of_the_month(self):
        entity = test_entities["date"][0]
        generated_text = self.generator.generate(
            entity, output_gen="last_day_of_the_month"
        )
        self.assertEqual(generated_text, "31-05-2024")

    def test_generate_middle_of_the_month(self):
        entity = test_entities["date"][0]
        generated_text = self.generator.generate(
            entity, output_gen="middle_of_the_month"
        )
        self.assertEqual(generated_text, "15-05-2024")

    def test_generate_middle_of_the_year(self):
        entity = test_entities["date"][0]
        generated_text = self.generator.generate(
            entity, output_gen="middle_of_the_year"
        )
        self.assertEqual(generated_text, "01-07-2024")

    def test_generate_random(self):
        entity = test_entities["date"][0]
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

    def test_process_different_formats(self):
        for entity in test_entities["date"]:
            try:
                self.generator.generate(entity, output_gen="random")
            except ValueError:
                self.fail(
                    f"self.generator.generate() raised ValueError unexpectedly for date: {entity.text}"
                )


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
