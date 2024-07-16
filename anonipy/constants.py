"""Module containing the `constants`.

The `constants` module provides a set of predefined constants used in the package.
These include supported languages, types of entities, and date transformation
variants.

Classes:
    LANGUAGES: Predefined supported languages.
    ENTITY_TYPES: Predefined types of entities.
    DATE_TRANSFORM_VARIANTS: Predefined types of the date transformation variants.

"""

from typing import List


class LANGUAGES:
    """The main anonipy supported languages.

    Attributes:
        DUTCH (Tuple[Literal["nl"], Literal["Dutch"]]): The Dutch language.
        ENGLISH (Tuple[Literal["en"], Literal["English"]]): The English language.
        FRENCH (Tuple[Literal["fr"], Literal["French"]]): The French language.
        GERMAN (Tuple[Literal["de"], Literal["German"]]): The German language.
        GREEK (Tuple[Literal["el"], Literal["Greek"]]): The Greek language.
        ITALIAN (Tuple[Literal["it"], Literal["Italian"]]): The Italian language.
        SLOVENE (Tuple[Literal["sl"], Literal["Slovene"]]): The Slovene language.
        SPANISH (Tuple[Literal["es"], Literal["Spanish"]]): The Spanish language.
        UKRAINIAN (Tuple[Literal["uk"], Literal["Ukrainian"]]): The Ukrainian language.

    """

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
    """The anonipy supported entity types.

    Attributes:
        CUSTOM (Literal["custom"]): The custom entity type.
        STRING (Literal["string"]): The string entity type.
        INTEGER (Literal["integer"]): The integer entity type.
        FLOAT (Literal["float"]): The float entity type.
        DATE (Literal["date"]): The date entity type.
        EMAIL (Literal["email"]): The email entity type.
        WEBSITE_URL (Literal["website_url"]): The website url entity type.
        PHONE_NUMBER (Literal["phone_number"]): The phone number entity type.

    """

    CUSTOM = "custom"
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    EMAIL = "email"
    WEBSITE_URL = "website_url"
    PHONE_NUMBER = "phone_number"


class DATE_TRANSFORM_VARIANTS:
    """The supported date transform variants.

    Attributes:
        FIRST_DAY_OF_THE_MONTH (Literal["FIRST_DAY_OF_THE_MONTH"]): The first day of the month.
        LAST_DAY_OF_THE_MONTH (Literal["LAST_DAY_OF_THE_MONTH"]): The last day of the month.
        MIDDLE_OF_THE_MONTH (Literal["MIDDLE_OF_THE_MONTH"]): The middle of the month.
        MIDDLE_OF_THE_YEAR (Literal["MIDDLE_OF_THE_YEAR"]): The middle of the year.
        RANDOM (Literal["RANDOM"]): A random date.

    Methods:
        values():
            Return a list of all possible date transform variants.
        is_valid(value):
            Check if the value is a valid date variant.

    """

    FIRST_DAY_OF_THE_MONTH = "FIRST_DAY_OF_THE_MONTH"
    LAST_DAY_OF_THE_MONTH = "LAST_DAY_OF_THE_MONTH"
    MIDDLE_OF_THE_MONTH = "MIDDLE_OF_THE_MONTH"
    MIDDLE_OF_THE_YEAR = "MIDDLE_OF_THE_YEAR"
    RANDOM = "RANDOM"

    @classmethod
    def values(self) -> List[str]:
        """Return a list of all possible date transform variants.

        Returns:
            The list of all possible variants.

        """
        return [
            self.FIRST_DAY_OF_THE_MONTH,
            self.LAST_DAY_OF_THE_MONTH,
            self.MIDDLE_OF_THE_MONTH,
            self.MIDDLE_OF_THE_YEAR,
            self.RANDOM,
        ]

    @classmethod
    def is_valid(self, value: str) -> bool:
        """Check if the value is a valid date variant.

        Args:
            value: The value to check.

        Returns:
            `True` if the value is a valid date variant, `False` otherwise.

        """
        return value in self.values()
