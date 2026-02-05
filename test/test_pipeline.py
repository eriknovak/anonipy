"""Tests for anonipy.anonymize.pipeline."""

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
    """Test that Pipeline requires arguments."""
    with pytest.raises(TypeError):
        Pipeline()


@pytest.mark.slow
@pytest.mark.integration
def test_init_extractor_single(setup):
    """Test Pipeline initialization with a single extractor."""
    extractors, _, strategy, _, _ = setup
    pipeline = Pipeline(extractors[0], strategy)
    assert isinstance(pipeline, Pipeline)


@pytest.mark.slow
@pytest.mark.integration
def test_init_extractor_list(setup):
    """Test Pipeline initialization with a list of extractors."""
    extractors, _, strategy, _, _ = setup
    pipeline = Pipeline(extractors, strategy)
    assert isinstance(pipeline, Pipeline)


@pytest.mark.slow
@pytest.mark.integration
def test_init_extractor_multi(setup):
    """Test Pipeline initialization with MultiExtractor."""
    _, multi_extractor, strategy, _, _ = setup
    pipeline = Pipeline(multi_extractor, strategy)
    assert isinstance(pipeline, Pipeline)


@pytest.mark.slow
@pytest.mark.integration
def test_methods(setup):
    """Test that Pipeline has anonymize method."""
    _, multi_extractor, strategy, _, _ = setup
    pipeline = Pipeline(multi_extractor, strategy)
    assert hasattr(pipeline, "anonymize")


@pytest.mark.slow
@pytest.mark.integration
def test_anonymize(setup):
    """Test Pipeline anonymization of files."""
    _, multi_extractor, strategy, input_dir, output_dir = setup
    pipeline = Pipeline(multi_extractor, strategy)
    pipeline.anonymize(input_dir, output_dir)

    assert os.path.exists(output_dir)
    for root, _, files in os.walk(output_dir):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                assert f.read()


@pytest.mark.slow
@pytest.mark.integration
def test_anonymize_flatten(setup):
    """Test Pipeline anonymization with flatten option."""
    _, multi_extractor, strategy, input_dir, output_dir = setup
    pipeline = Pipeline(multi_extractor, strategy)
    pipeline.anonymize(input_dir, output_dir, flatten=True)

    assert os.path.exists(output_dir)
    for root, _, files in os.walk(output_dir):
        for file in files:
            with open(os.path.join(root, file), "r") as f:
                assert f.read()


@pytest.mark.slow
@pytest.mark.integration
def test_anonymize_invalid_input_dir(setup):
    """Test Pipeline with invalid input directory."""
    _, multi_extractor, strategy, _, output_dir = setup
    pipeline = Pipeline(multi_extractor, strategy)
    with pytest.raises(ValueError):
        pipeline.anonymize("invalid", output_dir)


@pytest.mark.slow
@pytest.mark.integration
def test_anonymize_invalid_output_dir(setup):
    """Test Pipeline with input dir as output dir."""
    _, multi_extractor, strategy, input_dir, _ = setup
    pipeline = Pipeline(multi_extractor, strategy)
    with pytest.raises(ValueError):
        pipeline.anonymize(input_dir, input_dir)
