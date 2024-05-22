"""
Contains the pseudonymization strategy
"""

from typing import List

from .interface import StrategyInterface
from ...definitions import Entity


# =====================================
# Main class
# =====================================


class PseudonymizationStrategy(StrategyInterface):

    def __init__(self, mapping, *args, **kwargs):
        self.mapping = mapping

    def anonymize(self, text: str, entities: List[Entity], *args, **kwargs):
        replacements = []
        for ent in entities[::-1]:
            r = self._create_replacement(text, ent, replacements)
            text = (
                text[: r["start_index"]] + r["anonymized_text"] + text[r["end_index"] :]
            )
            replacements.append(r)
        return text, replacements[::-1]

    def _create_replacement(self, text: str, entity: Entity, replacements: List[dict]):
        # check if the replacement already exists
        anonymized_text = self._check_replacement(entity, replacements)
        # create a new replacement if it doesn't exist
        anonymized_text = (
            self.mapping(text, entity) if not anonymized_text else anonymized_text
        )
        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": anonymized_text,
        }

    def _check_replacement(self, entity: Entity, replacements: List[dict]):
        existing_replacement = list(
            filter(lambda x: x["original_text"] == entity.text, replacements)
        )
        return (
            existing_replacement[0]["anonymized_text"]
            if len(existing_replacement) > 0
            else None
        )
