"""
The file system utilities
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


def remove_extra_spaces(text: str) -> str:
    """Remove extra spaces from text

    Parameters
    ----------
    text : str
        The text to remove extra spaces from

    Returns
    -------
    str
        The text with extra spaces removed

    """
    text = text.strip()
    # remove extra spaces
    text = re.sub(" +", " ", text)
    text = re.sub("\n{2,}", "\n\n", text)
    return text


def remove_page_numbers(text: str) -> str:
    """Removes page numbers from text

    Parameters
    ----------
    text : str
        The text to remove page numbers from

    Returns
    -------
    str
        The text with page numbers removed

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


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extracts text from a PDF file

    Parameters
    ----------
    pdf_path : str
        The path to the PDF file

    Returns
    -------
    str
        The text from the PDF file

    """

    pdf_reader = PdfReader(pdf_path)

    pages_text = []
    for page in pdf_reader.pages:
        text = page.extract_text(extraction_mode="layout")
        text = remove_page_numbers(text)
        text = remove_extra_spaces(text)
        pages_text.append(text)
    document_text = "\n".join(pages_text)

    return document_text


# =====================================
# Word extractor
# =====================================


def _word_process_paragraph(p) -> str:
    return p.text


def _word_process_table(t) -> str:
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


def extract_text_from_word(doc_path: str) -> str:
    """Extracts text from a Word file

    Parameters
    ----------
    doc_path : str
        The path to the Word file

    Returns
    -------
    str
        The text from the Word file

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
    """
    Opens a file and returns its content as a string

    Parameters
    ----------
    file_path : str
        The path to the file

    Returns
    -------
    str
        The content of the file as a string

    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_extension.lower() in [".doc", ".docx"]:
        return extract_text_from_word(file_path)
    elif file_extension.lower() == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError(f"The file extension is not supported: {file_extension}")


def open_json(file_path: str) -> dict:
    """
    Opens a JSON file and returns its content as a dictionary

    Parameters
    ----------
    file_path : str
        The path to the JSON file

    Returns
    -------
    dict
        The content of the JSON file as a dictionary

    """

    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file does not exist: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_file(text: str, file_path: str, encode: Union[str, bool] = True) -> None:
    """Writes text to a file

    Parameters
    ----------
    text : str
        The text to write to the file
    file_path : str
        The path to the file
    encode : Union[str, bool], optional
        The encoding to use. Default: True

    Raises
    ------
    TypeError
        If text, file_path is not a string; encode is not a string or a boolean
    FileNotFoundError
        If the directory does not exist

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


def write_json(data: dict, file_path: str) -> None:
    """Writes data to a JSON file

    Parameters
    ----------
    data : dict
        The data to write to the JSON file
    file_path : str
        The path to the JSON file

    """

    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
