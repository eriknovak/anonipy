"""Tests for anonipy.utils.file_system."""

import os
import json

import pytest

from anonipy.utils.file_system import open_file, write_file, open_json, write_json
from test.resources.example_outputs import WORD_TEXT, PDF_TEXT, TXT_TEXT

# =====================================
# Test Data
# =====================================

RESOURCES_DIR = os.path.join(os.path.dirname(__file__), "resources")
RESOURCES = {
    "word": os.path.join(RESOURCES_DIR, "example.docx"),
    "pdf": os.path.join(RESOURCES_DIR, "example.pdf"),
    "txt": os.path.join(RESOURCES_DIR, "example.txt"),
}

# =====================================
# Test open_file
# =====================================


@pytest.mark.parametrize(
    "file_type, expected_output",
    [
        ("word", WORD_TEXT),
        ("pdf", PDF_TEXT),
        ("txt", TXT_TEXT),
    ],
)
def test_open_file(file_type, expected_output):
    """Test opening supported file formats."""
    assert open_file(RESOURCES[file_type]) == expected_output


def test_open_file_not_found():
    """Test that opening a nonexistent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        open_file("/nonexistent/path/file.txt")


def test_open_file_unsupported_extension(tmp_path):
    """Test that an unsupported extension raises ValueError."""
    unsupported = tmp_path / "file.xyz"
    unsupported.write_text("data")
    with pytest.raises(ValueError, match="not supported"):
        open_file(str(unsupported))


# =====================================
# Test write_file
# =====================================


def test_write_file_basic(tmp_path):
    """Test basic file writing."""
    path = str(tmp_path / "out.txt")
    write_file("hello", path)
    with open(path, "r", encoding="utf-8") as f:
        assert f.read() == "hello"


def test_write_file_text_type_error():
    """Test that non-string text raises TypeError."""
    with pytest.raises(TypeError, match="text must be a string"):
        write_file(123, "some_path.txt")


def test_write_file_path_type_error():
    """Test that non-string file_path raises TypeError."""
    with pytest.raises(TypeError, match="file_path must be a string"):
        write_file("hello", 123)


def test_write_file_nonexistent_dir():
    """Test that writing to a nonexistent directory raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        write_file("hello", "/nonexistent/dir/file.txt")


def test_write_file_encode_string(tmp_path):
    """Test writing with a string encoding parameter."""
    path = str(tmp_path / "out.txt")
    write_file("hello", path, encode="utf-8")
    with open(path, "r", encoding="utf-8") as f:
        assert f.read() == "hello"


def test_write_file_encode_false(tmp_path):
    """Test writing with encode=False."""
    path = str(tmp_path / "out.txt")
    write_file("hello", path, encode=False)
    with open(path, "r") as f:
        assert f.read() == "hello"


def test_write_file_encode_type_error():
    """Test that invalid encode type raises TypeError."""
    with pytest.raises(TypeError, match="encode must be a string or a boolean"):
        write_file("hello", "/tmp/file.txt", encode=123)


# =====================================
# Test open_json
# =====================================


def test_open_json(tmp_path):
    """Test opening a JSON file."""
    path = str(tmp_path / "data.json")
    data = {"key": "value", "num": 42}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    result = open_json(path)
    assert result == data


def test_open_json_not_found():
    """Test that opening a nonexistent JSON file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        open_json("/nonexistent/path/data.json")


# =====================================
# Test write_json
# =====================================


def test_write_json(tmp_path):
    """Test writing a JSON file."""
    path = str(tmp_path / "output.json")
    data = {"key": "value"}
    write_json(data, path)
    with open(path, "r", encoding="utf-8") as f:
        result = json.load(f)
    assert result == data


def test_write_json_creates_dir(tmp_path):
    """Test that write_json creates missing directories."""
    path = str(tmp_path / "subdir" / "output.json")
    data = {"nested": True}
    write_json(data, path)
    assert os.path.isfile(path)
    with open(path, "r", encoding="utf-8") as f:
        assert json.load(f) == data
