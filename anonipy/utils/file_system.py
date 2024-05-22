"""
The file system utilities
"""

from typing import Union, Any

import textract

# =====================================
# Helper functions
# =====================================


def text_decode(text: str, decode: Union[str, bool] = True) -> str:
    if not decode:
        return text
    if isinstance(decode, str):
        return text.decode(decode)
    if isinstance(decode, bool):
        return text.decode("utf-8")


def get_variable_name(var: Any) -> str:
    for name, value in globals().items():
        if value is var:
            return name
    return None


# =====================================
# Main functions
# =====================================


def open_file(file_path: str, encode: Union[str, bool] = True) -> str:
    text = textract.process(file_path)
    text = text_decode(text, encode)
    return text


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
