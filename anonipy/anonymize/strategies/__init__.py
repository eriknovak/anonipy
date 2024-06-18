"""
strategies

The module provides a set of strategies used in the library.

Classes
-------
StrategyInterface :
    The class representing the strategy interface
MaskingStrategy :
    The class representing the masking strategy
RedactionStrategy :
    The class representing the redaction strategy
PseudonymizationStrategy :
    The class representing the pseudonymization strategy

"""

from .interface import StrategyInterface
from .masking import MaskingStrategy
from .redaction import RedactionStrategy
from .pseudonymization import PseudonymizationStrategy


__all__ = [
    "StrategyInterface",
    "MaskingStrategy",
    "RedactionStrategy",
    "PseudonymizationStrategy",
]
