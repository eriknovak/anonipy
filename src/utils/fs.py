from typing import Union

import pypdf


def open_file(file_path: str) -> Union[str, pypdf.PdfReader]:
    if file_path.endswith(".pdf"):
        pdf = pypdf.PdfReader(file_path)
        return pdf
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def get_file_text(f: Union[str, pypdf.PdfReader]) -> str:
    if isinstance(f, pypdf.PdfReader):
        texts = [page.extract_text() for page in f.pages]
        return "\n".join(texts)
    return f
