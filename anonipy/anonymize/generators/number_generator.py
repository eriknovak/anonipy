import random
import warnings
from .interface import GeneratorInterface
from ...definitions import Entity

# =====================================
# Main class
# =====================================


class NumberGenerator(GeneratorInterface):
    """The class representing the number generator

    Methods
    -------
    generate(self, entity: Entity)
        Generates a number replacement

    """

    def __init__(self, *args, **kwargs):
        """
        Parameters
        ----------
        None

        """
        super().__init__(*args, **kwargs)
        pass

    def generate(self, entity: Entity, *args, **kwargs):
        """Generates a number replacement

        Parameters
        ----------
        entity : Entity
            The entity to generate the number from

        Returns
        -------
        str
            The generated number

        Raises
        ------
        ValueError
            If the entity type is not `integer`, `float`, `phone_number` or `custom`

        """
        if entity.type in ["custom"]:
            warnings.warn(
                "The entity type is `custom`. Make sure the generator is returning appropriate values."
            )
        elif entity.type not in ["integer", "float", "phone_number"]:
            raise ValueError(
                "The entity type must be `integer`, `float`, `phone_number` or `custom` to generate numbers."
            )
        return "".join(
            [str(random.randint(0, 9)) if d.isdigit() else d for d in entity.text]
        )
