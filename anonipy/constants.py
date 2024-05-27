"""
The constants used to make it easier to use the library
"""

# ================================================
# Constants
# ================================================


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
