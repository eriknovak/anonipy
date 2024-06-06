"""
Contains the redaction strategy
"""

from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class RedactionStrategy(StrategyInterface):

    def __init__(self, substitute_label: str = "[REDACTED]", *args, **kwargs) -> None:
        self.substitute_label = substitute_label

    def anonymize(
        self, text: str, entities: List[Entity], *args, **kwargs
    ) -> Tuple[str, List[Replacement]]:
        replacements = [self._create_replacement(ent) for ent in entities]
        anonymized_text, replacements = anonymize(text, replacements)
        return anonymized_text, replacements

    def _create_replacement(self, entity: Entity) -> Replacement:
        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": self.substitute_label,
        }
