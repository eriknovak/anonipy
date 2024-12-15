import pytest

from anonipy.definitions import Entity
from anonipy.anonymize.strategies import (
    RedactionStrategy,
    MaskingStrategy,
    PseudonymizationStrategy,
)

# =====================================
# Helper functions
# =====================================

TEST_TEXT = "Test this string, and this test too!"
TEST_ENTITIES = [
    Entity(text="Test", label="test", start_index=0, end_index=4),
    Entity(text="string", label="type", start_index=10, end_index=16),
    Entity(text="test", label="test", start_index=27, end_index=31),
]


def anonymization_mapping(text, entity):
    if entity.label == "test":
        return "[TEST]"
    elif entity.label == "type":
        return "[TYPE]"
    return "[REDACTED]"


@pytest.fixture
def redaction_strategy():
    return RedactionStrategy()


@pytest.fixture
def masking_strategy():
    return MaskingStrategy()


@pytest.fixture
def pseudonymization_strategy():
    return PseudonymizationStrategy(mapping=anonymization_mapping)


# =====================================
# Test Redaction Strategy
# =====================================


def test_redaction_strategy_init(redaction_strategy):
    assert redaction_strategy.__class__ == RedactionStrategy


def test_redaction_strategy_has_methods(redaction_strategy):
    assert hasattr(redaction_strategy, "anonymize")


@pytest.mark.parametrize(
    "substitute_label, expected_label",
    [
        (None, "[REDACTED]"),
        ("[TEST]", "[TEST]"),
    ],
)
def test_redaction_strategy_inputs(substitute_label, expected_label):
    strategy = RedactionStrategy(substitute_label=substitute_label)
    assert strategy.substitute_label == expected_label


@pytest.mark.parametrize(
    "substitute_label, expected_text, expected_replacements",
    [
        (
            None,
            "[REDACTED] this [REDACTED], and this [REDACTED] too!",
            [
                {
                    "original_text": "Test",
                    "label": "test",
                    "start_index": 0,
                    "end_index": 4,
                    "anonymized_text": "[REDACTED]",
                },
                {
                    "original_text": "string",
                    "label": "type",
                    "start_index": 10,
                    "end_index": 16,
                    "anonymized_text": "[REDACTED]",
                },
                {
                    "original_text": "test",
                    "label": "test",
                    "start_index": 27,
                    "end_index": 31,
                    "anonymized_text": "[REDACTED]",
                },
            ],
        ),
        (
            "[TEST]",
            "[TEST] this [TEST], and this [TEST] too!",
            [
                {
                    "original_text": "Test",
                    "label": "test",
                    "start_index": 0,
                    "end_index": 4,
                    "anonymized_text": "[TEST]",
                },
                {
                    "original_text": "string",
                    "label": "type",
                    "start_index": 10,
                    "end_index": 16,
                    "anonymized_text": "[TEST]",
                },
                {
                    "original_text": "test",
                    "label": "test",
                    "start_index": 27,
                    "end_index": 31,
                    "anonymized_text": "[TEST]",
                },
            ],
        ),
    ],
)
def test_redaction_strategy_anonymize(
    substitute_label, expected_text, expected_replacements
):
    strategy = RedactionStrategy(substitute_label=substitute_label)
    anonymized_text, replacements = strategy.anonymize(TEST_TEXT, TEST_ENTITIES)
    assert anonymized_text == expected_text
    assert replacements == expected_replacements


# =====================================
# Test Masking Strategy
# =====================================


def test_masking_strategy_init(masking_strategy):
    assert masking_strategy.__class__ == MaskingStrategy


def test_masking_strategy_methods(masking_strategy):
    assert hasattr(masking_strategy, "anonymize")


@pytest.mark.parametrize(
    "substitute_label, expected_label",
    [
        (None, "*"),
        ("A", "A"),
    ],
)
def test_masking_strategy_inputs(substitute_label, expected_label):
    strategy = MaskingStrategy(substitute_label=substitute_label)
    assert strategy.substitute_label == expected_label


@pytest.mark.parametrize(
    "substitute_label, expected_text, expected_replacements",
    [
        (
            None,
            "**** this ******, and this **** too!",
            [
                {
                    "original_text": "Test",
                    "label": "test",
                    "start_index": 0,
                    "end_index": 4,
                    "anonymized_text": "****",
                },
                {
                    "original_text": "string",
                    "label": "type",
                    "start_index": 10,
                    "end_index": 16,
                    "anonymized_text": "******",
                },
                {
                    "original_text": "test",
                    "label": "test",
                    "start_index": 27,
                    "end_index": 31,
                    "anonymized_text": "****",
                },
            ],
        ),
        (
            "A",
            "AAAA this AAAAAA, and this AAAA too!",
            [
                {
                    "original_text": "Test",
                    "label": "test",
                    "start_index": 0,
                    "end_index": 4,
                    "anonymized_text": "AAAA",
                },
                {
                    "original_text": "string",
                    "label": "type",
                    "start_index": 10,
                    "end_index": 16,
                    "anonymized_text": "AAAAAA",
                },
                {
                    "original_text": "test",
                    "label": "test",
                    "start_index": 27,
                    "end_index": 31,
                    "anonymized_text": "AAAA",
                },
            ],
        ),
    ],
)
def test_masking_strategy_anonymize(
    substitute_label, expected_text, expected_replacements
):
    strategy = MaskingStrategy(substitute_label=substitute_label)
    anonymized_text, replacements = strategy.anonymize(TEST_TEXT, TEST_ENTITIES)
    assert anonymized_text == expected_text
    assert replacements == expected_replacements


# =====================================
# Test Pseudonymization Strategy
# =====================================


def test_pseudonymization_strategy_init():
    with pytest.raises(TypeError):
        PseudonymizationStrategy()


def test_pseudonymization_strategy_init_inputs(pseudonymization_strategy):
    assert pseudonymization_strategy.__class__ == PseudonymizationStrategy


def test_pseudonymization_strategy_methods(pseudonymization_strategy):
    assert hasattr(pseudonymization_strategy, "anonymize")


def test_pseudonymization_strategy_anonymize_inputs(pseudonymization_strategy):
    anonymized_text, replacements = pseudonymization_strategy.anonymize(
        TEST_TEXT, TEST_ENTITIES
    )
    assert anonymized_text == "[TEST] this [TYPE], and this [TEST] too!"
    assert replacements == [
        {
            "original_text": "Test",
            "label": "test",
            "start_index": 0,
            "end_index": 4,
            "anonymized_text": "[TEST]",
        },
        {
            "original_text": "string",
            "label": "type",
            "start_index": 10,
            "end_index": 16,
            "anonymized_text": "[TYPE]",
        },
        {
            "original_text": "test",
            "label": "test",
            "start_index": 27,
            "end_index": 31,
            "anonymized_text": "[TEST]",
        },
    ]
