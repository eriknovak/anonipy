from anonipy.anonymize import anonymize

# =====================================
# Helper functions
# =====================================

test_text = "Test this string, and this test too!"
test_text_anonymized = "********* this TYPE, and this NEWTEST too!"
test_replacements = [
    {
        "original_text": "Test",
        "label": "test",
        "start_index": 0,
        "end_index": 4,
        "anonymized_text": "*********",
    },
    {
        "start_index": 10,
        "end_index": 16,
        "anonymized_text": "TYPE",
    },
    {
        "original_text": "test",
        "label": "test",
        "start_index": 27,
        "end_index": 31,
        "anonymized_text": "NEWTEST",
    },
]

# =====================================
# Test Anonymize
# =====================================


def test_anonymize():
    anonymized_text, replacements = anonymize(test_text, test_replacements)
    assert anonymized_text == test_text_anonymized
    assert replacements == test_replacements
