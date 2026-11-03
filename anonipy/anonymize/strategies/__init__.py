"""Module containing the `strategies`.

The `strategies` module provides a set of strategies used to anonymize the
identified vulnerable data.

Classes:
    RedactionStrategy: The class representing the redaction strategy.
    MaskingStrategy: The class representing the masking strategy.
    PseudonymizationStrategy: The class representing the pseudonymization strategy.

"""

from .interface import StrategyInterface
from .masking import MaskingStrategy
from .pseudonymization import PseudonymizationStrategy
from .redaction import RedactionStrategy

__all__ = [
    "StrategyInterface",
    "MaskingStrategy",
    "RedactionStrategy",
    "PseudonymizationStrategy",
]
