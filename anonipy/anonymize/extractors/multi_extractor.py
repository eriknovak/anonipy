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

    def __init__(self, extractors: List[ExtractorInterface]):
        """
        Parameters
        ----------
        extractors : List[ExtractorInterface]
            The list of extractors

        """

        self.extractors = extractors

    def __call__(
        self, text: str
    ) -> Tuple[List[Tuple[Doc, List[Entity]]], List[Entity]]:
        """Extract the entities from the text

        Parameters
        ----------
        text : str
            The text to extract entities from

        Returns
        -------
        Tuple[List[Tuple[Doc, List[Entity]]], List[Entity]]
            The touple containing the list of extractor outputs (doc, entities)
            and the list of joint entities

        """

        extractor_outputs = [e(text) for e in self.extractors]
        joint_entities = self._merge_entities(extractor_outputs)
        return extractor_outputs, joint_entities

    def display(self, doc: Doc) -> str:
        """Display the entities in the text

        Parameters
        ----------
        doc : Doc
            The spacy doc to display

        Returns
        -------
        str
            The html representation of the doc

        """

        labels = list(
            itertools.chain.from_iterable([e.labels for e in self.extractors])
        )
        options = {"colors": {l["label"]: get_label_color(l["label"]) for l in labels}}
        return displacy.render(doc, style="ent", options=options)

    def _merge_entities(
        self, extractor_outputs: List[Tuple[Doc, List[Entity]]]
    ) -> List[Entity]:
        """Merges the entities returned by the extractors

        Parameters
        ----------
        extractor_outputs : List[Tuple[Doc, List[Entity]]]
            The list of extractor outputs

        Returns
        -------
        List[Entity]
            The merged entities

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
        """Filters the entities based on their start and end indices

        Parameters
        ----------
        entities : Iterable[Entity]
            The entities to filter

        Returns
        -------
        List[Entity]
            The filtered entities

        """

        get_sort_key = lambda entity: (
            entity.end_index - entity.start_index,
            -entity.start_index,
        )
        sorted_entities = sorted(entities, key=get_sort_key, reverse=True)
        result = []
        seen_tokens: Set[int] = set()
        for entities in sorted_entities:
            # Check for end - 1 here because boundaries are inclusive
            if (
                entities.start_index not in seen_tokens
                and entities.end_index - 1 not in seen_tokens
            ):
                result.append(entities)
                seen_tokens.update(range(entities.start_index, entities.end_index))
        result = sorted(result, key=lambda entity: entity.start_index)
        return result
