"""
anonymize

The module provides a set of anonymization utilities.

Submodules
----------
extractors :
    The module containing the extractor classes
generators :
    The module containing the generator classes
strategies :
    The module containing the strategy classes
regex :
    The module containing the regex patterns

Methods
-------
anonymize()

"""

from . import extractors
from . import generators
from . import strategies
from . import regex
from .helpers import anonymize

__all__ = ["extractors", "generators", "strategies", "regex", "anonymize"]
