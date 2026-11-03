"""Tests for anonipy.anonymize.extractors."""

import itertools
import warnings

import pytest
import torch
from transformers import logging

from anonipy.anonymize.extractors import MultiExtractor, NERExtractor, PatternExtractor
from anonipy.anonymize.helpers import filter_entities
from anonipy.constants import LANGUAGES
from anonipy.definitions import Entity
from test.conftest import FAKE_GLINER_SCORE, HAS_GPU

# disable transformers logging
logging.set_verbosity_error()

# =====================================
# Test Data
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

# =====================================
# Fixtures
# =====================================


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


# =====================================
# Test NER Extractor
# =====================================


def test_ner_extractor_init():
    """Test that NERExtractor requires arguments."""
    with pytest.raises(TypeError):
        NERExtractor()


@pytest.mark.slow
def test_ner_extractor_init_inputs(ner_extractor):
    """Test NERExtractor instantiation with custom inputs."""
    extractor = NERExtractor(labels=ner_extractor.labels, lang=LANGUAGES.ENGLISH, score_th=0.5)
    assert isinstance(extractor, NERExtractor)


@pytest.mark.skipif(not HAS_GPU, reason="GPU not available")
@pytest.mark.slow
def test_ner_extractor_init_gpu(ner_extractor):
    """Test NERExtractor instantiation with GPU."""
    extractor = NERExtractor(
        labels=ner_extractor.labels,
        lang=LANGUAGES.ENGLISH,
        score_th=0.5,
        use_gpu=True,
    )
    assert isinstance(extractor, NERExtractor)


@pytest.mark.slow
def test_ner_extractor_methods(ner_extractor):
    """Test that NERExtractor has required methods."""
    assert callable(ner_extractor)
    assert hasattr(ner_extractor, "display")


@pytest.mark.slow
def test_ner_extractor_extract_default_params(ner_extractor):
    """Test NER extraction with default parameters."""
    _, entities = ner_extractor(TEST_ORIGINAL_TEXT)
    for p_entity, t_entity in zip(entities, TEST_NER_ENTITIES):
        assert p_entity.text == t_entity.text
        assert p_entity.label == t_entity.label
        assert p_entity.start_index == t_entity.start_index
        assert p_entity.end_index == t_entity.end_index
        assert p_entity.type == t_entity.type
        assert p_entity.regex == t_entity.regex
        assert p_entity.score >= 0.5


@pytest.mark.slow
def test_ner_extractor_extract_default_params_input():
    """Test NER extraction with explicit default model."""
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


@pytest.mark.slow
def test_ner_extractor_extract_custom_params_input():
    """Test NER extraction with custom GLiNER model."""
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


@pytest.mark.slow
def test_ner_extractor_detect_repeats_true(ner_extractor):
    """Test NER extraction with repeat detection enabled."""
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


# =====================================
# Test NER Extractor With A Fake Model
# =====================================


def make_ner_labels():
    return [
        {"label": "name", "type": "string"},
        {"label": "social security number", "type": "custom", "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}"},
        {"label": "date of birth", "type": "date"},
        {"label": "date", "type": "date"},
    ]


@pytest.fixture
def fake_ner_extractor(fake_gliner):
    return NERExtractor(labels=make_ner_labels(), lang=LANGUAGES.ENGLISH)


def test_ner_extractor_fake_returns_tagged_entities(fake_ner_extractor):
    """Test that each tagged phrase becomes an entity typed by its label."""
    _, entities = fake_ner_extractor(TEST_ORIGINAL_TEXT)
    found = [(e.text, e.label, e.type, e.start_index, e.score) for e in entities]
    assert found == [
        ("John Doe", "name", "string", 30, FAKE_GLINER_SCORE),
        ("15-01-1985", "date of birth", "date", 54, FAKE_GLINER_SCORE),
        ("123-45-6789", "social security number", "custom", 121, FAKE_GLINER_SCORE),
        ("John Doe", "name", "string", 771, FAKE_GLINER_SCORE),
    ]


def test_ner_extractor_fake_maps_chunk_offsets_to_text(fake_ner_extractor):
    """Test that entities found in later text chunks point at their text."""
    _, entities = fake_ner_extractor(TEST_ORIGINAL_TEXT)
    assert entities[-1].start_index > 384
    for entity in entities:
        assert TEST_ORIGINAL_TEXT[entity.start_index : entity.end_index] == entity.text


def test_ner_extractor_fake_drops_entities_failing_label_regex(fake_ner_extractor):
    """Test that a tagged phrase not matching its label regex is dropped."""
    _, entities = fake_ner_extractor(TEST_ORIGINAL_TEXT)
    assert "Medical Record" not in [e.text for e in entities]


def test_ner_extractor_fake_detect_repeats_finds_untagged_occurrences(fake_ner_extractor):
    """Test that repeat detection adds occurrences the model did not tag."""
    _, entities = fake_ner_extractor(TEST_ORIGINAL_TEXT, detect_repeats=True)
    assert [e.start_index for e in entities if e.text == "John Doe"] == [30, 157, 771]


def test_ner_extractor_fake_span_style_stores_spans(fake_gliner):
    """Test that the span style stores the entities in the doc spans."""
    extractor = NERExtractor(labels=make_ner_labels(), lang=LANGUAGES.ENGLISH, spacy_style="span")
    doc, entities = extractor(TEST_ORIGINAL_TEXT)
    span_starts = {span.start_char for span in doc.spans["sc"]}
    assert {e.start_index for e in entities} <= span_starts
    assert doc.ents == ()


def test_ner_extractor_fake_loads_configured_model_on_cpu(fake_gliner):
    """Test that the extractor loads the requested GLiNER model on the CPU."""
    NERExtractor(labels=make_ner_labels(), gliner_model="some/gliner-model")
    assert fake_gliner == [{"model_name": "some/gliner-model", "map_location": "cpu"}]


@pytest.mark.skipif(HAS_GPU, reason="GPU available")
def test_ner_extractor_fake_gpu_without_cuda_falls_back_to_cpu(fake_gliner):
    """Test that requesting a missing GPU warns and loads the model on the CPU."""
    with pytest.warns(UserWarning, match="GPU"):
        NERExtractor(labels=make_ner_labels(), use_gpu=True)
    assert fake_gliner[0]["map_location"] == "cpu"


@pytest.mark.skipif(HAS_GPU, reason="GPU available")
def test_ner_extractor_fake_gpu_without_cuda_warns_at_caller(fake_gliner):
    """Test that the missing-GPU warning points at the line that built the extractor."""
    with pytest.warns(UserWarning, match="GPU") as record:
        NERExtractor(labels=make_ner_labels(), use_gpu=True)
    assert len(record) == 1
    assert record[0].filename == __file__


@pytest.mark.skipif(HAS_GPU, reason="GPU available")
def test_ner_extractor_fake_gpu_without_cuda_keeps_configured_settings(fake_gliner):
    """Test that the CPU fallback builds the GLiNER component from the extractor's settings."""
    with pytest.warns(UserWarning, match="GPU"):
        extractor = NERExtractor(
            labels=make_ner_labels(), use_gpu=True, score_th=0.7, gliner_model="some/gliner-model", spacy_style="span"
        )
    component = extractor.pipeline.get_pipe("gliner_spacy")
    assert component.labels == ["name", "social security number", "date of birth", "date"]
    assert component.threshold == 0.7
    assert component.style == "span"
    assert fake_gliner[0]["model_name"] == "some/gliner-model"


def test_ner_extractor_fake_gpu_with_cuda_loads_on_cuda(fake_gliner, monkeypatch):
    """Test that a requested and available GPU loads the model on CUDA without a warning."""
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        NERExtractor(labels=make_ner_labels(), use_gpu=True)
    assert fake_gliner[0]["map_location"] == "cuda"


def test_ner_extractor_fake_without_gpu_request_loads_on_cpu_silently(fake_gliner):
    """Test that use_gpu=False loads the model on the CPU without a warning."""
    with warnings.catch_warnings():
        warnings.simplefilter("error", UserWarning)
        NERExtractor(labels=make_ner_labels(), use_gpu=False)
    assert fake_gliner[0]["map_location"] == "cpu"


def test_ner_extractor_fake_display_renders_entities(fake_ner_extractor):
    """Test that display renders the extracted entities as HTML."""
    doc, _ = fake_ner_extractor(TEST_ORIGINAL_TEXT)
    html = fake_ner_extractor.display(doc)
    assert "John Doe" in html
    assert "date of birth" in html


# =====================================
# Test Pattern Extractor
# =====================================


def test_pattern_extractor_init():
    """Test that PatternExtractor requires arguments."""
    with pytest.raises(TypeError):
        PatternExtractor()


def test_pattern_extractor_init_inputs(pattern_extractor):
    """Test PatternExtractor instantiation."""
    assert isinstance(pattern_extractor, PatternExtractor)


def test_pattern_extractor_methods(pattern_extractor):
    """Test that PatternExtractor has required methods."""
    assert callable(pattern_extractor)
    assert hasattr(pattern_extractor, "display")


def test_pattern_extractor_extract_default(pattern_extractor):
    """Test pattern extraction with default parameters."""
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
    """Test pattern extraction with repeat detection disabled."""
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
    """Test pattern extraction with repeat detection enabled."""
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


def test_pattern_extractor_numbers_ssn_regex():
    """Test PatternExtractor for identifying Social Security Numbers using regex."""
    extractor = PatternExtractor(
        labels=[
            {
                "label": "social security number",
                "type": "custom",
                "regex": r"([0-9]{3}-[0-9]{2}-[0-9]{4})",
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(TEST_ORIGINAL_TEXT)
    assert len(entities) == 1
    assert entities[0].text == "123-45-6789"
    assert entities[0].label == "social security number"
    assert entities[0].start_index == 121
    assert entities[0].end_index == 132
    assert entities[0].type == "custom"
    assert entities[0].score == 1.0


def test_pattern_extractor_numbers_dosage():
    """Test PatternExtractor for identifying numeric dosages using patterns."""
    extractor = PatternExtractor(
        labels=[
            {
                "label": "dosage",
                "type": "string",
                "pattern": [[{"LIKE_NUM": True}, {"LOWER": "mg"}]],
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(TEST_ORIGINAL_TEXT)
    # Should find "200 mg" and "10 mg" (appears twice each in the text)
    assert len(entities) >= 2
    dosages = [entity.text for entity in entities]
    assert "200 mg" in dosages
    assert "10 mg" in dosages
    for entity in entities:
        assert entity.label == "dosage"
        assert entity.type == "string"
        assert entity.score == 1.0


def test_pattern_extractor_numbers_phone():
    """Test PatternExtractor for identifying phone numbers using regex."""
    test_text = "Contact: 555-123-4567 or call (555) 987-6543 for more info."
    extractor = PatternExtractor(
        labels=[
            {
                "label": "phone",
                "type": "custom",
                "regex": r"(\d{3}-\d{3}-\d{4})",
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(test_text)
    assert len(entities) == 1
    assert entities[0].text == "555-123-4567"
    assert entities[0].label == "phone"
    assert entities[0].type == "custom"
    assert entities[0].score == 1.0


def test_pattern_extractor_regex_without_capture_group():
    """Test PatternExtractor with regex that has no capture group."""
    test_text = "Contact: 555-123-4567 or call (555) 987-6543 for more info."
    extractor = PatternExtractor(
        labels=[
            {
                "label": "phone",
                "type": "custom",
                "regex": r"\d{3}-\d{3}-\d{4}",
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(test_text)
    assert len(entities) == 1
    assert entities[0].text == "555-123-4567"
    assert entities[0].label == "phone"
    assert entities[0].type == "custom"
    assert entities[0].score == 1.0


def test_pattern_extractor_numbers_general():
    """Test PatternExtractor for identifying general numeric values."""
    test_text = "The patient weighs 150 pounds and is 72 inches tall."
    extractor = PatternExtractor(
        labels=[
            {
                "label": "measurement",
                "type": "string",
                "pattern": [[{"LIKE_NUM": True}, {"IS_ALPHA": True}]],
            }
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(test_text)
    assert len(entities) == 2
    measurements = [entity.text for entity in entities]
    assert "150 pounds" in measurements
    assert "72 inches" in measurements
    for entity in entities:
        assert entity.label == "measurement"
        assert entity.type == "string"
        assert entity.score == 1.0


def test_pattern_extractor_numbers_mixed_formats():
    """Test PatternExtractor for identifying numbers in various formats."""
    test_text = "Account: 12345, Balance: $1,234.56, Code: ABC-123"
    extractor = PatternExtractor(
        labels=[
            {
                "label": "account_number",
                "type": "custom",
                "regex": r"Account: (\d+)",
            },
            {
                "label": "amount",
                "type": "custom",
                "regex": r"Balance: (\$[\d,]+\.?\d*)",
            },
        ],
        lang=LANGUAGES.ENGLISH,
    )
    _, entities = extractor(test_text)
    assert len(entities) == 2

    # Check account number
    account_entity = [e for e in entities if e.label == "account_number"][0]
    assert account_entity.text == "12345"
    assert account_entity.type == "custom"

    # Check amount
    amount_entity = [e for e in entities if e.label == "amount"][0]
    assert amount_entity.text == "$1,234.56"
    assert amount_entity.type == "custom"


# =====================================
# Test Multi Extractor
# =====================================


def test_multi_extractor_init():
    """Test that MultiExtractor requires arguments."""
    with pytest.raises(TypeError):
        MultiExtractor()


@pytest.mark.slow
def test_multi_extractor_init_inputs(multi_extractor):
    """Test MultiExtractor instantiation."""
    assert isinstance(multi_extractor, MultiExtractor)


@pytest.mark.slow
def test_multi_extractor_methods(multi_extractor):
    """Test that MultiExtractor has required methods."""
    assert callable(multi_extractor)
    assert hasattr(multi_extractor, "display")


@pytest.mark.slow
@pytest.mark.integration
def test_multi_extractor_extract_default(multi_extractor):
    """Test MultiExtractor extraction with default parameters."""
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
    """Test that empty extractor list raises ValueError."""
    with pytest.raises(ValueError):
        MultiExtractor([])


def test_multi_extractor_extract_invalid_extractor_list(fake_gliner):
    """Test that invalid extractor in list raises ValueError."""
    with pytest.raises(ValueError):
        MultiExtractor([NERExtractor(labels=[], lang=LANGUAGES.ENGLISH), "invalid"])


def test_multi_extractor_fake_merges_entities_of_all_extractors(fake_ner_extractor, pattern_extractor):
    """Test that the joint entities hold both extractors' entities, ordered and without overlap."""
    extractor = MultiExtractor([fake_ner_extractor, pattern_extractor])
    outputs, joint_entities = extractor(TEST_ORIGINAL_TEXT)
    assert len(outputs) == 2
    assert {"name", "medicine"} <= {e.label for e in joint_entities}
    for previous, current in itertools.pairwise(joint_entities):
        assert previous.end_index <= current.start_index


def test_multi_extractor_fake_display_renders_entities(fake_ner_extractor, pattern_extractor):
    """Test that display renders the entities as HTML."""
    extractor = MultiExtractor([fake_ner_extractor, pattern_extractor])
    outputs, _ = extractor(TEST_ORIGINAL_TEXT)
    html = extractor.display(outputs[0][0])
    assert "John Doe" in html


@pytest.mark.slow
@pytest.mark.integration
def test_multi_extractor_extract_single_extractor_ner(multi_extractor):
    """Test MultiExtractor with single NER extractor."""
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


@pytest.mark.slow
@pytest.mark.integration
def test_multi_extractor_extract_single_extractor_pattern(multi_extractor):
    """Test MultiExtractor with single pattern extractor."""
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


@pytest.mark.slow
@pytest.mark.integration
def test_multi_extractor_detect_repeats_false():
    """Test MultiExtractor with repeat detection disabled."""
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


@pytest.mark.slow
@pytest.mark.integration
def test_multi_extractor_detect_repeats_true():
    """Test MultiExtractor with repeat detection enabled."""
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
