from typing import List, Tuple

from spacy.tokens import Doc
from ...definitions import Entity


class ExtractorInterface:
    """The class representing the extractor interface.

    All extractors should inherit from this class.

    Methods:
        __call__(text):
            Extract entities from the text.

    """

    def __init__(self, labels: List[dict], *args, **kwargs):
        pass

    def __call__(self, text: str, *args, **kwargs) -> Tuple[Doc, List[Entity]]:
        pass
