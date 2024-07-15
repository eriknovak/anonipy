import re
from typing import List, Tuple

from .interface import StrategyInterface
from ...definitions import Entity, Replacement
from ..helpers import anonymize

# =====================================
# Main class
# =====================================


class MaskingStrategy(StrategyInterface):
    """The class representing the masking strategy.

    Examples:
        >>> from anonipy.anonymize.strategies import MaskingStrategy
        >>> strategy = MaskingStrategy()
        >>> strategy.anonymize(text, entities)

    Attributes:
        substitute_label (str): The label to substitute in the anonymized text.

    Methods:
        anonymize(text, entities):
            Anonymize the text based on the entities.

    """

    def __init__(self, substitute_label: str = "*", *args, **kwargs):
        """Initializes the masking strategy.

        Examples:
            >>> from anonipy.anonymize.strategies import MaskingStrategy
            >>> strategy = MaskingStrategy()

        Args:
            substitute_label: The label to substitute in the anonymized text.

        """

        super().__init__(*args, **kwargs)
        self.substitute_label = substitute_label

    def anonymize(
        self, text: str, entities: List[Entity], *args, **kwargs
    ) -> Tuple[str, List[Replacement]]:
        """Anonymize the text using the masking strategy.

        Examples:
            >>> from anonipy.anonymize.strategies import MaskingStrategy
            >>> strategy = MaskingStrategy()
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

        mask = self._create_mask(entity)
        return {
            "original_text": entity.text,
            "label": entity.label,
            "start_index": entity.start_index,
            "end_index": entity.end_index,
            "anonymized_text": mask,
        }

    def _create_mask(self, entity: Entity) -> str:
        """Creates a mask for the entity.

        Args:
            entity: The entity to create the mask for.

        Returns:
            The created mask.

        """

        # TODO: add random length substitution
        return " ".join(
            [
                self.substitute_label * len(chunk)
                for chunk in re.split(r"\s+", entity.text)
            ]
        )
