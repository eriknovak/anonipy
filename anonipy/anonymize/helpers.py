from typing import List
from ..definitions import Entity, Replacement

# =====================================
# Entity converters
# =====================================


def convert_spacy_to_entity(entity, type=None, regex=".*", *args, **kwargs):
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
    s_replacements = sorted(replacements, key=lambda x: x["start_index"], reverse=True)

    anonymized_text = text
    for replacement in s_replacements:
        anonymized_text = (
            anonymized_text[: replacement["start_index"]]
            + replacement["anonymized_text"]
            + anonymized_text[replacement["end_index"] :]
        )
    return anonymized_text, s_replacements[::-1]
