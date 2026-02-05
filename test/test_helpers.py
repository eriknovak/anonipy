"""Tests for anonipy.anonymize.helpers.filter_entities."""

from anonipy.definitions import Entity
from anonipy.anonymize.helpers import filter_entities

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
