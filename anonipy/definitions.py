"""
The definitions used within the package
"""

import re
from typing import Union, TypedDict
from typing_extensions import NotRequired
from dataclasses import dataclass

from .constants import ENTITY_TYPES

# ================================================
# Entity Definitions
# ================================================


@dataclass
class Entity:
    text: str
    label: str
    start_index: int
    end_index: int
    score: float = 1.0
    type: ENTITY_TYPES = None
    regex: Union[str, re.Pattern] = ".*"


class Replacement(TypedDict):
    original_text: NotRequired[str]
    label: NotRequired[str]
    start_index: int
    end_index: int
    anonymized_text: str
