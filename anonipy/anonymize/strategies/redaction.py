from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class RedactionStrategy(StrategyInterface):
    """The class representing the redaction strategy.

    Examples:
        >>> from anonipy.anonymize.strategies import RedactionStrategy
        >>> strategy = RedactionStrategy()
        >>> strategy.anonymize(text, entities)

    Attributes:
        substitute_label (str): The label to substitute in the anonymized text.

    Methods:
        anonymize(text, entities):
            Anonymize the text based on the entities.

    """

    def __init__(self, substitute_label: str = "[REDACTED]", *args, **kwargs) -> None:
        """Initializes the redaction strategy.

        Examples:
            >>> from anonipy.anonymize.strategies import RedactionStrategy
            >>> strategy = RedactionStrategy()

        Args:
            substitute_label: The label to substitute in the anonymized text.

        """

        super().__init__(*args, **kwargs)
        self.substitute_label = substitute_label

    def anonymize(
        self, text: str, entities: List[Entity], *args, **kwargs
    ) -> Tuple[str, List[Replacement]]:
        """Anonymize the text using the redaction strategy.

        Examples:
            >>> from anonipy.anonymize.strategies import RedactionStrategy
            >>> strategy = RedactionStrategy()
            >>> strategy.anonymize(text, entities)

        Args:
            text: The text to anonymize.
            entities: The list of entities to anonymize.

        Returns:
            The anonymized text.
            The list of applied replacements.

        """

        replacements = [self._create_replacement(ent) for ent in entities]
        anonymized_text, replacements = anonymize(text, replacements)
        return anonymized_text, replacements

    # ===========================================
    # Private methods
    # ===========================================

    def _create_replacement(self, entity: Entity) -> Replacement:
        """Creates a replacement for the entity.

        Args:
            entity: The entity to create the replacement for.

        Returns:
            The created replacement.

        """

        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": self.substitute_label,
        }
