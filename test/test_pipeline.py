import os
import shutil
import warnings

import pytest
from transformers import logging

from anonipy.anonymize.pipeline import Pipeline
from anonipy.anonymize.extractors import NERExtractor, PatternExtractor, MultiExtractor
from anonipy.anonymize.strategies import RedactionStrategy
from anonipy.constants import LANGUAGES

# disable transformers logging
logging.set_verbosity_error()

# =====================================
# Test Pipeline
# =====================================


@pytest.fixture(autouse=True)
def suppress_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)


@pytest.fixture(scope="module")
def setup():
    ner_labels = [{"label": "PERSON", "type": "string"}]
    pattern_labels = [{"label": "DATE", "type": "regex", "regex": r"\d{4}-\d{2}-\d{2}"}]
    extractors = [
        NERExtractor(ner_labels, lang=LANGUAGES.ENGLISH),
        PatternExtractor(pattern_labels, lang=LANGUAGES.ENGLISH),
    ]
    multi_extractor = MultiExtractor(extractors)
    strategy = RedactionStrategy()
    input_dir = "test/resources"
    output_dir = "test/output"
    yield extractors, multi_extractor, strategy, input_dir, output_dir
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)


def test_init():
    with pytest.raises(TypeError):
        Pipeline()


def test_init_extractor_single(setup):
    extractors, _, strategy, _, _ = setup
    pipeline = Pipeline(extractors[0], strategy)
    assert isinstance(pipeline, Pipeline)


def test_init_extractor_list(setup):
    extractors, _, strategy, _, _ = setup
    pipeline = Pipeline(extractors, strategy)
    assert isinstance(pipeline, Pipeline)


def test_init_extractor_multi(setup):
    _, multi_extractor, strategy, _, _ = setup
    pipeline = Pipeline(multi_extractor, strategy)
    assert isinstance(pipeline, Pipeline)


def test_methods(setup):
    _, multi_extractor, strategy, _, _ = setup
    pipeline = Pipeline(multi_extractor, strategy)
    assert hasattr(pipeline, "anonymize")


def test_anonymize(setup):
    _, multi_extractor, strategy, input_dir, output_dir = setup
    pipeline = Pipeline(multi_extractor, strategy)
    pipeline.anonymize(input_dir, output_dir)

    assert os.path.exists(output_dir)
    for root, _, files in os.walk(output_dir):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                assert f.read()


def test_anonymize_flatten(setup):
    _, multi_extractor, strategy, input_dir, output_dir = setup
    pipeline = Pipeline(multi_extractor, strategy)
    pipeline.anonymize(input_dir, output_dir, flatten=True)

    assert os.path.exists(output_dir)
    for root, _, files in os.walk(output_dir):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                assert f.read()


def test_anonymize_invalid_input_dir(setup):
    _, multi_extractor, strategy, _, output_dir = setup
    pipeline = Pipeline(multi_extractor, strategy)
    with pytest.raises(ValueError):
        pipeline.anonymize("invalid", output_dir)


def test_anonymize_invalid_output_dir(setup):
    _, multi_extractor, strategy, input_dir, _ = setup
    pipeline = Pipeline(multi_extractor, strategy)
    with pytest.raises(ValueError):
        pipeline.anonymize(input_dir, input_dir)
