"""
anonipy

The anonipy package provides utilities for data anonymization.

Submodules
----------
anonymize :
    The package containing anonymization classes and functions.
utils :
    The package containing utility classes and functions.
definitions :
    The object definitions used within the package.
constants :
    The constant values used to help with data anonymization.


How to use the documentation
----------------------------
Documentation is available in two forms: docstrings provided
with the code and a loose standing reference guide, available
from `the anonipy homepage <https://eriknovak.github.io/anonipy>`.

"""

__version__ = "0.0.8"

from . import anonymize
from . import utils
from . import definitions
from . import constants
