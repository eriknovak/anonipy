import re
import datetime
from typing import Tuple

import dateparser
from babel.dates import format_datetime, format_datetime

from ..constants import LANGUAGES


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
    "EEE, MMM d, yyyy"
]


# =====================================
# Auto date format detector
# =====================================


def detect_datetime_format(datetime: str, lang: str) -> Tuple[datetime.datetime, str]:
    """Detects the datetime format.

    Args:
        datetime: The datetime string to detect the format.

    Returns:
        The detected datetime and it's format.

    """

    # Lowercase the first word
    if lang not in ['en', 'de', 'el']:
        datetime = datetime.lower()

    # Remove AM/PM 
    datetime = re.sub(r"[ ]?[APap][mM]", "", datetime).strip()

    # Remove all occurrences of '1er'
    datetime = re.sub(r'\b1er\b', '1', datetime)

    # Remove all occurrences of 'του' and 'η'
    datetime = re.sub(r"(\d+)η", r"\1", datetime)
    datetime = re.sub(r"\bτου\b", "", datetime)
    datetime = re.sub(r"\s+", " ", datetime).strip()

    # Remove all occurrences of '1°'
    datetime = re.sub(r"1°", '1', datetime)
    
    # Remove all occurrences of 'року'
    datetime = re.sub(r"\bроку\b", "", datetime).strip()
    
    try:
        parsed_datetime = dateparser.parse(datetime, languages=[lang])
    	
        for FMT in POSSIBLE_FORMATS:
            try:
                formatted_date = format_datetime(parsed_datetime, format=FMT, locale=lang)
                
                if formatted_date == datetime:
                    return parsed_datetime, FMT
            except ValueError:
                continue
           
        return parsed_datetime, ValueError("Unknown Format")

    except dateparser.ParserError:
        return None, None
    
