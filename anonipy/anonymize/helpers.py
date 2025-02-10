import re
from typing import List, Union, Tuple, Iterable, Set
import itertools

from spacy import util
from spacy.tokens import Span, Doc

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


# =====================================
# Entity helpers
# =====================================


def merge_entities(extractor_outputs: List[Tuple[Doc, List[Entity]]]) -> List[Entity]:
    """Merges the entities returned by the extractors.

    Args:
        extractor_outputs: The list of extractor outputs.

    Returns:
        The merged entities list.

    """

    if len(extractor_outputs) == 0:
        return []
    if len(extractor_outputs) == 1:
        return extractor_outputs[0][1]

    joint_entities = filter_entities(
        list(itertools.chain.from_iterable([entity[1] for entity in extractor_outputs]))
    )
    return joint_entities


def filter_entities(entities: Iterable[Entity]) -> List[Entity]:
    """Filters the entities based on their start and end indices.

    Args:
        entities: The entities to filter.

    Returns:
        The filtered entities.

    """

    def get_sort_key(entity):
        return (
            entity.end_index - entity.start_index,
            -entity.start_index,
        )

    sorted_entities = sorted(entities, key=get_sort_key, reverse=True)
    result = []
    seen_tokens: Set[int] = set()
    for entity in sorted_entities:
        # Check for end - 1 here because boundaries are inclusive
        if (
            entity.start_index not in seen_tokens
            and entity.end_index - 1 not in seen_tokens
        ):
            result.append(entity)
            seen_tokens.update(range(entity.start_index, entity.end_index))
    result = sorted(result, key=lambda entity: entity.start_index)
    return result


def detect_repeated_entities(
    doc: Doc, entities: List[Entity], spacy_style: str
) -> List[Entity]:
    """Detects repeated entities in the text.

    Args:
        doc: The spacy doc to detect entities in.
        entities: The entities to detect.
        spacy_style: The style the entities should be stored in the spacy doc.

    Returns:
        The list of all entities.

    """

    repeated_entities = []

    for entity in entities:
        matches = re.finditer(re.escape(entity.text), doc.text)
        for match in matches:
            start_index, end_index = match.start(), match.end()
            if start_index == entity.start_index and end_index == entity.end_index:
                continue
            repeated_entities.append(
                Entity(
                    text=entity.text,
                    label=entity.label,
                    start_index=start_index,
                    end_index=end_index,
                    score=entity.score,
                    type=entity.type,
                    regex=entity.regex,
                )
            )

    filtered_entities = filter_entities(entities + repeated_entities)
    final_entities = sorted(filtered_entities, key=lambda e: e.start_index)

    return final_entities


# ====================================
# Spacy helpers
# ====================================


def create_spacy_entities(doc: Doc, entities: List[Entity], spacy_style: str) -> None:
    """Create spacy entities in the spacy doc.

    Args:
        doc: The spacy doc to create entities in.
        entities: The entities to create.
        spacy_style: The style the entities should be stored in the spacy doc.

    """

    updated_spans = get_doc_entity_spans(doc, spacy_style)

    for entity in entities:
        span = doc.char_span(entity.start_index, entity.end_index, label=entity.label)
        if not span or span in updated_spans:
            continue
        span._.score = entity.score
        if spacy_style == "ent":
            updated_spans = util.filter_spans(updated_spans + (span,))
        elif spacy_style == "span":
            updated_spans.append(span)
        else:
            raise ValueError(f"Invalid spacy style: {spacy_style}")

    set_doc_entity_spans(doc, updated_spans, spacy_style)


def get_doc_entity_spans(doc: Doc, spacy_style: str) -> List[Span]:
    """Get the spacy doc entity spans.

    Args:
        doc: The spacy doc to get the entity spans from.
        spacy_style: The spacy style to use.

    Returns:
        The list of entity spans.

    """

    if spacy_style == "ent":
        return doc.ents
    if spacy_style == "span":
        if "sc" not in doc.spans:
            doc.spans["sc"] = []
        return doc.spans["sc"]
    raise ValueError(f"Invalid spacy style: {spacy_style}")


def set_doc_entity_spans(doc: Doc, entities: List[Span], spacy_style: str) -> None:
    """Set the spacy doc entity spans.

    Args:
        doc: The spacy doc to set the entity spans.
        entities: The entity spans to assign the doc.
        spacy_style: The spacy style to use.

    """

    if spacy_style == "ent":
        doc.ents = entities
    elif spacy_style == "span":
        doc.spans["sc"] = entities
    else:
        raise ValueError(f"Invalid spacy style: {spacy_style}")
