from typing import List
from ...definitions import Entity

# =====================================
# Main class
# =====================================


class StrategyInterface:
    """The class representing the strategy interface.

    Methods:
        anonymize(text, entities):
            Anonymize the text based on the entities.

    """

    def __init__(self, *args, **kwargs):
        pass

    def anonymize(self, text: str, entities: List[Entity], *args, **kwargs):
        pass
