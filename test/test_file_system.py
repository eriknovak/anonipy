import pytest

from anonipy.utils.file_system import open_file
from test.resources.example_outputs import WORD_TEXT, PDF_TEXT, TXT_TEXT

RESOURCES = {
    "word": "./test/resources/example.docx",
    "pdf": "./test/resources/example.pdf",
    "txt": "./test/resources/example.txt",
}


@pytest.mark.parametrize(
    "file_type, expected_output",
    [
        ("word", WORD_TEXT),
        ("pdf", PDF_TEXT),
        ("txt", TXT_TEXT),
    ],
)
def test_open_file(file_type, expected_output):
    assert open_file(RESOURCES[file_type]) == expected_output
