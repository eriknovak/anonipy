"""
Contains the pseudonymization strategy
"""

from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class PseudonymizationStrategy(StrategyInterface):
    """The class representing the pseudonymization strategy

    Attributes
    ----------
    mapping : dict
        The mapping of entities to pseudonyms

    Methods
    -------
    anonymize(text: str, entities: List[Entity])
        Anonymize the text based on the entities

    """

    def __init__(self, mapping, *args, **kwargs):
        """
        Parameters
        ----------
        mapping : func
            The mapping of entities to pseudonyms

        """

        super().__init__(*args, **kwargs)
        self.mapping = mapping

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

        replacements = []
        for ent in entities:
            replacement = self._create_replacement(ent, text, replacements)
            replacements.append(replacement)
        anonymized_text, replacements = anonymize(text, replacements)
        return anonymized_text, replacements

    def _create_replacement(
        self, entity: Entity, text: str, replacements: List[dict]
    ) -> Replacement:
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

    def _check_replacement(self, entity: Entity, replacements: List[dict]) -> str:
        existing_replacement = list(
            filter(lambda x: x["original_text"] == entity.text, replacements)
        )
        return (
            existing_replacement[0]["anonymized_text"]
            if len(existing_replacement) > 0
            else None
        )
