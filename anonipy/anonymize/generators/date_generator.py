import random
import warnings
import datetime

from ...utils.datetime import detect_datetime_format
from .interface import GeneratorInterface
from ...definitions import Entity

# =====================================
# Operation functions
# =====================================


def first_day_of_month(day: datetime.datetime, *args, **kwargs):
    """Returns the first day of the month of the given date

    Parameters
    ----------
    day : datetime.datetime
        The date to get the first day of the month from

    Returns
    -------
    datetime.datetime
        The first day of the month of the given date

    """
    return day.replace(day=1)


def last_day_of_month(day: datetime.datetime, *args, **kwargs):
    """Returns the last day of the month of the given date

    Parameters
    ----------
    day : datetime.datetime
        The date to get the last day of the month from

    Returns
    -------
    datetime.datetime
        The last day of the month of the given date

    """
    next_month = day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def middle_of_the_month(day: datetime.datetime, *args, **kwargs):
    """Returns the middle day of the month of the given date

    Parameters
    ----------
    day : datetime.datetime
        The date to get the middle day of the month from

    Returns
    -------
    datetime.datetime
        The middle day of the month of the given date

    """

    return day.replace(day=15)


def middle_of_the_year(day: datetime.datetime, *args, **kwargs):
    """Returns the middle day of the year of the given date

    Parameters
    ----------
    day : datetime.datetime
        The date to get the middle day of the year from

    Returns
    -------
    datetime.datetime
        The middle day of the year of the given date

    """

    return day.replace(month=7, day=1)


def random_date(day: datetime.datetime, sigma: int = 30, *args, **kwargs):
    """Returns a random date within the given date range

    The function returns a date within the range [day - sigma, day + sigma].

    Parameters
    ----------
    day : datetime.datetime
        The date to get the random date from
    sigma : int
        The range of the random date in days. Default: 30

    Returns
    -------
    datetime.datetime
        The random date within the given date range

    """
    delta = random.randint(-sigma, sigma)
    return day + datetime.timedelta(days=delta)


operations = {
    "first_day_of_the_month": first_day_of_month,
    "last_day_of_the_month": last_day_of_month,
    "middle_of_the_month": middle_of_the_month,
    "middle_of_the_year": middle_of_the_year,
    "random": random_date,
}


# =====================================
# Main class
# =====================================


class DateGenerator(GeneratorInterface):
    """The class representing the date generator

    Attributes
    ----------
    date_format : str
        The date format to use
    day_sigma : int
        The range of the random date in days

    Methods
    -------
    generate(entity: Entity, output_gen: str = "random")
        Generate the date based on the entity and output_gen

    """

    def __init__(self, date_format="auto", day_sigma: int = 30, *args, **kwargs):
        """
        Parameters
        ----------
        date_format : str, optional
            The date format to use. Default: "auto"
        day_sigma : int, optional
            The range of the random date in days. Default: 30

        """

        super().__init__(*args, **kwargs)
        self.date_format = date_format
        self.day_sigma = day_sigma

    def generate(self, entity: Entity, output_gen: str = "random", *args, **kwargs):
        """Generate the date based on the entity and output_gen

        Parameters
        ----------
        entity : Entity
            The entity to generate the date from
        output_gen : str, optional
            The output generator to use. Default: "random"

        Returns
        -------
        str
            The generated date

        Raises
        ------
        ValueError
            If the entity type is not `date` or `custom`

        """

        if entity.type in ["custom"]:
            warnings.warn(
                "The entity type is `custom`. Make sure the generator is returning appropriate values."
            )
        elif entity.type not in ["date"]:
            raise ValueError("The entity type must be `date` to generate dates.")

        if output_gen not in operations.keys():
            raise ValueError(
                f"The output_gen must be one of {', '.join(list(operations.keys()))} to generate dates."
            )

        if self.date_format == "auto":
            entity_date, date_format = detect_datetime_format(entity.text)
        else:
            entity_date = datetime.datetime.strptime(entity.text, self.date_format)
            date_format = self.date_format
        if entity_date is None:
            raise ValueError(f"Entity `{entity.text}` is not a valid date.")
        if date_format is None or date_format == ValueError("Unknown Format"):
            raise ValueError(f"Entity `{entity.text}` is not a valid date.")
        generate_date = operations[output_gen](entity_date, self.day_sigma)
        return generate_date.strftime(date_format)
