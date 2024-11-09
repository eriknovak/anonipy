import re
import warnings
import importlib
from typing import List, Tuple

import torch
from spacy import displacy
from spacy.tokens import Doc, Span
from spacy.language import Language

from ..helpers import convert_spacy_to_entity
from ...utils.regex import regex_mapping
from ...constants import LANGUAGES
from ...definitions import Entity
from ...utils.colors import get_label_color

from .interface import ExtractorInterface

# ===============================================
# Extractor class
# ===============================================


class NERExtractor(ExtractorInterface):
    """The class representing the named entity recognition (NER) extractor.

    Examples:
        >>> from anonipy.constants import LANGUAGES
        >>> from anonipy.anonymize.extractors import NERExtractor
        >>> labels = [{"label": "PERSON", "type": "string"}]
        >>> extractor = NERExtractor(labels, lang=LANGUAGES.ENGLISH)
        >>> extractor("John Doe is a 19 year old software engineer.")
        Doc, [Entity]

    Attributes:
        labels (List[dict]): The list of labels to extract.
        lang (str): The language of the text to extract.
        score_th (float): The score threshold.
        use_gpu (bool): Whether to use GPU.
        gliner_model (str): The gliner model to use.
        pipeline (Language): The spacy pipeline for extracting entities.
        spacy_style (str): The style the entities should be stored in the spacy doc.

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
        score_th: float = 0.5,
        use_gpu: bool = False,
        gliner_model: str = "urchade/gliner_multi_pii-v1",
        spacy_style: str = "ent",
        **kwargs,
    ):
        """Initialize the named entity recognition (NER) extractor.

        Examples:
            >>> from anonipy.constants import LANGUAGES
            >>> from anonipy.anonymize.extractors import NERExtractor
            >>> labels = [{"label": "PERSON", "type": "string"}]
            >>> extractor = NERExtractor(labels, lang=LANGUAGES.ENGLISH)
            NERExtractor()

        Args:
            labels: The list of labels to extract.
            lang: The language of the text to extract.
            score_th: The score threshold. Entities with a score below this threshold will be ignored.
            use_gpu: Whether to use GPU.
            gliner_model: The gliner model to use to identify the entities.
            spacy_style: The style the entities should be stored in the spacy doc. Options: `ent` or `span`.

        """

        super().__init__(labels, *args, **kwargs)
        self.lang = lang
        self.score_th = score_th
        self.use_gpu = use_gpu
        self.gliner_model = gliner_model
        self.spacy_style = spacy_style
        self.labels = self._prepare_labels(labels)
        self.pipeline = self._prepare_pipeline()

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
        anoni_entities, spacy_entities = self._prepare_entities(doc)
        self._set_spacy_fields(doc, spacy_entities)
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

    def _prepare_labels(self, labels: List[dict]) -> List[dict]:
        """Prepare the labels for the extractor.

        The provided labels are enriched with the corresponding regex
        definitions, if the `regex` key was not provided.

        Args:
            labels: The list of labels to prepare.

        Returns:
            The enriched labels.

        """
        for l in labels:
            if "regex" in l:
                continue
            regex = regex_mapping[l["type"]]
            if regex is not None:
                l["regex"] = regex
        return labels

    def _create_gliner_config(self) -> dict:
        """Create the config for the GLINER model.

        Returns:
            The configuration dictionary for the GLINER model.

        """

        map_location = "cpu"
        if self.use_gpu and not torch.cuda.is_available():
            return warnings.warn(
                "The user requested GPU use, but not available GPU was found. Reverting back to CPU use."
            )
        if self.use_gpu and torch.cuda.is_available():
            map_location = "cuda"

        return {
            # the model is specialized for extracting PII data
            "gliner_model": self.gliner_model,
            "labels": [l["label"] for l in self.labels],
            "threshold": self.score_th,
            "chunk_size": 384,
            "style": self.spacy_style,
            "map_location": map_location,
        }

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
        gliner_config = self._create_gliner_config()
        nlp.add_pipe("gliner_spacy", config=gliner_config)
        return nlp

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
        for s in self._get_spacy_fields(doc):
            label = list(filter(lambda x: x["label"] == s.label_, self.labels))[0]
            if re.match(label["regex"], s.text):
                anoni_entities.append(convert_spacy_to_entity(s, **label))
                spacy_entities.append(s)
        return anoni_entities, spacy_entities

    def _get_spacy_fields(self, doc: Doc) -> List[Span]:
        """Get the spacy doc entity spans.

        args:
            doc: The spacy doc to get the entity spans from.

        Returns:
            The list of Spans from the spacy doc.

        """

        if self.spacy_style == "ent":
            return doc.ents
        elif self.spacy_style == "span":
            return doc.spans["sc"]
        else:
            raise ValueError(f"Invalid spacy style: {self.spacy_style}")

    def _set_spacy_fields(self, doc: Doc, entities: List[Span]) -> None:
        """Set the spacy doc entity spans.

        Args:
            doc: The spacy doc to set the entity spans.
            entities: The entity spans to set.

        Returns:
            None

        """

        if self.spacy_style == "ent":
            doc.ents = entities
        elif self.spacy_style == "span":
            doc.spans["sc"] = entities
        else:
            raise ValueError(f"Invalid spacy style: {self.spacy_style}")
