"""Module containing the `regex` related utilities.

The `regex` module provides the regex definitions and functions used within the package.

Classes:
    RegexMapping: The class representing the mapping for data type to the corresponding regex.

Attributes:
    REGEX_STRING (str): The regex definition for string.
    REGEX_INTEGER (str): The regex definition for integer.
    REGEX_FLOAT (str): The regex definition for float.
    REGEX_DATE (str): The regex definition for date.
    REGEX_EMAIL_ADDRESS (str): The regex definition for email address.
    REGEX_PHONE_NUMBER (str): The regex definition for phone number.
    REGEX_WEBSITE_URL (str): The regex definition for website URL.

"""

from collections import defaultdict

from ..constants import ENTITY_TYPES


# =====================================
# Regex definitions
# =====================================

REGEX_STRING = ".*"
"""The regex definition for string."""

REGEX_INTEGER = "\d+"
"""The regex definition for integer."""

REGEX_FLOAT = "[\d\.,]+"
"""The regex definition for float."""

REGEX_DATE = (
    r"("
    r"(\d{4}[-/.\s]\d{2}[-/.\s]\d{2}[ T]\d{2}:\d{2}:\d{2})|"
    r"(\d{2}[-/.\s]\d{2}[-/.\s]\d{4}[ T]\d{2}:\d{2}:\d{2})|"
    r"(\d{2}[-/.\s]\d{2}[-/.\s]\d{4}[ T]\d{2}:\d{2})|"
    r"(\d{4}[-/.\s]\d{2}[-/.\s]\d{2}[ T]\d{2}:\d{2})|"
    r"(\d{4}[-/.\s]\d{2}[-/.\s]\d{2}[ T]\d{2}:\d{2} [APap][mM])|"
    r"(\d{2}[-/.\s]\d{2}[-/.\s]\d{4}[ T]\d{2}:\d{2} [APap][mM])|"
    r"(\d{4}[-/.\s]\d{2}[-/.\s]\d{2})|"
    r"(\d{2}[-/.\s]\d{2}[-/.\s]\d{4})|"
    r"(\d{2}[-/.\s]\d{2}[-/.\s]\d{4}[ ]?\d{2}:\d{2}:\d{2})|"
    r"(\d{4}[-/.\s]\d{2}[-/.\s]\d{2}[ ]?\d{2}:\d{2}:\d{2})|"
    r"(\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4}[ ]?\d{2}:\d{2}:\d{2})|"
    r"(\d{1,2}[ ](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ ]\d{4}[ ]?\d{2}:\d{2}:\d{2})|"
    r"(\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4}[ ]?\d{2}:\d{2}[ ]?[APap][mM])|"
    r"(\d{1,2}[ ](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ ]\d{4}[ ]?\d{2}:\d{2}[ ]?[APap][mM])|"
    r"([A-Za-z]+,[ ]\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4}[ ]?\d{2}:\d{2}:\d{2})|"
    r"([A-Za-z]+,[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{1,2},[ ]\d{4}[ ]?\d{2}:\d{2}:\d{2})|"
    r"([A-Za-z]+,[ ]\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4}[ ]?\d{2}:\d{2}[ ]?[APap][mM])|"
    r"([A-Za-z]+,[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{1,2},[ ]\d{4}[ ]?\d{2}:\d{2}[ ]?[APap][mM])"
    r")"
)
"""The regex definition for dates.

The regex definition for dates includes string representations, which are currently in
the English language.

TODO:
    - Add regex definitions for other languages.
"""

REGEX_EMAIL_ADDRESS = (
    "[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*"
)
"""The regex definition for email addresses."""

REGEX_PHONE_NUMBER = (
    "[(]?[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?([0-9]{2,}[-\s\.]?){2,}([0-9]{3,})"
)
"""The regex definition for phone numbers."""

REGEX_WEBSITE_URL = "((https?|ftp|smtp):\/\/)?(www.)?([a-zA-Z0-9]+\.)+[a-z]{2,}(\/[a-zA-Z0-9#\?\_\.\=\-\&]+|\/?)*"
"""The regex definition for website URLs."""


# =====================================
# Define the regex definitions
# =====================================


class RegexMapping:
    """The class representing the regex mapping.

    Examples:
        >>> from anonipy.anonymize.regex import regex_mapping
        >>> regex_mapping["string"]
        ".*"

    Attributes:
        regex_mapping (defaultdict):
            The mapping between the data type and the corresponding regex.

    Methods:
        __getitem__(type):
            Gets the regex for the given type.

    """

    def __init__(self):
        """Initialize the regex mapping.

        Examples:
            >>> from anonipy.anonymize.regex import RegexMapping
            >>> regex_mapping = RegexMapping()

        """

        self.regex_mapping = defaultdict(lambda: ".*")
        # Define the regex mappings
        self.regex_mapping[ENTITY_TYPES.STRING] = REGEX_STRING
        self.regex_mapping[ENTITY_TYPES.INTEGER] = REGEX_INTEGER
        self.regex_mapping[ENTITY_TYPES.FLOAT] = REGEX_FLOAT
        self.regex_mapping[ENTITY_TYPES.DATE] = REGEX_DATE
        self.regex_mapping[ENTITY_TYPES.EMAIL] = REGEX_EMAIL_ADDRESS
        self.regex_mapping[ENTITY_TYPES.PHONE_NUMBER] = REGEX_PHONE_NUMBER
        self.regex_mapping[ENTITY_TYPES.WEBSITE_URL] = REGEX_WEBSITE_URL

    def __getitem__(self, regex_type: str) -> str:
        """Gets the regex for the given type.

        Examples:
            >>> from anonipy.anonymize.regex import RegexMapping
            >>> regex_mapping = RegexMapping()
            >>> regex_mapping["string"]
            ".*"

        Args:
            regex_type: The type of the entity.

        Returns:
            The regex for the given type.

        """
        return self.regex_mapping[regex_type]


regex_mapping = RegexMapping()
"""The shorthand to the `RegexMapping` instance."""
