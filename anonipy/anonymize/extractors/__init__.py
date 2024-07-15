"""Module containing the `extractors`.

The `extractors` module provides a set of extractors used to identify relevant
information within a document.

Classes:
    NERExtractor: The class representing the named entity recognition (NER) extractor.
    PatternExtractor: The class representing the pattern extractor.
    MultiExtractor: The class representing the multi extractor.

"""

from .interface import ExtractorInterface
from .multi_extractor import MultiExtractor
from .ner_extractor import NERExtractor
from .pattern_extractor import PatternExtractor


__all__ = ["ExtractorInterface", "MultiExtractor", "NERExtractor", "PatternExtractor"]
