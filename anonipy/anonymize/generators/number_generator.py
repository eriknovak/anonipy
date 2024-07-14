import random
import warnings
from .interface import GeneratorInterface
from ...definitions import Entity

# =====================================
# Main class
# =====================================


class NumberGenerator(GeneratorInterface):
    """The class representing the number generator.

    Examples:
        >>> from anonipy.anonymize.generators import NumberGenerator
        >>> generator = NumberGenerator()
        >>> generator.generate(entity)

    Methods:
        generate(self, entity):
            Generates a substitute for the numeric entity.

    """

    def __init__(self, *args, **kwargs):
        """Initializes the number generator.

        Examples:
            >>> from anonipy.anonymize.generators import NumberGenerator
            >>> generator = NumberGenerator()

        """

        super().__init__(*args, **kwargs)

    def generate(self, entity: Entity, *args, **kwargs) -> str:
        """Generates the substitute for the numeric entity.

        Examples:
            >>> from anonipy.anonymize.generators import NumberGenerator
            >>> generator = NumberGenerator()
            >>> generator.generate(entity)
            "1234567890"

        Args:
            entity: The numeric entity to generate the numeric substitute.

        Returns:
            The generated numeric substitute.

        Raises:
            ValueError: If the entity type is not `integer`, `float`, `phone_number` or `custom`.

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
