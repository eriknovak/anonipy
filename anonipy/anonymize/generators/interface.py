from ...definitions import Entity


# =====================================
# Main functions
# =====================================


class GeneratorInterface:
    """The class representing the generator interface."""

    def __init__(self, *args, **kwargs):
        pass

    def generate(self, entity: Entity, *args, **kwargs):
        pass
