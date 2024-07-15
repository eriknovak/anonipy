from typing import List, Tuple, Callable

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class PseudonymizationStrategy(StrategyInterface):
    """The class representing the pseudonymization strategy.

    Examples:
        >>> from anonipy.anonymize.strategies import PseudonymizationStrategy
        >>> strategy = PseudonymizationStrategy(mapping)
        >>> strategy.anonymize(text, entities)

    Attributes:
        mapping: The mapping of entities to pseudonyms.

    Methods:
        anonymize(text, entities):
            Anonymize the text based on the entities.

    """

    def __init__(self, mapping: Callable, *args, **kwargs):
        """Initializes the pseudonymization strategy.

        Examples:
            >>> from anonipy.anonymize.strategies import PseudonymizationStrategy
            >>> strategy = PseudonymizationStrategy(mapping)

        Args:
            mapping: The mapping function on how to handle each entity type.

        """

        super().__init__(*args, **kwargs)
        self.mapping = mapping

    def anonymize(
        self, text: str, entities: List[Entity], *args, **kwargs
    ) -> Tuple[str, List[Replacement]]:
        """Anonymize the text using the pseudonymization strategy.

        Examples:
            >>> from anonipy.anonymize.strategies import PseudonymizationStrategy
            >>> strategy = PseudonymizationStrategy(mapping)
            >>> strategy.anonymize(text, entities)

        Args:
            text: The text to anonymize.
            entities: The list of entities to anonymize.

        Returns:
            The anonymized text.
            The list of applied replacements.

        """

        replacements = []
        for ent in entities:
            replacement = self._create_replacement(ent, text, replacements)
            replacements.append(replacement)
        anonymized_text, replacements = anonymize(text, replacements)
        return anonymized_text, replacements

    # ===========================================
    # Private methods
    # ===========================================

    def _create_replacement(
        self, entity: Entity, text: str, replacements: List[dict]
    ) -> Replacement:
        """Creates a replacement for the entity.

        Args:
            entity: The entity to create the replacement for.
            text: The text to anonymize.
            replacements: The list of existing replacements.

        Returns:
            The created replacement.

        """

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

    def _check_replacement(
        self, entity: Entity, replacements: List[Replacement]
    ) -> str:
        """Checks if a suitable replacement already exists.

        Args:
            entity: The entity to check.
            replacements: The list of replacements.

        Returns:
            The anonymized text if the replacement already exists, None otherwise.

        """
        existing_replacement = list(
            filter(lambda x: x["original_text"] == entity.text, replacements)
        )
        return (
            existing_replacement[0]["anonymized_text"]
            if len(existing_replacement) > 0
            else None
        )
