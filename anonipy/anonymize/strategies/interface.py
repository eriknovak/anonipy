"""
Contains the interface for the strategy
"""

from typing import List
from ...definitions import Entity

# =====================================
# Main class
# =====================================


class StrategyInterface:

    def __init__(self, *args, **kwargs):
        pass

    def anonymize(self, text: str, entities: List[Entity], *args, **kwargs):
        pass
