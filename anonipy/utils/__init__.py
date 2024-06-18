"""
utils

The module provides a set of utilities used in the library.

Submodules
----------
language_detector :
    The module containing the language detector
file_system :
    The module containing the file system utilities

"""

from . import language_detector
from . import file_system


__all__ = ["language_detector", "file_system"]
