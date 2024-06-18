from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class RedactionStrategy(StrategyInterface):
    """The class representing the redaction strategy

    Attributes
    ----------
    substitute_label : str
        The label to substitute in the anonymized text

    Methods
    -------
    anonymize(text: str, entities: List[Entity])
        Anonymize the text based on the entities

    """

    def __init__(self, substitute_label: str = "[REDACTED]", *args, **kwargs) -> None:
        """
        Parameters
        ----------
        substitute_label : str, optional
            The label to substitute in the anonymized text. Default: "[REDACTED]"

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
        """Creates a replacement for the entity

        Parameters
        ----------
        entity : Entity
            The entity to create the replacement for

        Returns
        -------
        Replacement
            The replacement for the entity

        """

        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": self.substitute_label,
        }
