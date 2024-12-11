import os
import unittest
import shutil

from transformers import logging

from anonipy.anonymize.pipeline import Pipeline
from anonipy.anonymize.extractors import NERExtractor, PatternExtractor, MultiExtractor
from anonipy.anonymize.strategies import RedactionStrategy
from anonipy.constants import LANGUAGES

# disable transformers logging
logging.set_verbosity_error()

# =====================================
# Helper functions
# =====================================


# =====================================
# Test Pipeline
# =====================================


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.ner_labels = [{"label": "PERSON", "type": "string"}]
        self.pattern_labels = [
            {"label": "DATE", "type": "regex", "regex": r"\d{4}-\d{2}-\d{2}"}
        ]
        self.extractors = [
            NERExtractor(self.ner_labels, lang=LANGUAGES.ENGLISH),
            PatternExtractor(self.pattern_labels, lang=LANGUAGES.ENGLISH),
        ]
        self.multi_extractor = MultiExtractor(self.extractors)
        self.strategy = RedactionStrategy()
        self.input_dir = "test/resources"
        self.output_dir = "test/output"

    def tearDown(self):
        if not os.path.exists(self.output_dir):
            return
        # remove the output directory
        shutil.rmtree(self.output_dir)

    def test_init(self):
        with self.assertRaises(TypeError):
            Pipeline()

    def test_init_extractor_single(self):
        pipeline = Pipeline(self.extractors[0], self.strategy)
        self.assertEqual(pipeline.__class__, Pipeline)

    def test_init_extractor_list(self):
        pipeline = Pipeline(self.extractors, self.strategy)
        self.assertEqual(pipeline.__class__, Pipeline)

    def test_init_extractor_multi(self):
        pipeline = Pipeline(self.multi_extractor, self.strategy)
        self.assertEqual(pipeline.__class__, Pipeline)

    def test_methods(self):
        pipeline = Pipeline(self.multi_extractor, self.strategy)
        self.assertTrue(hasattr(pipeline, "anonymize"))

    def test_anonymize(self):
        pipeline = Pipeline(self.multi_extractor, self.strategy)
        pipeline.anonymize(self.input_dir, self.output_dir)

        self.assertTrue(os.path.exists(self.output_dir))
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                with open(os.path.join(root, file), "r") as f:
                    self.assertTrue(f.read())

    def test_anonymize_flatten(self):
        pipeline = Pipeline(self.multi_extractor, self.strategy)
        pipeline.anonymize(self.input_dir, self.output_dir, flatten=True)

        self.assertTrue(os.path.exists(self.output_dir))
        for root, _, files in os.walk(self.output_dir):
            for file in files:
                with open(os.path.join(root, file), "r") as f:
                    self.assertTrue(f.read())

    def test_anonymize_invalid_input_dir(self):
        pipeline = Pipeline(self.multi_extractor, self.strategy)
        with self.assertRaises(ValueError):
            pipeline.anonymize("invalid", self.output_dir)

    def test_anonymize_invalid_output_dir(self):
        pipeline = Pipeline(self.multi_extractor, self.strategy)
        with self.assertRaises(ValueError):
            pipeline.anonymize(self.input_dir, self.input_dir)


if __name__ == "__main__":
    unittest.main()
