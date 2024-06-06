"""
Contains the masking strategy
"""

import re
from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement


# =====================================
# Main class
# =====================================


class MaskingStrategy(StrategyInterface):

    def __init__(self, substitute_label: str = "*", *args, **kwargs):
        self.substitute_label = substitute_label

    def anonymize(
        self, text: str, entities: List[Entity], *args, **kwargs
    ) -> Tuple[str, List[Replacement]]:
        s_entities = sorted(entities, key=lambda x: x.start_index, reverse=True)

        replacements = []
        for ent in s_entities:
            r = self._create_replacement(ent)
            text = (
                text[: r["start_index"]] + r["anonymized_text"] + text[r["end_index"] :]
            )
            replacements.append(r)
        return text, replacements[::-1]

    def _create_replacement(self, entity: Entity) -> Replacement:
        mask = self._create_mask(entity)
        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": mask,
        }

    def _create_mask(self, entity: Entity) -> str:
        return " ".join(
            [
                self.substitute_label * len(chunk)
                for chunk in re.split(r"\s+", entity.text)
            ]
        )
