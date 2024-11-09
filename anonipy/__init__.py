"""`Anonipy` is a text anonymization package.

The `anonipy` package provides utilities for data anonymization. It provides
a set of modules and utilities for (1) identifying relevant information
that needs to be anonymized, (2) generating substitutes for the identified
information, and (3) strategies for anonymizing the identified information.

Modules:
    anonymize: The module containing the anonymization submodules and utility.
    utils: The module containing utility classes and functions.
    definitions: The module containing predefined types used across the package.
    constants: The module containing the predefined constants used across the package.

"""

__version__ = "0.2.0"

from . import anonymize
from . import utils
from . import definitions
from . import constants
