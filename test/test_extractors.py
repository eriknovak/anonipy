import warnings

import pytest
import torch
from transformers import logging

from anonipy.definitions import Entity
from anonipy.anonymize.extractors import NERExtractor, PatternExtractor, MultiExtractor
from anonipy.constants import LANGUAGES
from anonipy.anonymize.helpers import filter_entities

# disable transformers logging
logging.set_verbosity_error()

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

The examination took place on 20-05-2024. John Doe was prescribed Ibuprofen 200 mg and Lisinopril 10 mg.
"""

TEST_NER_ENTITIES = [
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
    Entity(
        text="20-05-2024",
        label="date",
        start_index=759,
        end_index=769,
        type="date",
    ),
]
TEST_REPEATS_ENTITIES = [
    Entity(
        text="John Doe",
        label="name",
        start_index=771,
        end_index=779,
        type="string",
    ),
]
TEST_PATTERN_ENTITIES = [
    Entity(
        text="15-01-1985",
        label="date",
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
        text="blood pressure, heart rate, temperature",
        label="symptoms",
        start_index=254,
        end_index=293,
        type="string",
        regex="\\((.*)\\)",
    ),
    Entity(
        text="Ibuprofen 200 mg",
        label="medicine",
        start_index=533,
        end_index=549,
        type="string",
    ),
    Entity(
        text="Lisinopril 10 mg",
        label="medicine",
        start_index=623,
        end_index=639,
        type="string",
    ),
    Entity(
        text="15-11-2024",
        label="date",
        start_index=717,
        end_index=727,
        type="date",
    ),
    Entity(
        text="20-05-2024",
        label="date",
        start_index=759,
        end_index=769,
        type="date",
    ),
    Entity(
        text="Ibuprofen 200 mg",
        label="medicine",
        start_index=795,
        end_index=811,
        type="string",
    ),
    Entity(
        text="Lisinopril 10 mg",
        label="medicine",
        start_index=816,
        end_index=832,
        type="string",
    ),
]
TEST_PATTERN_DETECT_REPEATS = [
    Entity(
        text="20-05-2024",
        label="date",
        start_index=86,
        end_index=96,
        type="date",
        regex=r"Date of Examination: (.*)",
    ),
    # Repeated entity
    Entity(
        text="20-05-2024",
        label="date",
        start_index=759,
        end_index=769,
        type="date",
        regex=r"Date of Examination: (.*)",
    ),
]
TEST_MULTI_REPEATS = [
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
        regex=r"Date of Examination: (.*)",
    ),
    Entity(
        text="John Doe",
        label="name",
        start_index=157,
        end_index=165,
        type="string",
    ),
    # Repeated entities
    Entity(
        text="20-05-2024",
        label="date",
        start_index=759,
        end_index=769,
        type="date",
        regex=r"Date of Examination: (.*)",
    ),
    Entity(
        text="John Doe",
        label="name",
        start_index=771,
        end_index=779,
        type="string",
    ),
]


@pytest.fixture(autouse=True)
def suppress_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=ResourceWarning)


@pytest.fixture(scope="module")
def ner_extractor():
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
    return NERExtractor(labels=labels, lang=LANGUAGES.ENGLISH)


@pytest.fixture(scope="module")
def pattern_extractor():
    labels = [
        {
            "label": "symptoms",
            "type": "string",
            "regex": r"\((.*)\)",  # symptoms are enclosed in parentheses
        },
        {
            "label": "medicine",
            "type": "string",
            "pattern": [[{"IS_ALPHA": True}, {"LIKE_NUM": True}, {"LOWER": "mg"}]],
        },
        {
            "label": "date",
            "type": "date",
            "pattern": [  # represent the date as a sequence of digits using spacy
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
    return PatternExtractor(labels=labels, lang=LANGUAGES.ENGLISH)


@pytest.fixture(scope="module")
def multi_extractor(ner_extractor, pattern_extractor):
    return MultiExtractor([ner_extractor, pattern_extractor])


def test_ner_extractor_init():
    with pytest.raises(TypeError):
        NERExtractor()


def test_ner_extractor_init_inputs(ner_extractor):
    extractor = NERExtractor(
        labels=ner_extractor.labels, lang=LANGUAGES.ENGLISH, score_th=0.5
    )
    assert isinstance(extractor, NERExtractor)


def test_ner_extractor_init_gpu(ner_extractor):
    if torch.cuda.is_available():
        extractor = NERExtractor(
            labels=ner_extractor.labels,
            lang=LANGUAGES.ENGLISH,
            score_th=0.5,
            use_gpu=True,
        )
        assert isinstance(extractor, NERExtractor)


def test_ner_extractor_methods(ner_extractor):
    assert hasattr(ner_extractor, "__call__")
    assert hasattr(ner_extractor, "display")


def test_ner_extractor_extract_default_params(ner_extractor):
    _, entities = ner_extractor(TEST_ORIGINAL_TEXT)
    for p_entity, t_entity in zip(entities, TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_ner_extractor_extract_default_params_input():
    extractor = NERExtractor(
        labels=[
            {"label": "name", "type": "string"},
            {
                "label": "social security number",
                "type": "custom",
                "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}",
            },
            {"label": "date of birth", "type": "date"},
            {"label": "date", "type": "date"},
        ],
        lang=LANGUAGES.ENGLISH,
        gliner_model="urchade/gliner_multi_pii-v1",
        score_th=0.5,
    )
    _, entities = extractor(TEST_ORIGINAL_TEXT)
    for p_entity, t_entity in zip(entities, TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_ner_extractor_extract_custom_params_input():
    extractor = NERExtractor(
        labels=[
            {"label": "name", "type": "string"},
            {
                "label": "social security number",
                "type": "custom",
                "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}",
            },
            {"label": "date of birth", "type": "date"},
            {"label": "date", "type": "date"},
        ],
        lang=LANGUAGES.ENGLISH,
        gliner_model="E3-JSI/gliner-multi-pii-domains-v1",
        score_th=0.5,
    )
    _, entities = extractor(TEST_ORIGINAL_TEXT)
    for p_entity, t_entity in zip(entities, TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_ner_extractor_detect_repeats_true(ner_extractor):
    _, entities = ner_extractor(TEST_ORIGINAL_TEXT, detect_repeats=True)
    expected_entities = TEST_NER_ENTITIES + TEST_REPEATS_ENTITIES
    for p_entity, t_entity in zip(entities, expected_entities):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_pattern_extractor_init():
    with pytest.raises(TypeError):
        PatternExtractor()


def test_pattern_extractor_init_inputs(pattern_extractor):
    assert isinstance(pattern_extractor, PatternExtractor)


def test_pattern_extractor_methods(pattern_extractor):
    assert hasattr(pattern_extractor, "__call__")
    assert hasattr(pattern_extractor, "display")


def test_pattern_extractor_extract_default(pattern_extractor):
    doc, entities = pattern_extractor(TEST_ORIGINAL_TEXT)
    for p_entity, t_entity in zip(entities, TEST_PATTERN_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score == 1.0


def test_pattern_extractor_detect_repeats_false():
    extractor = PatternExtractor(
        labels=[
            {
                "label": "date",
                "type": "date",
                "regex": r"Date of Examination: (.*)",
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(TEST_ORIGINAL_TEXT, detect_repeats=False)
    excepted_entity = TEST_PATTERN_DETECT_REPEATS[0]
    assert len(entities) == 1
    assert excepted_entity.text == entities[0].text
    assert excepted_entity.label == entities[0].label
    assert excepted_entity.start_index == entities[0].start_index
    assert excepted_entity.end_index == entities[0].end_index
    assert excepted_entity.type == entities[0].type
    assert excepted_entity.regex == entities[0].regex
    assert excepted_entity.score >= 0.5


def test_pattern_extractor_detect_repeats_true():
    extractor = PatternExtractor(
        labels=[
            {
                "label": "date",
                "type": "date",
                "regex": r"Date of Examination: (.*)",
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(TEST_ORIGINAL_TEXT, detect_repeats=True)
    for p_entity, t_entity in zip(entities, TEST_PATTERN_DETECT_REPEATS):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_multi_extractor_init():
    with pytest.raises(TypeError):
        MultiExtractor()


def test_multi_extractor_init_inputs(multi_extractor):
    assert isinstance(multi_extractor, MultiExtractor)


def test_multi_extractor_methods(multi_extractor):
    assert hasattr(multi_extractor, "__call__")
    assert hasattr(multi_extractor, "display")


def test_multi_extractor_extract_default(multi_extractor):
    extractor_outputs, joint_entities = multi_extractor(TEST_ORIGINAL_TEXT)

    # check the performance of the first extractor
    for p_entity, t_entity in zip(extractor_outputs[0][1], TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5

    # check the performance of the second extractor
    for p_entity, t_entity in zip(extractor_outputs[1][1], TEST_PATTERN_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score == 1.0

    # check the performance of the joint entities generation
    for p_entity, t_entity in zip(
        joint_entities,
        filter_entities(TEST_NER_ENTITIES + TEST_REPEATS_ENTITIES + TEST_PATTERN_ENTITIES),
    ):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_multi_extractor_extract_empty_extractor_list():
    with pytest.raises(ValueError):
        MultiExtractor([])


def test_multi_extractor_extract_invalid_extractor_list():
    with pytest.raises(ValueError):
        MultiExtractor([NERExtractor(labels=[], lang=LANGUAGES.ENGLISH), "invalid"])


def test_multi_extractor_extract_single_extractor_ner(multi_extractor):
    extractor = MultiExtractor([multi_extractor.extractors[0]])
    extractor_outputs, joint_entities = extractor(TEST_ORIGINAL_TEXT)

    # check the performance of the extractor
    for p_entity, t_entity in zip(extractor_outputs[0][1], TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5

    # check the performance of the joint entities generation
    for p_entity, t_entity in zip(joint_entities, TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_multi_extractor_extract_single_extractor_pattern(multi_extractor):
    extractor = MultiExtractor([multi_extractor.extractors[1]])
    extractor_outputs, joint_entities = extractor(TEST_ORIGINAL_TEXT)

    # check the performance of the extractor
    for p_entity, t_entity in zip(extractor_outputs[0][1], TEST_PATTERN_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5

    # check the performance of the joint entities generation
    for p_entity, t_entity in zip(joint_entities, TEST_PATTERN_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_multi_extractor_detect_repeats_false():
    extractors = [
        NERExtractor(
            labels=[
                {"label": "name", "type": "string"},
            ]
        ),
        PatternExtractor(
            labels=[
                {
                    "label": "date",
                    "type": "date",
                    "regex": r"Date of Examination: (.*)",
                },
            ]
        ),
    ]
    extractor = MultiExtractor(extractors)
    _, joint_entities = extractor(TEST_ORIGINAL_TEXT, detect_repeats=False)
    for p_entity, t_entity in zip(joint_entities, TEST_MULTI_REPEATS[:3]):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


def test_multi_extractor_detect_repeats_true():
    extractors = [
        NERExtractor(
            labels=[
                {"label": "name", "type": "string"},
            ]
        ),
        PatternExtractor(
            labels=[
                {
                    "label": "date",
                    "type": "date",
                    "regex": r"Date of Examination: (.*)",
                },
            ]
        ),
    ]
    extractor = MultiExtractor(extractors)
    _, joint_entities = extractor(TEST_ORIGINAL_TEXT, detect_repeats=True)
    for p_entity, t_entity in zip(joint_entities, TEST_MULTI_REPEATS):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5
