"""
Contains the masking strategy
"""

import re
from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class MaskingStrategy(StrategyInterface):
    """The class representing the masking strategy

    Attributes
    ----------
    substitute_label : str
        The label to substitute in the anonymized text

    Methods
    -------
    anonymize(text: str, entities: List[Entity])
        Anonymize the text based on the entities

    """

    def __init__(self, substitute_label: str = "*", *args, **kwargs):
        """
        Parameters
        ----------
        substitute_label : str, optional
            The label to substitute in the anonymized text. Default: "*"

        """

        super().__init__(*args, **kwargs)
        self.substitute_label = substitute_label

    def anonymize(
        self, text: str, entities: List[Entity], *args, **kwargs
    ) -> Tuple[str, List[Replacement]]:
        """Anonymize the text based on the entities

        Parameters
        ----------
        text : str
            The text to anonymize
        entities : List[Entity]
            The list of entities to anonymize

        Returns
        -------
        Tuple[str, List[Replacement]]
            The anonymized text and the list of replacements applied

        """

        replacements = [self._create_replacement(ent) for ent in entities]
        anonymized_text, replacements = anonymize(text, replacements)
        return anonymized_text, replacements

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
