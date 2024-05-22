"""
Contains the redaction strategy
"""

from typing import List

from .interface import StrategyInterface
from ...definitions import Entity


# =====================================
# Main class
# =====================================


class RedactionStrategy(StrategyInterface):

    def __init__(self, substitute_label: str = "[REDACTED]", *args, **kwargs):
        self.substitute_label = substitute_label

    def anonymize(self, text: str, entities: List[Entity], *args, **kwargs):
        replacements = []
        for ent in entities[::-1]:
            r = self._create_replacement(ent)
            text = (
                text[: r["start_index"]] + r["anonymized_text"] + text[r["end_index"] :]
            )
            replacements.append(r)
        return text, replacements[::-1]

    def _create_replacement(self, entity: Entity):
        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": self.substitute_label,
        }
