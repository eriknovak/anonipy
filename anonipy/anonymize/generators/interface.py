from ...definitions import Entity


# =====================================
# Main functions
# =====================================


class GeneratorInterface:
    """The class representing the generator interface.

    All generators should inherit from this class.

    Methods:
        generate(entity):
            Generate a substitute for the entity.

    """

    def __init__(self, *args, **kwargs):
        pass

    def generate(self, entity: Entity, *args, **kwargs):
        pass
