import re

import importlib
from typing import List, Tuple, Optional, Callable

from spacy import displacy, util
from spacy.tokens import Doc, Span
from spacy.language import Language
from spacy.matcher import Matcher

from ..helpers import convert_spacy_to_entity
from ...constants import LANGUAGES
from ...definitions import Entity
from ...utils.colors import get_label_color

from .interface import ExtractorInterface


# ===============================================
# Extractor class
# ===============================================


class PatternExtractor(ExtractorInterface):
    """The class representing the pattern extractor.

    Examples:
        >>> from anonipy.constants import LANGUAGES
        >>> from anonipy.anonymize.extractors import PatternExtractor
        >>> labels = [{"label": "PERSON", "type": "string", "regex": "([A-Z][a-z]+ [A-Z][a-z]+)"}]
        >>> extractor = PatternExtractor(labels, lang=LANGUAGES.ENGLISH)
        >>> extractor("John Doe is a 19 year old software engineer.")
        Doc, [Entity]

    Attributes:
        labels (List[dict]): The list of labels and patterns to extract.
        lang (str): The language of the text to extract.
        pipeline (Language): The spacy pipeline for extracting entities.
        token_matchers (Matcher): The spacy token pattern matcher.
        global_matchers (function): The global pattern matcher.

    Methods:
        __call__(self, text):
            Extract the entities from the text.
        display(self, doc):
            Display the entities in the text.

    """

    def __init__(
        self,
        labels: List[dict],
        *args,
        lang: LANGUAGES = LANGUAGES.ENGLISH,
        spacy_style: str = "ent",
        **kwargs,
    ):
        """Initialize the pattern extractor.

        Examples:
            >>> from anonipy.constants import LANGUAGES
            >>> from anonipy.anonymize.extractors import PatternExtractor
            >>> labels = [{"label": "PERSON", "type": "string", "regex": "([A-Z][a-z]+ [A-Z][a-z]+)"}]
            >>> extractor = PatternExtractor(labels, lang=LANGUAGES.ENGLISH)
            PatternExtractor()

        Args:
            labels: The list of labels and patterns to extract.
            lang: The language of the text to extract.
            spacy_style: The style the entities should be stored in the spacy doc. Options: `ent` or `span`.

        """

        super().__init__(labels, *args, **kwargs)
        self.lang = lang
        self.labels = labels
        self.spacy_style = spacy_style
        self.pipeline = self._prepare_pipeline()
        self.token_matchers = self._prepare_token_matchers()
        self.global_matchers = self._prepare_global_matchers()

    def __call__(self, text: str, *args, **kwargs) -> Tuple[Doc, List[Entity]]:
        """Extract the entities from the text.

        Examples:
            >>> extractor("John Doe is a 19 year old software engineer.")
            Doc, [Entity]

        Args:
            text: The text to extract entities from.

        Returns:
            The spacy document.
            The list of extracted entities.

        """

        doc = self.pipeline(text)
        self.token_matchers(doc) if self.token_matchers else None
        self.global_matchers(doc) if self.global_matchers else None
        anoni_entities, spacy_entities = self._prepare_entities(doc)
        self._set_doc_entity_spans(doc, spacy_entities)
        return doc, anoni_entities

    def display(self, doc: Doc, page: bool = False, jupyter: bool = None) -> str:
        """Display the entities in the text.

        Examples:
            >>> doc, entities = extractor("John Doe is a 19 year old software engineer.")
            >>> extractor.display(doc)
            HTML

        Args:
            doc: The spacy doc to display.
            page: Whether to display the doc in a web browser.
            jupyter: Whether to display the doc in a jupyter notebook.

        Returns:
            The HTML representation of the document and the extracted entities.

        """

        options = {
            "colors": {l["label"]: get_label_color(l["label"]) for l in self.labels}
        }
        return displacy.render(
            doc, style=self.spacy_style, options=options, page=page, jupyter=jupyter
        )

    # ===========================================
    # Private methods
    # ===========================================

    def _prepare_pipeline(self) -> Language:
        """Prepare the spacy pipeline.

        Prepares the pipeline for processing the text in the corresponding
        provided language.

        Returns:
            The spacy text processing and extraction pipeline.

        """

        # load the appropriate parser for the language
        module_lang, class_lang = self.lang[0].lower(), self.lang[1].lower().title()
        language_module = importlib.import_module(f"spacy.lang.{module_lang}")
        language_class = getattr(language_module, class_lang)
        # initialize the language parser
        nlp = language_class()
        nlp.add_pipe("sentencizer")
        return nlp

    def _prepare_token_matchers(self) -> Optional[Matcher]:
        """Prepare the token pattern matchers.

        Prepares the token pattern matchers for the provided labels.

        Returns:
            The spacy matcher object or None if no relevant labels are provided.

        """

        relevant_labels = list(filter(lambda l: "pattern" in l, self.labels))
        if len(relevant_labels) == 0:
            return None

        matcher = Matcher(self.pipeline.vocab)
        for label in relevant_labels:
            if isinstance(label["pattern"], list):
                on_match = self._create_add_event_ent(label["label"])
                matcher.add(label["label"], label["pattern"], on_match=on_match)
        return matcher

    def _prepare_global_matchers(self) -> Optional[Callable]:
        """Prepares the global pattern matchers.

        Prepares the global pattern matchers for the provided labels.

        Returns:
            The function used to match the patterns or None if no relevant labels are provided.

        """

        relevant_labels = list(filter(lambda l: "regex" in l, self.labels))
        if len(relevant_labels) == 0:
            return None

        def global_matchers(doc: Doc) -> None:
            for label in relevant_labels:
                for match in re.finditer(label["regex"], doc.text):
                    # define the entity span
                    start, end = match.span(1)
                    entity = doc.char_span(start, end, label=label["label"])
                    if not entity:
                        continue
                    entity._.score = 1.0
                    # add the entity to the previous entity list
                    prev_entities = self._get_doc_entity_spans(doc)
                    if self.spacy_style == "ent":
                        prev_entities = util.filter_spans(prev_entities + (entity,))
                    elif self.spacy_style == "span":
                        prev_entities.append(entity)
                    else:
                        raise ValueError(f"Invalid spacy style: {self.spacy_style}")
                    self._set_doc_entity_spans(doc, prev_entities)

        return global_matchers

    def _prepare_entities(self, doc: Doc) -> Tuple[List[Entity], List[Span]]:
        """Prepares the anonipy and spacy entities.

        Args:
            doc: The spacy doc to prepare.

        Returns:
            The list of anonipy entities.
            The list of spacy entities.

        """

        # TODO: make this part more generic
        anoni_entities = []
        spacy_entities = []
        for e in self._get_doc_entity_spans(doc):
            label = list(filter(lambda x: x["label"] == e.label_, self.labels))[0]
            anoni_entities.append(convert_spacy_to_entity(e, **label))
            spacy_entities.append(e)
        return anoni_entities, spacy_entities

    def _create_add_event_ent(self, label: str) -> Callable:
        """Create the add event entity function

        Args:
            label: The identified label entity.

        Returns:
            The function used to add the entity to the spacy doc.

        """

        def add_event_ent(matcher, doc, i, matches):
            # define the entity span
            _, start, end = matches[i]
            entity = Span(doc, start, end, label=label)
            if not entity:
                return
            entity._.score = 1.0
            # add the entity to the previous entity list
            prev_entities = self._get_doc_entity_spans(doc)
            if self.spacy_style == "ent":
                prev_entities = util.filter_spans(prev_entities + (entity,))
            elif self.spacy_style == "span":
                prev_entities.append(entity)
            else:
                raise ValueError(f"Invalid spacy style: {self.spacy_style}")
            self._set_doc_entity_spans(doc, prev_entities)

        return add_event_ent

    def _get_doc_entity_spans(self, doc: Doc) -> List[Span]:
        """Get the spacy doc entity spans.

        Args:
            doc: The spacy doc to get the entity spans from.

        Returns:
            The list of entity spans.

        """

        if self.spacy_style == "ent":
            return doc.ents
        if self.spacy_style == "span":
            if "sc" not in doc.spans:
                doc.spans["sc"] = []
            return doc.spans["sc"]
        raise ValueError(f"Invalid spacy style: {self.spacy_style}")

    def _set_doc_entity_spans(self, doc: Doc, entities: List[Span]) -> None:
        """Set the spacy doc entity spans.

        Args:
            doc: The spacy doc to set the entity spans.
            entities: The entity spans to assign the doc.

        """

        if self.spacy_style == "ent":
            doc.ents = entities
        elif self.spacy_style == "span":
            doc.spans["sc"] = entities
        else:
            raise ValueError(f"Invalid spacy style: {self.spacy_style}")
