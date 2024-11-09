from typing import List, Set, Tuple, Iterable

import itertools

from spacy import displacy
from spacy.tokens import Doc

from ...definitions import Entity
from ...utils.colors import get_label_color

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
        >>> extractor("John Doe is a 19 year old software engineer.")
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

        self.extractors = extractors

    def __call__(
        self, text: str
    ) -> Tuple[List[Tuple[Doc, List[Entity]]], List[Entity]]:
        """Extract the entities fron the text using the provided extractors.

        Examples:
            >>> extractor("John Doe is a 19 year old software engineer.")
            [(Doc, [Entity]), (Doc, [Entity])], [Entity]

        Args:
            text: The text to extract entities from.

        Returns:
            The list of extractor outputs containing the tuple (spacy document, extracted entities).
            The list of joint entities.
        """

        extractor_outputs = [e(text) for e in self.extractors]
        joint_entities = self._merge_entities(extractor_outputs)
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

    def _merge_entities(
        self, extractor_outputs: List[Tuple[Doc, List[Entity]]]
    ) -> List[Entity]:
        """Merges the entities returned by the extractors.

        Args:
            extractor_outputs: The list of extractor outputs.

        Returns:
            The merged entities list.

        """

        if len(extractor_outputs) == 0:
            return []
        if len(extractor_outputs) == 1:
            return extractor_outputs[1]

        joint_entities = self._filter_entities(
            list(
                itertools.chain.from_iterable(
                    [entity[1] for entity in extractor_outputs]
                )
            )
        )
        return joint_entities

    def _filter_entities(self, entities: Iterable[Entity]) -> List[Entity]:
        """Filters the entities based on their start and end indices.

        Args:
            entities: The entities to filter.

        Returns:
            The filtered entities.

        """

        def get_sort_key(entity):
            return (
                entity.end_index - entity.start_index,
                -entity.start_index,
            )

        sorted_entities = sorted(entities, key=get_sort_key, reverse=True)
        result = []
        seen_tokens: Set[int] = set()
        for entity in sorted_entities:
            # Check for end - 1 here because boundaries are inclusive
            if (
                entity.start_index not in seen_tokens
                and entity.end_index - 1 not in seen_tokens
            ):
                result.append(entity)
                seen_tokens.update(range(entity.start_index, entity.end_index))
        result = sorted(result, key=lambda entity: entity.start_index)
        return result
