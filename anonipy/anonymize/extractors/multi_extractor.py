from typing import List, Tuple
import itertools

from spacy import displacy
from spacy.tokens import Doc

from ...definitions import Entity
from ...utils.colors import get_label_color
from ..helpers import merge_entities

from .interface import ExtractorInterface


# ===============================================
# Extractor class
# ===============================================


class MultiExtractor:
    """The class representing the multi extractor.

    Examples:
        >>> from anonipy.constants import LANGUAGES
        >>> from anonipy.anonymize.extractors import NERExtractor, PatternExtractor, MultiExtractor
        >>> extractors = [
        >>>     NERExtractor(ner_labels, lang=LANGUAGES.ENGLISH),
        >>>     PatternExtractor(pattern_labels, lang=LANGUAGES.ENGLISH),
        >>> ]
        >>> extractor = MultiExtractor(extractors)
        >>> extractor("John Doe is a 19 year old software engineer.", detect_repeats=False)
        [(Doc, [Entity]), (Doc, [Entity])], [Entity]

    Attributes:
        extractors (List[ExtractorInterface]):
            The list of extractors to use.

    Methods:
        __call__(self, text):
            Extract the entities fron the text using the provided extractors.
        display(self, doc):
            Display the entities extracted from the text document.

    """

    def __init__(self, extractors: List[ExtractorInterface]):
        """Initialize the multi extractor.

        Examples:
            >>> from anonipy.constants import LANGUAGES
            >>> from anonipy.anonymize.extractors import NERExtractor, PatternExtractor, MultiExtractor
            >>> extractors = [
            >>>     NERExtractor(ner_labels, lang=LANGUAGES.ENGLISH),
            >>>     PatternExtractor(pattern_labels, lang=LANGUAGES.ENGLISH),
            >>> ]
            >>> extractor = MultiExtractor(extractors)
            MultiExtractor()

        Args:
            extractors: The list of extractors to use.

        """
        if len(extractors) == 0:
            raise ValueError("At least one extractor must be provided.")
        if not all(isinstance(e, ExtractorInterface) for e in extractors):
            raise ValueError("All extractors must be instances of ExtractorInterface.")

        self.extractors = extractors

    def __call__(
        self, text: str, detect_repeats: bool = False
    ) -> Tuple[List[Tuple[Doc, List[Entity]]], List[Entity]]:
        """Extract the entities fron the text using the provided extractors.

        Examples:
            >>> extractor("John Doe is a 19 year old software engineer.", detect_repeats=False)
            [(Doc, [Entity]), (Doc, [Entity])], [Entity]

        Args:
            text: The text to extract entities from.
            detect_repeats: Whether to check text again for repeated entities.

        Returns:
            The list of extractor outputs containing the tuple (spacy document, extracted entities).
            The list of joint entities.

        """

        extractor_outputs = [e(text, detect_repeats) for e in self.extractors]
        joint_entities = merge_entities(extractor_outputs)

        return extractor_outputs, joint_entities

    def display(self, doc: Doc, page: bool = False, jupyter: bool = None) -> str:
        """Display the entities in the text.

        Examples:
            >>> extractor_outputs, entities = extractor("John Doe is a 19 year old software engineer.")
            >>> extractor.display(extractor_outputs[0][0])
            HTML

        Args:
            doc: The spacy doc to display.
            page: Whether to display the doc in a web browser.
            jupyter: Whether to display the doc in a jupyter notebook.

        Returns:
            The HTML representation of the document and the extracted entities.

        """

        labels = list(
            itertools.chain.from_iterable([e.labels for e in self.extractors])
        )
        options = {"colors": {l["label"]: get_label_color(l["label"]) for l in labels}}
        return displacy.render(
            doc, style="ent", options=options, page=page, jupyter=jupyter
        )
