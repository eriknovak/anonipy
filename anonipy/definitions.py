"""Module containing the `definitions`.

The `definitions` module provides a set of predefined types used in the package.

Classes:
    Entity: The class representing the anonipy entity object.
    Replacement: The class representing the anonipy replacement object.

"""

import re
from typing import Union, TypedDict
from typing_extensions import NotRequired
from dataclasses import dataclass

from .utils.regex import regex_mapping
from .constants import ENTITY_TYPES

# ================================================
# Entity Definitions
# ================================================


@dataclass
class Entity:
    """The class representing the anonipy Entity object.

    Attributes:
        text (str): The text of the entity.
        label (str): The label of the entity.
        start_index (int): The start index of the entity in the text.
        end_index (int): The end index of the entity in the text.
        score (float): The prediction score of the entity. The score is returned by the extractor models.
        type (ENTITY_TYPES): The type of the entity.
        regex (Union[str, re.Pattern]): The regular expression the entity must match.

    """

    text: str
    label: str
    start_index: int
    end_index: int
    score: float = 1.0
    type: ENTITY_TYPES = None
    regex: Union[str, re.Pattern] = None

    def __post_init__(self):
        if self.regex is None:
            if self.type == "custom":
                raise ValueError("Custom entities require a regex.")
            self.regex = regex_mapping[self.type]

    def get_regex_group(self) -> Union[str, None]:
        """Get the regex group.

        Returns:
            The regex group.

        """

        p_match = re.match(r"^.*?\((.*)\).*$", self.regex)
        return p_match.group(1) if p_match else self.regex


class Replacement(TypedDict):
    """The class representing the anonipy Replacement object.

    Attributes:
        original_text (str): The original text of the entity.
        label (str): The label of the entity.
        start_index (int): The start index of the entity in the text.
        end_index (int): The end index of the entity in the text.
        anonymized_text (str): The anonymized text replacing the original.

    """

    original_text: NotRequired[str]
    label: NotRequired[str]
    start_index: int
    end_index: int
    anonymized_text: str
