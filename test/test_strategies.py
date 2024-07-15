import unittest

from anonipy.definitions import Entity
from anonipy.anonymize.strategies import (
    RedactionStrategy,
    MaskingStrategy,
    PseudonymizationStrategy,
)

# =====================================
# Helper functions
# =====================================

test_text = "Test this string, and this test too!"
test_entities = [
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


# =====================================
# Test Redaction Strategy
# =====================================


class TestRedactionStrategy(unittest.TestCase):
    def test_init(self):
        strategy = RedactionStrategy()
        self.assertEqual(strategy.__class__, RedactionStrategy)

    def test_has_methods(self):
        strategy = RedactionStrategy()
        self.assertEqual(hasattr(strategy, "anonymize"), True)

    def test_default_inputs(self):
        strategy = RedactionStrategy()
        self.assertEqual(strategy.substitute_label, "[REDACTED]")

    def test_custom_inputs(self):
        strategy = RedactionStrategy(substitute_label="[TEST]")
        self.assertEqual(strategy.substitute_label, "[TEST]")

    def test_anonymize_default_inputs(self):
        strategy = RedactionStrategy()
        anonymized_text, replacements = strategy.anonymize(test_text, test_entities)
        self.assertEqual(
            anonymized_text, "[REDACTED] this [REDACTED], and this [REDACTED] too!"
        )
        self.assertEqual(
            replacements,
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
        )

    def test_anonymize_custom_inputs(self):
        strategy = RedactionStrategy(substitute_label="[TEST]")
        anonymized_text, replacements = strategy.anonymize(test_text, test_entities)
        self.assertEqual(anonymized_text, "[TEST] this [TEST], and this [TEST] too!")
        self.assertEqual(
            replacements,
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
        )


# =====================================
# Test Masking Strategy
# =====================================


class TestMaskingStrategy(unittest.TestCase):
    def test_init(self):
        strategy = MaskingStrategy()
        self.assertEqual(strategy.__class__, MaskingStrategy)

    def test_methods(self):
        strategy = MaskingStrategy()
        self.assertEqual(hasattr(strategy, "anonymize"), True)

    def test_default_inputs(self):
        strategy = MaskingStrategy()
        self.assertEqual(strategy.substitute_label, "*")

    def test_custom_inputs(self):
        strategy = MaskingStrategy(substitute_label="A")
        self.assertEqual(strategy.substitute_label, "A")

    def test_anonymize_default_inputs(self):
        strategy = MaskingStrategy()
        anonymized_text, replacements = strategy.anonymize(test_text, test_entities)
        self.assertEqual(anonymized_text, "**** this ******, and this **** too!")
        self.assertEqual(
            replacements,
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
        )

    def test_anonymize_custom_inputs(self):
        strategy = MaskingStrategy(substitute_label="A")
        anonymized_text, replacements = strategy.anonymize(test_text, test_entities)
        self.assertEqual(anonymized_text, "AAAA this AAAAAA, and this AAAA too!")
        self.assertEqual(
            replacements,
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
        )


# =====================================
# Test Pseudonymization Strategy
# =====================================


class TestPseudonymizationStrategy(unittest.TestCase):
    def test_init(self):
        try:
            PseudonymizationStrategy()
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_init_inputs(self):
        strategy = PseudonymizationStrategy(mapping=anonymization_mapping)
        self.assertEqual(strategy.__class__, PseudonymizationStrategy)

    def test_methods(self):
        strategy = PseudonymizationStrategy(mapping=anonymization_mapping)
        self.assertEqual(hasattr(strategy, "anonymize"), True)

    def test_anonymize_inputs(self):
        strategy = PseudonymizationStrategy(mapping=anonymization_mapping)
        anonymized_text, replacements = strategy.anonymize(test_text, test_entities)
        self.assertEqual(anonymized_text, "[TEST] this [TYPE], and this [TEST] too!")
        self.assertEqual(
            replacements,
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
                    "anonymized_text": "[TYPE]",
                },
                {
                    "original_text": "test",
                    "label": "test",
                    "start_index": 27,
                    "end_index": 31,
                    "anonymized_text": "[TEST]",
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()
