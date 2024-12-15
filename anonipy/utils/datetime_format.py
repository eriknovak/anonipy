import re
import datetime
import warnings
from typing import Tuple

import dateparser
from babel.dates import format_datetime, format_datetime


# =====================================
# Constants
# =====================================


POSSIBLE_FORMATS = [
    "yyyy-MM-dd HH:mm:ss",
    "dd-MM-yyyy HH:mm:ss",
    "MM-dd-yyyy HH:mm:ss",
    "yyyy/MM/dd HH:mm:ss",
    "dd/MM/yyyy HH:mm:ss",
    "MM/dd/yyyy HH:mm:ss",
    "yyyy.MM.dd HH:mm:ss",
    "dd.MM.yyyy HH:mm:ss",
    "d.M.yyyy HH:mm:ss",
    "MM.dd.yyyy HH:mm:ss",
    "yyyy-MM-dd HH:mm",
    "dd-MM-yyyy HH:mm",
    "MM-dd-yyyy HH:mm",
    "yyyy/MM/dd HH:mm",
    "dd/MM/yyyy HH:mm",
    "MM/dd/yyyy HH:mm",
    "yyyy.MM.dd HH:mm",
    "dd.MM.yyyy HH:mm",
    "d.M.yyyy HH:mm",
    "MM.dd.yyyy HH:mm",
    "yyyy-MM-dd",
    "dd-MM-yyyy",
    "MM-dd-yyyy",
    "yyyy/MM/dd",
    "dd/MM/yyyy",
    "MM/dd/yyyy",
    "yyyy.MM.dd",
    "dd.MM.yyyy",
    "d.M.yyyy",
    "MM.dd.yyyy",
    "d MMMM yyyy HH:mm:ss",
    "d MMMM yyyy HH:mm",
    "d MMMM yyyy",
    "d. MMMM yyyy HH:mm:ss",
    "d. MMMM yyyy HH:mm",
    "d. MMMM yyyy",
    "d MMM yyyy HH:mm:ss",
    "d MMM yyyy HH:mm",
    "d MMM yyyy",
    "d. MMM yyyy HH:mm:ss",
    "d. MMM yyyy HH:mm",
    "d. MMM yyyy",
    "EEE, d MMMM yyyy HH:mm:ss",
    "EEE, d MMMM yyyy HH:mm",
    "EEE, d MMMM yyyy",
    "EEE, d MMMM, yyyy HH:mm:ss",
    "EEE, d MMMM, yyyy HH:mm",
    "EEE, d MMMM, yyyy",
    "EEE, d. MMMM yyyy HH:mm:ss",
    "EEE, d. MMMM yyyy HH:mm",
    "EEE, d. MMMM yyyy",
    "EEE, d. MMMM, yyyy HH:mm:ss",
    "EEE, d. MMMM, yyyy HH:mm",
    "EEE, d. MMMM, yyyy",
    "EEE, MMMM d, yyyy HH:mm:ss",
    "EEE, MMMM d, yyyy HH:mm",
    "EEE, MMMM d, yyyy",
    "EEE, MMMM d yyyy HH:mm:ss",
    "EEE, MMMM d yyyy HH:mm",
    "EEE, MMMM d yyyy",
    "EEEE, d MMMM yyyy HH:mm:ss",
    "EEEE, d MMMM yyyy HH:mm",
    "EEEE, d MMMM yyyy",
    "EEEE, d MMMM, yyyy HH:mm:ss",
    "EEEE, d MMMM, yyyy HH:mm",
    "EEEE, d MMMM, yyyy",
    "EEEE, d. MMMM yyyy HH:mm:ss",
    "EEEE, d. MMMM yyyy HH:mm",
    "EEEE, d. MMMM yyyy",
    "EEEE, d. MMMM, yyyy HH:mm:ss",
    "EEEE, d. MMMM, yyyy HH:mm",
    "EEEE, d. MMMM, yyyy",
    "EEEE, MMMM d, yyyy HH:mm:ss",
    "EEEE, MMMM d, yyyy HH:mm",
    "EEEE, MMMM d, yyyy",
    "EEEE, MMMM d yyyy HH:mm:ss",
    "EEEE, MMMM d yyyy HH:mm",
    "EEEE, MMMM d yyyy",
    "d 'de' MMMM 'de' yyyy HH:mm:ss",
    "d 'de' MMMM 'de' yyyy HH:mm",
    "d 'de' MMMM 'de' yyyy",
    "EEEE, d 'de' MMMM 'de' yyyy HH:mm:ss",
    "EEEE, d 'de' MMMM 'de' yyyy HH:mm",
    "EEEE, d 'de' MMMM 'de' yyyy",
    "EEEE, MMMM d 'de' yyyy HH:mm:ss",
    "EEEE, MMMM d 'de' yyyy HH:mm",
    "EEEE, MMMM d 'de' yyyy",
    "MMM d, yyyy HH:mm:ss",
    "MMM d, yyyy HH:mm",
    "MMM d, yyyy",
    "d MMM yyyy HH:mm:ss",
    "d MMM yyyy HH:mm",
    "d MMM yyyy",
    "EEE, MMM d, yyyy HH:mm:ss",
    "EEE, MMM d, yyyy HH:mm",
    "EEE, MMM d, yyyy",
]


# =====================================
# Auto date format detector
# =====================================


def detect_datetime_format(datetime: str, lang: str) -> Tuple[datetime.datetime, str]:
    """Detects the datetime format.

    Args:
        datetime: The datetime string to detect the format.
        lang: The language of the datetime string.

    Returns:
        The detected datetime and it's format.

    """

    fdatetime = _prepare_datetime(datetime, lang)

    try:
        parsed_datetime = dateparser.parse(fdatetime, languages=[lang])

        for FMT in POSSIBLE_FORMATS:
            try:
                formatted_date = format_datetime(
                    parsed_datetime, format=FMT, locale=lang
                )
                if formatted_date == fdatetime:
                    return parsed_datetime, FMT
            except ValueError:
                continue

        warnings.warn(
            f"Could not detect the datetime format for `{datetime}`. Defaulting to `yyyy-MM-dd`..."
        )
        return parsed_datetime, "yyyy-MM-dd"

    except dateparser.ParserError:
        return None, None


def _prepare_datetime(datetime: str, lang: str) -> str:
    """Preares the datetime string for formatting.

    Args:
        datetime: The datetime string to format.
        lang: The language of the datetime string.

    Returns:
        The formatted datetime string.

    """

    if lang not in ["en", "de", "el"]:
        datetime = datetime.lower()

    # Remove AM/PM
    datetime = re.sub(r"[ ]?[APap][mM]", "", datetime).strip()

    # Language-specific cleaning
    datetime = re.sub(r"\b1er\b", "1", datetime)  # French
    datetime = re.sub(r"(\d+)η", r"\1", datetime)  # Greek
    datetime = re.sub(r"\bτου\b", "", datetime)  # Greek
    datetime = re.sub(r"°", "", datetime)  # Italian, Spanish
    datetime = re.sub(r"\bроку\b", "", datetime)  # Ukrainian

    # Remove extra spaces
    datetime = re.sub(r"\s+", " ", datetime).strip()

    return datetime
