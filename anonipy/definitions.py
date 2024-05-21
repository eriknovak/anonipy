"""
The definitions used within the package
"""

from dataclasses import dataclass


# ================================================
# Entity Definitions
# ================================================


@dataclass
class Entity:
    text: str
    label: str
    start_index: str
    end_index: str
    type: str = None
    regex: str = ".*"
