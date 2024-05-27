import re
import importlib
from typing import List, Tuple

from spacy import displacy
from spacy.tokens import Doc
from gliner_spacy.pipeline import GlinerSpacy

from ..helpers import convert_spacy_to_entity
from ..regex import regex_map
from ...constants import LANGUAGES
from ...definitions import Entity

from .interface import ExtractorInterface


class EntityExtractor(ExtractorInterface):

    def __init__(
        self,
        labels: List[dict],
        lang: LANGUAGES = LANGUAGES.ENGLISH,
        score_th=0.5,
    ):
        self.lang = lang
        self.score_th = score_th
        self.labels = self._prepare_labels(labels)
        self.pipeline = self._prepare_pipeline()

    def __call__(self, text: str) -> Tuple[Doc, List[Entity]]:
        doc = self.pipeline(text)
        entities, doc.ents = self._prepare_entities(doc)
        return doc, entities

    def display(self, doc: Doc):
        options = {"colors": {l["label"]: "#5C7AEA" for l in self.labels}}
        displacy.render(doc, style="ent", options=options)

    # ===========================================
    # Private methods
    # ===========================================

    def _prepare_labels(self, labels):
        for l in labels:
            if "regex" in l:
                continue
            regex = regex_map(l["type"])
            if regex is not None:
                l["regex"] = regex
        return labels

    def _create_gliner_config(self):
        return {
            # the model is specialized for extracting PII data
            "gliner_model": "urchade/gliner_multi_pii-v1",
            "labels": [l["label"] for l in self.labels],
            "threshold": self.score_th,
            "chunk_size": 384,
            "style": "ent",
        }

    def _prepare_pipeline(self):
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

    def _prepare_entities(self, doc):
        # prepares the anonymized and spacy entities

        # TODO: make this part more generic
        anoni_entities = []
        spacy_entities = []
        for e in doc.ents:
            label = list(filter(lambda x: x["label"] == e.label_, self.labels))[0]
            if re.match(label["regex"], e.text):
                anoni_entities.append(convert_spacy_to_entity(e, **label))
                spacy_entities.append(e)
        return anoni_entities, spacy_entities
