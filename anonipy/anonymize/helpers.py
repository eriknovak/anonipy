from typing import List
from ..definitions import Entity, Replacement

# =====================================
# Entity converters
# =====================================


def convert_spacy_to_entity(entity, type=None, regex=".*", *args, **kwargs):
    """Convert a SpaCy entity to an Entity object

    Parameters
    ----------
    entity : SpaCy Span
        The SpaCy entity to convert
    type : ENTITY_TYPES, optional
        The type of the entity. Default: None
    regex : Union[str, re.Pattern], optional
        The regular expression the entity must match. Default: ".*"

    Returns
    -------
    Entity
        The converted Entity object

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


def anonymize(text: str, replacements: List[Replacement]) -> str:
    """Anonymize a text based on a list of replacements

    Parameters
    ----------
    text : str
        The text to anonymize
    replacements : List[Replacement]
        The list of replacements to apply

    Returns
    -------
    Tuple[str, List[Replacement]]
        The anonymized text and the list of replacements applied

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
