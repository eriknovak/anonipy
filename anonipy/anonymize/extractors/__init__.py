"""
extractors

The module provides a set of extractors used in the library.

Classes
-------
ExtractorInterface :
    The class representing the extractor interface
EntityExtractor :
    The class representing the entity extractor

"""

from .interface import ExtractorInterface
from .entity_extractor import EntityExtractor

__all__ = ["ExtractorInterface", "EntityExtractor"]
