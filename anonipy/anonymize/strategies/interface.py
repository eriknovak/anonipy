"""
Contains the interface for the strategy
"""

from typing import List
from ...definitions import Entity, Replacement

# =====================================
# Main class
# =====================================


class StrategyInterface:

    def __init__(self, *args, **kwargs):
        pass

    def anonymize(self, text: str, entities: List[Entity], *args, **kwargs):
        pass

    def refinement(
        self, text: str, replacements: List[Replacement], *args, **kwargs
    ) -> str:
        s_replacements = sorted(
            replacements, key=lambda x: x["start_index"], reverse=True
        )
        refined_text = text
        for replacement in s_replacements:
            refined_text = (
                refined_text[: replacement["start_index"]]
                + replacement["anonymized_text"]
                + refined_text[replacement["end_index"] :]
            )
        return refined_text
