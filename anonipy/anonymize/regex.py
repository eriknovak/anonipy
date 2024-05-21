"""
The regex definitions for various use cases
"""

from collections import defaultdict

# =====================================
# Regex definitions
# =====================================

REGEX_STRING = ".*"
REGEX_INTEGER = "\d+"
REGEX_FLOAT = "[\d\.,]+"
REGEX_DATE = (
    "(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})|(\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})"
)
REGEX_EMAIL_ADDRESS = (
    "[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*"
)
REGEX_PHONE_NUMBER = (
    "[(]?[\+]?[(]?[0-9]{1,3}[)]?[-\s\.]?([0-9]{2,}[-\s\.]?){2,}([0-9]{3,})"
)
REGEX_WEBSITE_URL = "((https?|ftp|smtp):\/\/)?(www.)?([a-zA-Z0-9]+\.)+[a-z]{2,}(\/[a-zA-Z0-9#\?\_\.\=\-\&]+|\/?)*"


# =====================================
# Define the regex definitions
# =====================================


class RegexMap:

    def __init__(self):
        self.regex_mapping = defaultdict(lambda: ".*")
        # Define the regex mappings
        self.regex_mapping["string"] = REGEX_STRING
        self.regex_mapping["integer"] = REGEX_INTEGER
        self.regex_mapping["float"] = REGEX_FLOAT
        self.regex_mapping["date"] = REGEX_DATE
        self.regex_mapping["email"] = REGEX_EMAIL_ADDRESS
        self.regex_mapping["phone_number"] = REGEX_PHONE_NUMBER
        self.regex_mapping["website_url"] = REGEX_WEBSITE_URL

    def __call__(self, type: str) -> str:
        return self.regex_mapping[type]


regex_map = RegexMap()
