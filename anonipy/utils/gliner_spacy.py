"""Local spacy component for GLiNER entity extraction.

Replaces the external `gliner-spacy` package which has a bug where it
passes `load_tokenizer=False` to `GLiNER.from_pretrained()` for non-ONNX
models, preventing proper embedding resizing.
"""

from gliner import GLiNER
from spacy.language import Language
from spacy.tokens import Span

Span.set_extension("score", default=0, force=True)

DEFAULT_CONFIG = {
    "gliner_model": "urchade/gliner_base",
    "chunk_size": 250,
    "labels": ["person", "organization"],
    "style": "ent",
    "threshold": 0.5,
    "map_location": "cpu",
}


@Language.factory(
    "gliner_spacy",
    assigns=["doc.ents"],
    default_config=DEFAULT_CONFIG,
)
class GlinerSpacy:
    """Spacy pipeline component that uses GLiNER for entity extraction.

    Args:
        nlp: The spacy Language instance.
        name: The component name.
        gliner_model: The GLiNER model identifier.
        chunk_size: Max characters per text chunk.
        labels: Entity labels to detect.
        style: Storage style — "ent" for doc.ents, "span" for doc.spans.
        threshold: Minimum score threshold for entities.
        map_location: Device to load model on ("cpu" or "cuda").
    """

    def __init__(
        self,
        nlp: Language,
        name: str,
        gliner_model: str,
        chunk_size: int,
        labels: list,
        style: str,
        threshold: float,
        map_location: str,
    ):
        self.nlp = nlp
        self.model = GLiNER.from_pretrained(
            gliner_model,
            map_location=map_location,
        )
        self.labels = labels
        self.chunk_size = chunk_size
        self.style = style
        self.threshold = threshold

    def __call__(self, doc):
        """Process a spacy Doc through the GLiNER model."""

        # Chunk text on word boundaries
        text = doc.text
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            while end < len(text) and text[end] not in (" ", "\n"):
                end += 1
            chunks.append(text[start:end])
            start = end

        # Run prediction on each chunk
        all_entities = []
        offset = 0
        for chunk in chunks:
            flat_ner = self.style != "span"
            chunk_entities = self.model.predict_entities(
                chunk,
                self.labels,
                flat_ner=flat_ner,
                threshold=self.threshold,
            )
            for entity in chunk_entities:
                all_entities.append(
                    {
                        "start": offset + entity["start"],
                        "end": offset + entity["end"],
                        "label": entity["label"],
                        "score": entity["score"],
                    }
                )
            offset += len(chunk)

        # Create spacy spans and store on doc
        spans = []
        for ent in all_entities:
            span = doc.char_span(ent["start"], ent["end"], label=ent["label"])
            if span:
                span._.score = ent["score"]
                spans.append(span)

        if self.style == "span":
            doc.spans["sc"] = spans
        else:
            doc.ents = spans

        return doc
