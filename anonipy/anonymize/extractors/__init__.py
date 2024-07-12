"""
extractors

The module provides a set of extractors used in the library.

Classes
-------
ExtractorInterface :
    The class representing the extractor interface
NERExtractor :
    The class representing the named entitiy recognition (NER) extractor
RegexExtractor :
    The class representing the regex extractor

"""

from .interface import ExtractorInterface
from .multi_extractor import MultiExtractor
from .ner_extractor import NERExtractor
from .pattern_extractor import PatternExtractor


__all__ = ["ExtractorInterface", "MultiExtractor", "NERExtractor", "PatternExtractor"]
