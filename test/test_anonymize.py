"""Tests for anonipy.anonymize."""

import pytest

from anonipy.anonymize import anonymize

# =====================================
# Test Data
# =====================================

TEST_TEXT = "Test this string, and this test too!"
TEST_TEXT_ANONYMIZED = "********* this TYPE, and this NEWTEST too!"
TEST_REPLACEMENTS = [
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
    """Test basic anonymization with multiple replacements."""
    anonymized_text, replacements = anonymize(TEST_TEXT, TEST_REPLACEMENTS)
    assert anonymized_text == TEST_TEXT_ANONYMIZED
    assert replacements == TEST_REPLACEMENTS


def test_anonymize_empty_text():
    """Test anonymization with empty text and no replacements."""
    anonymized_text, replacements = anonymize("", [])
    assert anonymized_text == ""
    assert replacements == []


def test_anonymize_empty_replacements():
    """Test anonymization with text but no replacements."""
    anonymized_text, replacements = anonymize(TEST_TEXT, [])
    assert anonymized_text == TEST_TEXT
    assert replacements == []


def test_anonymize_single_replacement():
    """Test anonymization with a single replacement."""
    replacement = [
        {
            "original_text": "Test",
            "start_index": 0,
            "end_index": 4,
            "anonymized_text": "REPLACED",
        },
    ]
    anonymized_text, _ = anonymize(TEST_TEXT, replacement)
    assert anonymized_text == "REPLACED this string, and this test too!"


def test_anonymize_out_of_order_replacements():
    """Test that replacements given out of order still work."""
    replacements = [
        {
            "start_index": 27,
            "end_index": 31,
            "anonymized_text": "SECOND",
        },
        {
            "start_index": 0,
            "end_index": 4,
            "anonymized_text": "FIRST",
        },
    ]
    anonymized_text, _ = anonymize(TEST_TEXT, replacements)
    assert anonymized_text == "FIRST this string, and this SECOND too!"


def test_anonymize_length_changing_replacement():
    """Test replacement that changes the text length."""
    replacement = [
        {
            "start_index": 0,
            "end_index": 4,
            "anonymized_text": "X",
        },
    ]
    anonymized_text, _ = anonymize(TEST_TEXT, replacement)
    assert anonymized_text == "X this string, and this test too!"


def test_anonymize_longer_replacement():
    """Test replacement longer than original text."""
    replacement = [
        {
            "start_index": 0,
            "end_index": 4,
            "anonymized_text": "MUCHLONGERTEXT",
        },
    ]
    anonymized_text, _ = anonymize(TEST_TEXT, replacement)
    assert anonymized_text == "MUCHLONGERTEXT this string, and this test too!"


def test_anonymize_adjacent_replacements():
    """Test replacements that are right next to each other."""
    text = "AB"
    replacements = [
        {
            "start_index": 0,
            "end_index": 1,
            "anonymized_text": "X",
        },
        {
            "start_index": 1,
            "end_index": 2,
            "anonymized_text": "Y",
        },
    ]
    anonymized_text, _ = anonymize(text, replacements)
    assert anonymized_text == "XY"
