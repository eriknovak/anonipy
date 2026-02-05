"""Tests for anonipy.definitions.Entity."""

import pytest

from anonipy.definitions import Entity
from anonipy.utils.regex import REGEX_DATE

# =====================================
# Test Entity
# =====================================


def test_init_default():
    """Test Entity initialization with default values."""
    entity = Entity(
        text="test",
        label="test",
        start_index=0,
        end_index=4,
    )
    assert entity.text == "test"
    assert entity.label == "test"
    assert entity.start_index == 0
    assert entity.end_index == 4
    assert entity.score == 1.0
    assert entity.type is None
    assert entity.regex == ".*"


def test_init_custom():
    """Test Entity initialization with custom values."""
    entity = Entity(
        text="test",
        label="test",
        start_index=0,
        end_index=4,
        score=0.89,
        type="test",
        regex="test",
    )
    assert entity.text == "test"
    assert entity.label == "test"
    assert entity.start_index == 0
    assert entity.end_index == 4
    assert entity.score == 0.89
    assert entity.type == "test"
    assert entity.regex == "test"


def test_init_custom_type_without_regex_raises():
    """Test that type='custom' without regex raises ValueError."""
    with pytest.raises(ValueError, match="Custom entities require a regex"):
        Entity(
            text="test",
            label="test",
            start_index=0,
            end_index=4,
            type="custom",
        )


def test_init_date_type_gets_mapped_regex():
    """Test that type='date' maps to the REGEX_DATE pattern."""
    entity = Entity(
        text="15-01-2024",
        label="date",
        start_index=0,
        end_index=10,
        type="date",
    )
    assert entity.regex == REGEX_DATE


def test_default_score():
    """Test that the default score is 1.0."""
    entity = Entity(text="x", label="y", start_index=0, end_index=1)
    assert entity.score == 1.0


def test_custom_score():
    """Test entity with a custom score value."""
    entity = Entity(
        text="x", label="y", start_index=0, end_index=1, score=0.75
    )
    assert entity.score == 0.75


def test_str_output():
    """Test __str__() produces expected format."""
    entity = Entity(
        text="John",
        label="name",
        start_index=0,
        end_index=4,
        type="string",
    )
    result = str(entity)
    assert "Entity(" in result
    assert "text='John'" in result
    assert "label='name'" in result
    assert "start_index=0" in result
    assert "end_index=4" in result
    assert "type='string'" in result


def test_get_regex_group_with_capture():
    """Test get_regex_group() extracts inner group."""
    entity = Entity(
        text="John",
        label="name",
        start_index=0,
        end_index=4,
        regex="Person: (.*)",
    )
    assert entity.get_regex_group() == ".*"


def test_get_regex_group_without_capture():
    """Test get_regex_group() returns full regex when no group."""
    entity = Entity(
        text="John",
        label="name",
        start_index=0,
        end_index=4,
        regex=".*",
    )
    assert entity.get_regex_group() == ".*"


def test_explicit_regex_overrides_type_mapping():
    """Test that explicit regex takes precedence over type mapping."""
    entity = Entity(
        text="15-01-2024",
        label="date",
        start_index=0,
        end_index=10,
        type="date",
        regex="\\d{2}-\\d{2}-\\d{4}",
    )
    assert entity.regex == "\\d{2}-\\d{2}-\\d{4}"
