"""
The definitions used within the package
"""

import re
from typing import Union
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
    type: ENTITY_TYPES = None
    regex: Union[str, re.Pattern] = ".*"
