import unittest

from anonipy.utils.file_system import open_file

# =====================================
# Helper functions
# =====================================

from test.resources.example_outputs import WORD_TEXT, PDF_TEXT, TXT_TEXT

resources = {
    "word": "./test/resources/example.docx",
    "pdf": "./test/resources/example.pdf",
    "txt": "./test/resources/example.txt",
}

# =====================================
# Test Entity Extractor
# =====================================


class TestFileSystem(unittest.TestCase):
    def test_open_file_word(self):
        self.assertEqual(open_file(resources["word"]), WORD_TEXT)

    def test_open_file_pdf(self):
        self.assertEqual(open_file(resources["pdf"]), PDF_TEXT)

    def test_open_file_txt(self):
        self.assertEqual(open_file(resources["txt"]), TXT_TEXT)


if __name__ == "__main__":
    unittest.main()
