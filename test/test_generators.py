import re
import warnings

import pytest
from transformers import logging

from anonipy.definitions import Entity
from anonipy.anonymize.generators import (
    LLMLabelGenerator,
    MaskLabelGenerator,
    DateGenerator,
    NumberGenerator,
)

# disable transformers logging
logging.set_verbosity_error()

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


TEST_ORIGINAL_TEXT = """\
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

TEST_ENTITIES = {
    "name": Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
    ),
    "name:pattern": Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
        regex="Person: (.*)",
    ),
    "date": [
        Entity(
            text="20-05-2024",
            label="date",
            start_index=86,
            end_index=96,
            type="date",
        )
    ]
    + [
        Entity(
            text=str,
            label="date",
            start_index=86,
            end_index=86 + len(str),
            type="date",
        )
        for str in DATETIME_STRS
    ],
    "integer": Entity(
        text="123456789",
        label="integer",
        start_index=121,
        end_index=132,
        type="integer",
    ),
    "float": Entity(
        text="123,456,789.000",
        label="float",
        start_index=121,
        end_index=132,
        type="float",
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


@pytest.fixture(scope="module")
def llm_label_generator():
    return LLMLabelGenerator()


def test_llm_label_generator_has_methods(llm_label_generator):
    assert hasattr(llm_label_generator, "generate")


def test_llm_label_generator_generate_default(llm_label_generator):
    entity = TEST_ENTITIES["name"]
    generated_text = llm_label_generator.generate(entity)
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_llm_label_generator_generate_custom(llm_label_generator):
    entity = TEST_ENTITIES["name"]
    generated_text = llm_label_generator.generate(
        entity, add_entity_attrs="Spanish", temperature=0.5
    )
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_llm_label_generator_generate_pattern(llm_label_generator):
    entity = TEST_ENTITIES["name:pattern"]
    generated_text = llm_label_generator.generate(entity)
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


# =====================================
# Test Mask Label Generator
# =====================================


@pytest.fixture(scope="module")
def mask_label_generator():
    return MaskLabelGenerator()


@pytest.fixture(autouse=True)
def suppress_warnings():
    warnings.filterwarnings("ignore", category=ImportWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)


def test_mask_label_generator_has_methods(mask_label_generator):
    assert hasattr(mask_label_generator, "generate")


def test_mask_label_generator_generate_default(mask_label_generator):
    entity = TEST_ENTITIES["name"]
    generated_text = mask_label_generator.generate(entity, text=TEST_ORIGINAL_TEXT)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


# =====================================
# Test Date Generator
# =====================================


@pytest.fixture(scope="module")
def date_generator():
    return DateGenerator(lang="en")


def test_date_generator_has_methods(date_generator):
    assert hasattr(date_generator, "generate")


def test_date_generator_generate_default(date_generator):
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_date_generator_generate_custom_date_format():
    entity = TEST_ENTITIES["date"][0]
    generator = DateGenerator(date_format="dd-MM-yyyy")
    generated_text = generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_date_generator_generate_non_matching_date_format():
    entity = TEST_ENTITIES["date"][0]
    generator = DateGenerator(date_format="yyyy-MM-dd")
    custom_date = generator.generate(entity, sub_variant="FIRST_DAY_OF_THE_MONTH")
    assert custom_date == "2024-05-01"


def test_date_generator_generate_first_day_of_the_month(date_generator):
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(
        entity, sub_variant="FIRST_DAY_OF_THE_MONTH"
    )
    assert generated_text == "01-05-2024"


def test_date_generator_generate_last_day_of_the_month(date_generator):
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(
        entity, sub_variant="LAST_DAY_OF_THE_MONTH"
    )
    assert generated_text == "31-05-2024"


def test_date_generator_generate_middle_of_the_month(date_generator):
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_MONTH")
    assert generated_text == "15-05-2024"


def test_date_generator_generate_middle_of_the_year(date_generator):
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_YEAR")
    assert generated_text == "01-07-2024"


def test_date_generator_generate_random(date_generator):
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="RANDOM")
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_date_generator_generate_uncorrect_type(date_generator):
    entity = TEST_ENTITIES["name"]
    with pytest.raises(ValueError):
        date_generator.generate(entity)


def test_date_generator_process_different_formats(date_generator):
    for entity in TEST_ENTITIES["date"]:
        try:
            date_generator.generate(entity, sub_variant="RANDOM")
        except ValueError:
            pytest.fail(
                f"date_generator.generate() raised ValueError unexpectedly for date: {entity.text}"
            )


# =====================================
# Test Number Generator
# =====================================


@pytest.fixture(scope="module")
def number_generator():
    return NumberGenerator()


def test_number_generator_has_methods(number_generator):
    assert hasattr(number_generator, "generate")


def test_number_generator_generate_integer(number_generator):
    entity = TEST_ENTITIES["integer"]
    generated_text = number_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_number_generator_generate_float(number_generator):
    entity = TEST_ENTITIES["float"]
    generated_text = number_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_number_generator_generate_custom(number_generator):
    entity = TEST_ENTITIES["custom"]
    generated_text = number_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_number_generator_generate_uncorrect_type(number_generator):
    entity = TEST_ENTITIES["name"]
    with pytest.raises(ValueError):
        number_generator.generate(entity)
