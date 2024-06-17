import dateutil.parser as parser

# =====================================
# Constants
# =====================================

POSSIBLE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%m-%d-%Y %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
    "%Y.%m.%d %H:%M:%S",
    "%d.%m.%Y %H:%M:%S",
    "%m.%d.%Y %H:%M:%S",
    "%Y %m %d %H:%M:%S",
    "%d %m %Y %H:%M:%S",
    "%m %d %Y %H:%M:%S",
    "%Y-%m-%d %I:%M %p",
    "%d-%m-%Y %I:%M %p",
    "%m-%d-%Y %I:%M %p",
    "%Y/%m/%d %I:%M %p",
    "%d/%m/%Y %I:%M %p",
    "%m/%d/%Y %I:%M %p",
    "%Y.%m.%d %I:%M %p",
    "%d.%m.%Y %I:%M %p",
    "%m.%d.%Y %I:%M %p",
    "%Y %m %d %I:%M %p",
    "%d %m %Y %I:%M %p",
    "%m %d %Y %I:%M %p",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%m-%d-%Y %H:%M",
    "%Y/%m/%d %H:%M",
    "%d/%m/%Y %H:%M",
    "%m/%d/%Y %H:%M",
    "%Y.%m.%d %H:%M",
    "%d.%m.%Y %H:%M",
    "%m.%d.%Y %H:%M",
    "%Y %m %d %H:%M",
    "%d %m %Y %H:%M",
    "%m %d %Y %H:%M",
    "%Y-%m-%d %H:%M",
    "%A, %d %B %Y %H:%M:%S",
    "%A, %B %d, %Y %H:%M:%S",
    "%A, %d %B %Y %I:%M %p",
    "%A, %B %d, %Y %I:%M %p",
    "%B %d, %Y %H:%M:%S",
    "%d %B %Y %H:%M:%S",
    "%b %d, %Y %H:%M:%S",
    "%d %b %Y %H:%M:%S",
    "%B %d, %Y %I:%M %p",
    "%d %B %Y %I:%M %p",
    "%b %d, %Y %I:%M %p",
    "%d %b %Y %I:%M %p",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%m-%d-%Y",
    "%Y/%m/%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%Y.%m.%d",
    "%d.%m.%Y",
    "%m.%d.%Y",
    "%Y %m %d",
    "%d %m %Y",
    "%m %d %Y",
    "%B %d, %Y",
    "%d %B %Y",
    "%b %d, %Y",
    "%d %b %Y",
    "%A, %d %B %Y",
    "%A, %B %d, %Y",
]


# =====================================
# Auto date format detector
# =====================================


def detect_datetime_format(datetime):
    try:
        parsed_datetime = parser.parse(datetime, fuzzy=True)

        for FMT in POSSIBLE_FORMATS:
            try:
                if parsed_datetime.strftime(FMT) == datetime:
                    return parsed_datetime, FMT
            except ValueError:
                continue

        return parsed_datetime, ValueError("Unknown Format")

    except parser.ParserError:
        return None, None
