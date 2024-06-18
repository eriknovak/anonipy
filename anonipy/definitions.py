"""
definitions

The module provides a set of object definitions used in the library.

Classes
-------
Entity :
    The class representing the entity
Replacement :
    The class representing the replacement

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
    """The class representing the entity

    Attributes
    ----------
    text : str
        The text of the entity
    label : str
        The label of the entity
    start_index : int
        The start index of the entity in the text
    end_index : int
        The end index of the entity in the text
    score : float
        The prediction score of the entity. The score is returned by the extractor models. Default: 1.0
    type : ENTITY_TYPES
        The type of the entity. Default: None
    regex : Union[str, re.Pattern]
        The regular expression the entity must match. Default: ".*"

    """

    text: str
    label: str
    start_index: int
    end_index: int
    score: float = 1.0
    type: ENTITY_TYPES = None
    regex: Union[str, re.Pattern] = ".*"


class Replacement(TypedDict):
    """The class representing the replacement

    Attributes
    ----------
    original_text : str, optional
        The original text of the entity
    label : str, optional
        The label of the entity
    start_index : int
        The start index of the entity in the text
    end_index : int
        The end index of the entity in the text
    anonymized_text : str
        The anonymized text replacing the original

    """

    original_text: NotRequired[str]
    label: NotRequired[str]
    start_index: int
    end_index: int
    anonymized_text: str
