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


def open_file(file_path: str, decode: Union[str, bool] = True) -> str:
    text = textract.process(file_path)
    text = text_decode(text, decode)
    return text
