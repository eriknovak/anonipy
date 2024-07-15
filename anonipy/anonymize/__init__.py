"""Module containing the anonymization modules and utility.

The `anonymize` module provides a set of anonymization modules and utility,
including `extractors`, `generators`, and `strategies`. In addition, it provides
methods for anonymizing text based on a list of replacements.

Modules:
    extractors: The module containing the extractor classes.
    generators: The module containing the generator classes.
    strategies: The module containing the strategy classes.

Methods:
    anonymize(text, replacements):
        Anonymize the text based on the replacements.

"""

from . import extractors
from . import generators
from . import strategies
from .helpers import anonymize

__all__ = ["extractors", "generators", "strategies", "anonymize"]
