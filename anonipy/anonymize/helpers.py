import re
from typing import List, Union

from spacy.tokens import Span

from ..definitions import Entity, Replacement
from ..constants import ENTITY_TYPES

# =====================================
# Entity converters
# =====================================


def convert_spacy_to_entity(
    entity: Span,
    type: ENTITY_TYPES = None,
    regex: Union[str, re.Pattern] = None,
    *args,
    **kwargs,
) -> Entity:
    """Convert a spacy entity to an anonipy entity object.

    Args:
        entity: The spacy Span representing the entity to convert.
        type: The type of the entity.
        regex: The regular expression the entity must match.

    Returns:
        The converted anonipy entity object.

    """

    return Entity(
        entity.text,
        entity.label_,
        entity.start_char,
        entity.end_char,
        entity._.score,
        type,
        regex,
    )


# =====================================
# Anonymization function
# =====================================


def anonymize(text: str, replacements: List[Replacement]) -> str:
    """Anonymize a text based on a list of replacements.

    Examples:
        >>> from anonipy.anonymize import anonymize
        >>> anonymize(text, replacements)

    Args:
        text: The text to anonymize.
        replacements: The list of replacements to apply.

    Returns:
        The anonymized text.

    """

    s_replacements = sorted(replacements, key=lambda x: x["start_index"], reverse=True)

    anonymized_text = text
    for replacement in s_replacements:
        anonymized_text = (
            anonymized_text[: replacement["start_index"]]
            + replacement["anonymized_text"]
            + anonymized_text[replacement["end_index"] :]
        )
    return anonymized_text, s_replacements[::-1]
