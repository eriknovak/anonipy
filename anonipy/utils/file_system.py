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
    text = text.strip()
    # remove extra spaces
    text = re.sub(" +", " ", text)
    text = re.sub("\n{2,}", "\n\n", text)
    return text


def remove_page_numbers(text: str) -> str:
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
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_file(text: str, file_path: str, encode: Union[str, bool] = True) -> None:
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
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
