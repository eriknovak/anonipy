import random
import warnings
import datetime
from .interface import GeneratorInterface
from ...definitions import Entity

# =====================================
# Helper functions
# =====================================


def first_day_of_month(day: datetime.datetime, *args, **kwargs):
    return day.replace(day=1)


def last_day_of_month(day: datetime.datetime, *args, **kwargs):
    next_month = day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def middle_of_the_month(day: datetime.datetime, *args, **kwargs):
    return day.replace(day=15)


def middle_of_the_year(day: datetime.datetime, *args, **kwargs):
    return day.replace(month=7, day=1)


def random_date(day: datetime.datetime, sigma: int = 30, *args, **kwargs):
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

    def __init__(
        self, date_format: str = "%d-%m-%Y", day_sigma: int = 30, *args, **kwargs
    ):
        self.date_format = date_format
        self.day_sigma = day_sigma

    def generate(self, entity: Entity, output_gen: str = "random", *args, **kwargs):
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

        entity_date = datetime.datetime.strptime(entity.text, self.date_format)
        generate_date = operations[output_gen](entity_date, self.day_sigma)
        return generate_date.strftime(self.date_format)
