"""Shared fixtures and configuration for the test suite."""

from types import SimpleNamespace

import pytest

from anonipy.utils import gliner_spacy

try:
    import torch

    HAS_GPU = torch.cuda.is_available()
except ImportError:
    HAS_GPU = False

# =====================================
# Test Data
# =====================================

# phrases the fake GLiNER model tags, with the label it gives each
FAKE_GLINER_PHRASES = {
    "John Doe": "name",
    "15-01-1985": "date of birth",
    "123-45-6789": "social security number",
    # fails the date regex, so the NER extractor must drop it
    "Medical Record": "date",
}

FAKE_GLINER_SCORE = 0.9


# =====================================
# Fake GLiNER Model
# =====================================


class FakeGLiNER:
    """Stands in for a GLiNER model by tagging the first occurrence of each known phrase."""

    def predict_entities(self, text, labels, flat_ner=True, threshold=0.5):
        entities = []
        for phrase, label in FAKE_GLINER_PHRASES.items():
            start = text.find(phrase)
            if label in labels and start >= 0:
                end = start + len(phrase)
                entities.append({"start": start, "end": end, "label": label, "score": FAKE_GLINER_SCORE})
        return entities


@pytest.fixture
def fake_gliner(monkeypatch):
    """Replace GLiNER model loading with the fake; returns the keyword arguments of each load."""

    loads = []

    def from_pretrained(model_name, **kwargs):
        loads.append({"model_name": model_name, **kwargs})
        return FakeGLiNER()

    monkeypatch.setattr(gliner_spacy, "GLiNER", SimpleNamespace(from_pretrained=from_pretrained))
    return loads
