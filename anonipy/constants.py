"""
constants

The module provides a set of constants used in the library.

Classes
-------
LANGUAGES :
    Predefined supported languages
ENTITY_TYPES :
    Predefined types of entities

"""


class LANGUAGES:
    """Supported languages"""

    DUTCH = ("nl", "Dutch")
    ENGLISH = ("en", "English")
    FRENCH = ("fr", "French")
    GERMAN = ("de", "German")
    GREEK = ("el", "Greek")
    ITALIAN = ("it", "Italian")
    SLOVENE = ("sl", "Slovene")
    SPANISH = ("es", "Spanish")
    UKRAINIAN = ("uk", "Ukrainian")


class ENTITY_TYPES:
    """Types of entities"""

    CUSTOM = "custom"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    EMAIL = "email"
    WEBSITE_URL = "website_url"
    PHONE_NUMBER = "phone_number"
