"""Tests for anonipy.anonymize.helpers."""

import pytest
import spacy

from anonipy.anonymize.helpers import (
    create_spacy_entities,
    filter_entities,
    get_doc_entity_spans,
    set_doc_entity_spans,
)
from anonipy.definitions import Entity

# =====================================
# Test filter_entities
# =====================================


def test_filter_no_overlap():
    """Test that non-overlapping entities are all kept."""
    entities = [
        Entity(text="A", label="x", start_index=0, end_index=1),
        Entity(text="B", label="x", start_index=5, end_index=6),
        Entity(text="C", label="x", start_index=10, end_index=11),
    ]
    result = filter_entities(entities)
    assert len(result) == 3


def test_filter_overlap_keeps_larger():
    """Test that overlapping entities keep the larger span."""
    entities = [
        Entity(text="AB", label="x", start_index=0, end_index=2),
        Entity(text="ABCD", label="x", start_index=0, end_index=4),
    ]
    result = filter_entities(entities)
    assert len(result) == 1
    assert result[0].text == "ABCD"


def test_filter_empty_list():
    """Test filter_entities with an empty list."""
    result = filter_entities([])
    assert result == []


def test_filter_sorted_by_start_index():
    """Test that results are sorted by start_index."""
    entities = [
        Entity(text="C", label="x", start_index=10, end_index=11),
        Entity(text="A", label="x", start_index=0, end_index=1),
        Entity(text="B", label="x", start_index=5, end_index=6),
    ]
    result = filter_entities(entities)
    assert [e.start_index for e in result] == [0, 5, 10]


# =====================================
# Test spaCy entity spans
# =====================================


@pytest.fixture
def doc():
    return spacy.blank("en")("Patient John Doe was examined.")


def test_get_doc_entity_spans_span_style_starts_empty(doc):
    """Test that the span style starts with an empty span group."""
    assert list(get_doc_entity_spans(doc, "span")) == []


def test_create_spacy_entities_span_style_adds_spans(doc):
    """Test that entities are stored as spans under the span style."""
    entity = Entity(text="John Doe", label="name", start_index=8, end_index=16)
    create_spacy_entities(doc, [entity], "span")
    assert [(span.text, span.label_) for span in doc.spans["sc"]] == [("John Doe", "name")]


@pytest.mark.parametrize("helper", [get_doc_entity_spans, lambda doc, style: set_doc_entity_spans(doc, [], style)])
def test_entity_span_helpers_reject_unknown_style(doc, helper):
    """Test that an unknown spaCy style raises ValueError."""
    with pytest.raises(ValueError, match="Invalid spacy style"):
        helper(doc, "unknown")
