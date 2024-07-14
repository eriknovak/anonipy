"""The module containing the `file_system` utilities.

The `file_system` module provides a set of utilities for reading and writing files.

Methods:
    open_file(file_path):
        Opens a file and returns its content as a string.
    write_file(text, file_path, encode):
        Writes the text to a file.
    open_json(file_path):
        Opens a JSON file and returns its content as a dictionary.
    write_json(data, file_path):
        Writes the data to a JSON file.

"""

import os
import re
import json
from typing import Union

from docx import Document
from pypdf import PdfReader


# Define namespaces
WORD_NAMESPACES = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

# =====================================
# Helper functions
# =====================================


def _remove_extra_spaces(text: str) -> str:
    """Remove extra spaces from text.

    Args:
        text: The text to remove extra spaces from.

    Returns:
        The text with extra spaces removed.

    """

    text = text.strip()
    # remove extra spaces
    text = re.sub(" +", " ", text)
    text = re.sub("\n{2,}", "\n\n", text)
    return text


def _remove_page_numbers(text: str) -> str:
    """Removes page numbers from text.

    Args:
        text: The text to remove page numbers from.

    Returns:
        The text with page numbers removed.

    """

    page_number_pattern = re.compile(r"^\s*\d+\s*$|\s*\d+\s*$")
    filtered_lines = [
        line.strip()
        for line in text.splitlines()
        if not page_number_pattern.match(line)
    ]
    return "\n".join(filtered_lines)


# =====================================
# PDF extractor
# =====================================


def _extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        The text from the PDF file.

    """

    pdf_reader = PdfReader(pdf_path)

    pages_text = []
    for page in pdf_reader.pages:
        text = page.extract_text(extraction_mode="layout")
        text = _remove_page_numbers(text)
        text = _remove_extra_spaces(text)
        pages_text.append(text)
    document_text = "\n".join(pages_text)

    return document_text


# =====================================
# Word extractor
# =====================================


def _word_process_paragraph(p) -> str:
    """Get the text from a paragraph.

    Args:
        p (etree._Element): The paragraph element.

    Returns:
        The text from the paragraph.

    """

    return p.text


def _word_process_table(t) -> str:
    """Get the text from a table.

    Args:
        t (etree._Element): The table element.

    Returns:
        The text from the table.

    """

    table_text = []
    for row in t.findall(".//w:tr", WORD_NAMESPACES):
        row_text = []
        for cell in row.findall(".//w:tc", WORD_NAMESPACES):
            cell_text = []
            for p in cell.findall(".//w:p", WORD_NAMESPACES):
                cell_text.append(p.text)
            row_text.append(" ".join(cell_text))
        table_text.append(" ".join(row_text))
    return "\n".join(table_text)


def _extract_text_from_word(doc_path: str) -> str:
    """Extracts text from a Word file.

    Args:
        doc_path: The path to the Word file.

    Returns:
        The text from the Word file.

    """

    doc = Document(doc_path)
    content = []
    for element in doc.element.body:
        if element.tag.endswith("p"):
            # element is a paragraph
            text = _word_process_paragraph(element)
            content.append(text)
        elif element.tag.endswith("tbl"):
            # element is a table
            text = _word_process_table(element)
            content.append(text)
    document_text = "\n".join(content)
    return document_text


# =====================================
# Main functions
# =====================================


def open_file(file_path: str) -> str:
    """Opens a file and returns its content as a string.

    Examples:
        >>> from anonipy.utils import file_system
        >>> file_system.open_file("path/to/file.txt")
        "Hello, World!"

    Args:
        file_path: The path to the file.

    Returns:
        The content of the file as a string.

    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        return _extract_text_from_pdf(file_path)
    elif file_extension.lower() in [".doc", ".docx"]:
        return _extract_text_from_word(file_path)
    elif file_extension.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"The file extension is not supported: {file_extension}")


def write_file(text: str, file_path: str, encode: Union[str, bool] = True) -> None:
    """Writes the text to a file.

    Examples:
        >>> from anonipy.utils import file_system
        >>> file_system.write_file("Hello, World!", "path/to/file.txt")

    Args:
        text: The text to write to the file.
        file_path: The path to the file.
        encode: The encoding to use.

    Raises:
        TypeError: If text, `file_path` is not a string; `encode` is not a string or a boolean.
        FileNotFoundError: If the directory does not exist.

    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    if not isinstance(file_path, str):
        raise TypeError("file_path must be a string")

    if not os.path.exists(os.path.dirname(file_path)):
        raise FileNotFoundError(
            f"The directory does not exist: {os.path.dirname(file_path)}"
        )

    if not isinstance(encode, str) and not isinstance(encode, bool):
        raise TypeError("encode must be a string or a boolean")

    encoding = None
    if isinstance(encode, str):
        encoding = encode
    elif isinstance(encode, bool):
        encoding = "utf-8" if encode else None

    with open(file_path, "w", encoding=encoding) as f:
        f.write(text)


def open_json(file_path: str) -> dict:
    """Opens a JSON file and returns its content as a dictionary.

    Examples:
        >>> from anonipy.utils import file_system
        >>> file_system.open_json("path/to/file.json")
        {"hello": "world"}

    Args:
        file_path: The path to the JSON file.

    Returns:
        The content of the JSON file as a dictionary.

    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data: dict, file_path: str) -> None:
    """Writes data to a JSON file.

    Examples:
        >>> from anonipy.utils import file_system
        >>> file_system.write_json({"hello": "world"}, "path/to/file.json")

    Args:
        data: The data to write to the JSON file.
        file_path: The path to the JSON file.

    """

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
