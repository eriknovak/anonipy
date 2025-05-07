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
    r"(\d{4}[-/.\s]\d{1,2}[-/.\s]\d{1,2}(?:[ T]\d{2}:\d{2}:\d{2})?)|"
    r"(\d{1,2}[-/.\s]\d{1,2}[-/.\s]\d{4}(?:[ T]\d{2}:\d{2}:\d{2})?)|"
    r"(\d{1,2}[-/.\s]\d{1,2}[-/.\s]\d{4}(?:[ T]\d{2}:\d{2})?)|"
    r"(\d{4}[-/.\s]\d{1,2}[-/.\s]\d{1,2}(?:[ T]\d{2}:\d{2})?)|"
    r"(\d{4}[-/.\s]\d{1,2}[-/.\s]\d{1,2}(?:[ T]\d{2}:\d{2} [APap][mM])?)|"
    r"(\d{1,2}[-/.\s]\d{1,2}[-/.\s]\d{4}(?:[ T]\d{2}:\d{2} [APap][mM])?)|"
    r"(\d{1,2}[-/.\s]\d{1,2}[-/.\s]\d{4}(?:[ ]?\d{2}:\d{2}:\d{2})?)|"
    r"(\d{4}[-/.\s]\d{1,2}[-/.\s]\d{1,2}(?:[ ]?\d{2}:\d{2}:\d{2})?)|"
    # English dates
    r"(\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4}(?:[ ]?\d{2}:\d{2}:\d{2})?)|"
    r"(\d{1,2}[ ](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ ]\d{4}(?:[ ]?\d{2}:\d{2}:\d{2})?)|"
    r"(\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{4}(?:[ ]?\d{2}:\d{2}[ ]?[APap][mM])?)|"
    r"(\d{1,2}[ ](Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[ ]\d{4}(?:[ ]?\d{2}:\d{2}[ ]?[APap][mM])?)|"
    r"([A-Za-z]+,[ ]\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December),?[ ]\d{4}(?:[ ]?\d{2}:\d{2}:\d{2})?)|"
    r"([A-Za-z]+,[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{1,2},?[ ]\d{4}(?:[ ]?\d{2}:\d{2}:\d{2})?)|"
    r"([A-Za-z]+,[ ]\d{1,2}[ ](January|February|March|April|May|June|July|August|September|October|November|December),?[ ]\d{4}(?:[ ]?\d{2}:\d{2}[ ]?[APap][mM])?)|"
    r"([A-Za-z]+,[ ](January|February|March|April|May|June|July|August|September|October|November|December)[ ]\d{1,2},?[ ]\d{4}(?:[ ]?\d{2}:\d{2}[ ]?[APap][mM])?)|"
    # Dutch dates
    r"(\d{1,2}[\.]?[ ](januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](jan|feb|mrt|apr|mei|jun|jul|aug|sep|okt|nov|dec)[\.]?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ]\d{1,2}[\.]?[ ](januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december),?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ](januari|februari|maart|april|mei|juni|juli|augustus|september|oktober|november|december)[ ]\d{1,2},?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # French dates
    r"(\d{1,2}(er)?[ ](janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}(er)?[ ](jan|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)[\.]?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zÀ-ÿ]+,?[ ]\d{1,2}(er)?[ ](janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre),?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zÀ-ÿ]+,?[ ](janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)[ ]\d{1,2}(er)?,?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # German dates
    r"(\d{1,2}[\.]?[ ](Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](Jan|Feb|Mär|Apr|Mai|Jun|Jul|Aug|Sep|Okt|Nov|Dez)[\.]?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zäöüßÄÖÜ]+,?[ ]\d{1,2}[\.]?[ ](Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zäöüßÄÖÜ]+,?[ ](Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)[ ]\d{1,2}[\.]?,?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # Greek dates
    r"(\d{1,2}η?[ ](Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου)( του)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}i?[ ](Ianouariou|Fevrouariou|Martiou|Apriliou|Maiou|Iouniou|Iouliou|Avgoustou|Septemvriou|Oktovriou|Noemvriou|Dekemvriou)( tou)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}η?[ ](Ιαν|Φεβ|Μάρ|Απρ|Μάι|Ιούν|Ιούλ|Aυγ|Σεπ|Οκτ|Νοε|Δεκ)[\.]?( του)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}i?[ ](Ian|Feb|Mar|Apr|Mai|Iou|Ioul|Avg|Sep|Okt|Noe|Dek)[\.]?( tou)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([\u0370-\u03FF]+,?[ ]\d{1,2}η?[ ](Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου),?( του)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ]\d{1,2}i?[ ](Ianouariou|Fevrouariou|Martiou|Apriliou|Maiou|Iouniou|Iouliou|Avgoustou|Septemvriou|Oktovriou|Noemvriou|Dekemvriou),?( tou)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([\u0370-\u03FF]+,?[ ](Ιανουαρίου|Φεβρουαρίου|Μαρτίου|Απριλίου|Μαΐου|Ιουνίου|Ιουλίου|Αυγούστου|Σεπτεμβρίου|Οκτωβρίου|Νοεμβρίου|Δεκεμβρίου)[ ]\d{1,2}η?,?( του)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ](Ianouariou|Fevrouariou|Martiou|Apriliou|Maiou|Iouniou|Iouliou|Avgoustou|Septemvriou|Oktovriou|Noemvriou|Dekemvriou)[ ]\d{1,2}i?,?( tou)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # Italian dates
    r"(\d{1,2}°?[ ](gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}°?[ ](gen|feb|mar|apr|mag|giu|lug|ago|set|ott|nov|dic)[\.]?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zÀ-ÿ]+,?[ ]\d{1,2}°?[ ](gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre),?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zÀ-ÿ]+,?[ ](gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)[ ]\d{1,2}°?,?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # Slovenian dates
    r"(\d{1,2}[\.]?[ ](januar|februar|marec|april|maj|junij|julij|avgust|september|oktober|november|december)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](januarja|februarja|marca|aprila|maja|junija|julija|avgusta|septembra|oktobra|novembra|decembra)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](jan|feb|mar|apr|maj|jun|jul|avg|sep|okt|nov|dec)[\.]?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zčšžČŠŽ]+,?[ ]\d{1,2}[\.]?[ ](januar|februar|marec|april|maj|junij|julij|avgust|september|oktober|november|december)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zčšžČŠŽ]+,?[ ]\d{1,2}[\.]?[ ](januarja|februarja|marca|aprila|maja|junija|julija|avgusta|septembra|oktobra|novembra|decembra)[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # Spanish dates
    r"(\d{1,2}°?( de)?[ ](enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)( de)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}°?( de)?[ ](ene|feb|mar|abr|may|jun|jul|ago|sept|oct|nov|dic)[\.]?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zÀ-ÿ]+,?[ ]\d{1,2}°?( de)?[ ](enero|febrero|marzo|abril|mayo|junio|julio|augusto|septiembre|octubre|noviembre|diciembre),?( de)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-zÀ-ÿ]+,?[ ](enero|febrero|marzo|abril|mayo|junio|julio|augusto|septiembre|octubre|noviembre|diciembre)[ ]\d{1,2}°?,?( de)?[ ]\d{4}(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    # Ukrainian dates
    r"(\d{1,2}[\.]?[ ](січень|лютий|березень|квітень|травень|червень|липень|серпень|вересень|жовтень|листопад|грудень)[ ]\d{4}( року| рік)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](sichen|lyutyi|berezen|kviten|traven|cherven|lypen|serpen|veresen|zhovten|lystopad|gruden)[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](січ|лют|бер|кві|тра|чер|лип|сер|вер|жов|лис|гру)[\.]?[ ]\d{4}( року| рік)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](sich|lyut|ber|kvi|tra|cher|lyp|ser|ver|zhov|lys|gru)[\.]?[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([А-ЩЬЮЯҐЄІЇа-щьюяґєії]+,?[ ]\d{1,2}[\.]?[ ](січень|лютий|березень|квітень|травень|червень|липень|серпень|вересень|жовтень|листопад|грудень)[ ]\d{4}( року)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ]\d{1,2}[\.]?[ ](sichen|lyutyi|berezen|kviten|traven|cherven|lypen|serpen|veresen|zhovten|lystopad|gruden)[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([А-ЩЬЮЯҐЄІЇа-щьюяґєії]+,?[ ](січень|лютий|березень|квітень|травень|червень|липень|серпень|вересень|жовтень|листопад|грудень)[ ]\d{1,2}[\.]?,?[ ]\d{4}( року)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ](sichen|lyutyi|berezen|kviten|traven|cherven|lypen|serpen|veresen|zhovten|lystopad|gruden)[ ]\d{1,2}[\.]?,?[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)[ ]\d{4}( року| рік)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"(\d{1,2}[\.]?[ ](sichnia|liutoho|bereznia|kvitnia|travniia|chervnia|lypnia|serpnia|veresnia|zhovtnia|lystopada|hrudnia)[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([А-ЩЬЮЯҐЄІЇа-щьюяґєії]+,?[ ]\d{1,2}[\.]?[ ](січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)[ ]\d{4}( року| рік)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ]\d{1,2}[\.]?[ ](sichnia|liutoho|bereznia|kvitnia|travniia|chervnia|lypnia|serpnia|veresnia|zhovtnia|lystopada|hrudnia)[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([А-ЩЬЮЯҐЄІЇа-щьюяґєії]+,?[ ](січня|лютого|березня|квітня|травня|червня|липня|серпня|вересня|жовтня|листопада|грудня)[ ]\d{1,2}[\.]?,?[ ]\d{4}( року| рік)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)|"
    r"([A-Za-z]+,?[ ](sichnia|liutoho|bereznia|kvitnia|travniia|chervnia|lypnia|serpnia|veresnia|zhovtnia|lystopada|hrudnia)[ ]\d{1,2}[\.]?,?[ ]\d{4}( roku)?(?:[ ]?\d{2}:\d{2}(?::\d{2})?)?)"
    r")"
)
"""The regex definition for dates."""

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
