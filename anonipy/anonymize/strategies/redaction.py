"""
Contains the redaction strategy
"""

from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement


# =====================================
# Main class
# =====================================


class RedactionStrategy(StrategyInterface):

    def __init__(self, substitute_label: str = "[REDACTED]", *args, **kwargs) -> None:
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
        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": self.substitute_label,
        }
