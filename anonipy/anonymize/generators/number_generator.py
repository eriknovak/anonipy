import random
import warnings
from .interface import GeneratorInterface
from ...definitions import Entity

# =====================================
# Main class
# =====================================


class NumberGenerator(GeneratorInterface):

    def __init__(self, *args, **kwargs):
        pass

    def generate(self, entity: Entity, *args, **kwargs):
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
