"""Tests for anonipy.anonymize.pipeline."""

import os
import shutil
import warnings

import pytest
from transformers import logging

from anonipy.anonymize.extractors import MultiExtractor, NERExtractor, PatternExtractor
from anonipy.anonymize.pipeline import Pipeline
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
            with open(os.path.join(root, file)) as f:
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
            with open(os.path.join(root, file)) as f:
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


# =====================================
# Test Pipeline With Pattern Extraction
# =====================================


@pytest.fixture
def pattern_pipeline():
    labels = [{"label": "name", "type": "string", "regex": r"(John Doe)"}]
    return Pipeline(PatternExtractor(labels, lang=LANGUAGES.ENGLISH), RedactionStrategy())


@pytest.fixture
def input_dir(tmp_path):
    root = tmp_path / "input"
    (root / "nested").mkdir(parents=True)
    (root / "top.txt").write_text("Patient John Doe was examined.")
    (root / "nested" / "deep.txt").write_text("John Doe returned for a follow-up.")
    return root


def read_outputs(output_dir):
    return {path.relative_to(output_dir).as_posix(): path.read_text() for path in output_dir.rglob("*.txt")}


def test_pipeline_rejects_invalid_extractor():
    """Test that an extractor of the wrong type raises ValueError."""
    with pytest.raises(ValueError, match="Extractor"):
        Pipeline("extractor", RedactionStrategy())


def test_pipeline_rejects_invalid_strategy(pattern_pipeline):
    """Test that a strategy of the wrong type raises ValueError."""
    with pytest.raises(ValueError, match="Strategy"):
        Pipeline(pattern_pipeline.extractor, "strategy")


def test_pipeline_wraps_extractor_list_in_multi_extractor(pattern_pipeline):
    """Test that a list of extractors becomes a MultiExtractor."""
    pipeline = Pipeline([pattern_pipeline.extractor], RedactionStrategy())
    assert isinstance(pipeline.extractor, MultiExtractor)


def test_pipeline_anonymize_redacts_every_file(pattern_pipeline, input_dir, tmp_path):
    """Test that each input file gets a redacted copy listed in the returned mapping."""
    mapping = pattern_pipeline.anonymize(str(input_dir), str(tmp_path / "output"))
    assert set(mapping) == {os.path.join("input", "top.txt"), os.path.join("input", "nested", "deep.txt")}
    for output_path in mapping.values():
        text = (tmp_path / output_path).read_text()
        assert "[REDACTED]" in text
        assert "John Doe" not in text


def test_pipeline_anonymize_keeps_subfolders(pattern_pipeline, input_dir, tmp_path):
    """Test that outputs mirror the input folder structure."""
    pattern_pipeline.anonymize(str(input_dir), str(tmp_path / "output"))
    folders = {name.rpartition("/")[0] for name in read_outputs(tmp_path / "output")}
    assert folders == {"", "nested"}


def test_pipeline_anonymize_flatten_writes_to_output_root(pattern_pipeline, input_dir, tmp_path):
    """Test that flatten puts every output file in the output folder itself."""
    pattern_pipeline.anonymize(str(input_dir), str(tmp_path / "output"), flatten=True)
    assert sorted(read_outputs(tmp_path / "output")) == ["file1_anony.txt", "file2_anony.txt"]


@pytest.mark.parametrize(
    ("file_name", "content", "message"),
    [
        ("empty.txt", "", "empty"),
        ("no_names.txt", "Nobody is named here.", "Entity extraction"),
        ("table.csv", "John Doe", "Problems while processing"),
    ],
)
def test_pipeline_anonymize_skips_unusable_files(pattern_pipeline, tmp_path, file_name, content, message):
    """Test that empty, entity-free and unsupported files are skipped with a warning."""
    (tmp_path / "input").mkdir()
    (tmp_path / "input" / file_name).write_text(content)
    with pytest.warns(UserWarning, match=message):
        mapping = pattern_pipeline.anonymize(str(tmp_path / "input"), str(tmp_path / "output"))
    assert mapping == {}


def test_pipeline_anonymize_rejects_missing_input_dir(pattern_pipeline, tmp_path):
    """Test that a missing input folder raises ValueError."""
    with pytest.raises(ValueError, match="does not exist"):
        pattern_pipeline.anonymize(str(tmp_path / "missing"), str(tmp_path / "output"))


def test_pipeline_anonymize_rejects_output_equal_to_input(pattern_pipeline, input_dir):
    """Test that writing outputs into the input folder raises ValueError."""
    with pytest.raises(ValueError, match="cannot be the same"):
        pattern_pipeline.anonymize(str(input_dir), str(input_dir))
