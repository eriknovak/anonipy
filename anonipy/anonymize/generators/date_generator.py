import random
import warnings
import datetime

from ...utils.datetime import detect_datetime_format
from .interface import GeneratorInterface
from ...definitions import Entity
from ...constants import DATE_TRANSFORM_VARIANTS

# =====================================
# Operation functions
# =====================================


def first_day_of_month(day: datetime.datetime, *args, **kwargs) -> datetime.datetime:
    """Returns the first day of the month of the given date.

    Args:
        day: The date to get the first day of the month from.

    Returns:
        The first day of the month of the given date.

    """
    return day.replace(day=1)


def last_day_of_month(day: datetime.datetime, *args, **kwargs) -> datetime.datetime:
    """Returns the last day of the month of the given date.

    Args:
        day: The date to get the last day of the month from.

    Returns:
        The last day of the month of the given date.

    """
    next_month = day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def middle_of_the_month(day: datetime.datetime, *args, **kwargs) -> datetime.datetime:
    """Returns the middle day of the month of the given date.

    Args:
        day: The date to get the middle day of the month from.

    Returns:
        The middle day of the month of the given date.

    """

    return day.replace(day=15)


def middle_of_the_year(day: datetime.datetime, *args, **kwargs) -> datetime.datetime:
    """Returns the middle day of the year of the given date.

    Args:
        day: The date to get the middle day of the year from.

    Returns:
        The middle day of the year of the given date.

    """

    return day.replace(month=7, day=1)


def random_date(
    day: datetime.datetime, sigma: int = 30, *args, **kwargs
) -> datetime.datetime:
    """Returns a random date within the given date range.

    The function returns a date within the range [day - sigma, day + sigma].

    Args:
        day: The date to get the random date from.
        sigma: The range of the random date in days.

    Returns:
        The random date within the given date range.

    """
    delta = random.randint(-sigma, sigma)
    return day + datetime.timedelta(days=delta)


DATE_VARIANTS_MAPPING = {
    DATE_TRANSFORM_VARIANTS.FIRST_DAY_OF_THE_MONTH: first_day_of_month,
    DATE_TRANSFORM_VARIANTS.LAST_DAY_OF_THE_MONTH: last_day_of_month,
    DATE_TRANSFORM_VARIANTS.MIDDLE_OF_THE_MONTH: middle_of_the_month,
    DATE_TRANSFORM_VARIANTS.MIDDLE_OF_THE_YEAR: middle_of_the_year,
    DATE_TRANSFORM_VARIANTS.RANDOM: random_date,
}

# =====================================
# Main class
# =====================================


class DateGenerator(GeneratorInterface):
    """The class representing the date generator.

    Examples:
        >>> from anonipy.anonymize.generators import DateGenerator
        >>> generator = DateGenerator()
        >>> generator.generate(entity)

    Attributes:
        date_format (str): The date format in which the date should be generated.
        day_sigma (int): The range of the random date in days.

    Methods:
        generate(entity, output_gen):
            Generate the date substitute based on the input parameters.

    """

    def __init__(self, *args, date_format: str = "auto", day_sigma: int = 30, **kwargs):
        """Initializes he date generator.

        Examples:
            >>> from anonipy.anonymize.generators import DateGenerator
            >>> generator = DateGenerator()

        Args:
            date_format: The date format in which the date should be generated. More on date formats [see here](https://www.contensis.com/help-and-docs/guides/querying-your-content/zenql-search/date-formats).
            day_sigma: The range of the random date in days.

        """

        super().__init__(*args, **kwargs)
        self.date_format = date_format
        self.day_sigma = day_sigma

    def generate(
        self,
        entity: Entity,
        *args,
        sub_variant: DATE_TRANSFORM_VARIANTS = DATE_TRANSFORM_VARIANTS.RANDOM,
        **kwargs,
    ) -> str:
        """Generate the entity substitute based on the input parameters.

        Args:
            entity: The entity to generate the date substitute from.
            sub_variant: The substitute function variant to use.

        Returns:
            The generated date substitute.

        Raises:
            ValueError: If the entity type is not `date` or `custom`.

        """

        if entity.type in ["custom"]:
            warnings.warn(
                "The entity type is `custom`. Make sure the generator is returning appropriate values."
            )
        elif entity.type not in ["date"]:
            raise ValueError("The entity type must be `date` to generate dates.")

        if not DATE_TRANSFORM_VARIANTS.is_valid(sub_variant):
            raise ValueError(
                f"The output_gen must be one of {', '.join(DATE_TRANSFORM_VARIANTS.values())} to generate dates."
            )

        # detect the date format
        if self.date_format == "auto":
            entity_date, date_format = detect_datetime_format(entity.text)
        else:
            entity_date = datetime.datetime.strptime(entity.text, self.date_format)
            date_format = self.date_format

        # validate the input values
        if entity_date is None:
            raise ValueError(f"Entity `{entity.text}` is not a valid date.")
        if date_format is None or date_format == ValueError("Unknown Format"):
            raise ValueError(f"Entity `{entity.text}` is not a valid date.")

        # generate the date substitute
        generate_date = DATE_VARIANTS_MAPPING[sub_variant](entity_date, self.day_sigma)
        return generate_date.strftime(date_format)
