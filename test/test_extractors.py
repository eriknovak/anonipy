import unittest
import warnings

import torch
from transformers import logging

from anonipy.definitions import Entity
from anonipy.anonymize.extractors import NERExtractor, PatternExtractor, MultiExtractor
from anonipy.constants import LANGUAGES

# disable transformers logging
logging.set_verbosity_error()

# =====================================
# Helper functions
# =====================================

original_text = """\
Medical Record

Patient Name: John Doe
Date of Birth: 15-01-1985
Date of Examination: 20-05-2024
Social Security Number: 123-45-6789

Examination Procedure:
John Doe underwent a routine physical examination. The procedure included measuring vital signs (blood pressure, heart rate, temperature), a comprehensive blood panel, and a cardiovascular stress test. The patient also reported occasional headaches and dizziness, prompting a neurological assessment and an MRI scan to rule out any underlying issues.

Medication Prescribed:

Ibuprofen 200 mg: Take one tablet every 6-8 hours as needed for headache and pain relief.
Lisinopril 10 mg: Take one tablet daily to manage high blood pressure.
Next Examination Date:
15-11-2024
"""

ner_entities = [
    Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
    ),
    Entity(
        text="15-01-1985",
        label="date of birth",
        start_index=54,
        end_index=64,
        type="date",
    ),
    Entity(
        text="20-05-2024",
        label="date",
        start_index=86,
        end_index=96,
        type="date",
    ),
    Entity(
        text="123-45-6789",
        label="social security number",
        start_index=121,
        end_index=132,
        type="custom",
        regex="[0-9]{3}-[0-9]{2}-[0-9]{4}",
    ),
    Entity(
        text="John Doe",
        label="name",
        start_index=157,
        end_index=165,
        type="string",
    ),
    Entity(
        text="15-11-2024",
        label="date",
        start_index=717,
        end_index=727,
        type="date",
    ),
]

pattern_entities = [
    Entity(
        text="15-01-1985",
        label="date",
        start_index=54,
        end_index=64,
        type="date",
    ),
    Entity(
        text="20-05-2024",
        label="date",
        start_index=86,
        end_index=96,
        type="date",
    ),
    Entity(
        text="blood pressure, heart rate, temperature",
        label="symptoms",
        start_index=254,
        end_index=293,
        type="string",
        regex="\\((.*)\\)",
    ),
    Entity(
        text="Ibuprofen 200 mg",
        label="medicine",
        start_index=533,
        end_index=549,
        type="string",
    ),
    Entity(
        text="Lisinopril 10 mg",
        label="medicine",
        start_index=623,
        end_index=639,
        type="string",
    ),
    Entity(
        text="15-11-2024",
        label="date",
        start_index=717,
        end_index=727,
        type="date",
    ),
]


# =====================================
# Test NER Extractor
# =====================================


class TestNERExtractor(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ImportWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        # define the labels to be extracted and anonymized
        self.labels = [
            {"label": "name", "type": "string"},
            {
                "label": "social security number",
                "type": "custom",
                "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}",
            },
            {"label": "date of birth", "type": "date"},
            {"label": "date", "type": "date"},
        ]

    def test_init(self):
        try:
            NERExtractor()
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_init_inputs(self):
        extractor = NERExtractor(
            labels=self.labels, lang=LANGUAGES.ENGLISH, score_th=0.5
        )
        self.assertEqual(extractor.__class__, NERExtractor)

    def test_init_gpu(self):
        if torch.cuda.is_available():
            extractor = NERExtractor(
                labels=self.labels, lang=LANGUAGES.ENGLISH, score_th=0.5, use_gpu=True
            )
            self.assertEqual(extractor.__class__, NERExtractor)

    def test_methods(self):
        extractor = NERExtractor(
            labels=self.labels, lang=LANGUAGES.ENGLISH, score_th=0.5
        )
        self.assertEqual(hasattr(extractor, "__call__"), True)
        self.assertEqual(hasattr(extractor, "display"), True)

    def test_extract_default_params(self):
        extractor = NERExtractor(labels=self.labels)
        _, entities = extractor(original_text)
        for p_entity, t_entity in zip(entities, ner_entities):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score >= 0.5, True)

    def test_extract_default_params_input(self):
        extractor = NERExtractor(
            labels=self.labels,
            lang=LANGUAGES.ENGLISH,
            gliner_model="urchade/gliner_multi_pii-v1",
            score_th=0.5,
        )
        _, entities = extractor(original_text)
        for p_entity, t_entity in zip(entities, ner_entities):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score >= 0.5, True)

    def test_extract_custom_params_input(self):
        extractor = NERExtractor(
            labels=self.labels,
            lang=LANGUAGES.ENGLISH,
            gliner_model="E3-JSI/gliner-multi-pii-domains-v1",
            score_th=0.5,
        )
        _, entities = extractor(original_text)
        for p_entity, t_entity in zip(entities, ner_entities):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score >= 0.5, True)


# =====================================
# Test Pattern Extractor
# =====================================


class TestPatternExtractor(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ImportWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        # define the labels to be extracted and anonymized
        self.labels = [
            {
                "label": "symptoms",
                "type": "string",
                "regex": r"\((.*)\)",  # symptoms are enclosed in parentheses
            },
            {
                "label": "medicine",
                "type": "string",
                "pattern": [[{"IS_ALPHA": True}, {"LIKE_NUM": True}, {"LOWER": "mg"}]],
            },
            {
                "label": "date",
                "type": "date",
                "pattern": [  # represent the date as a sequence of digits using spacy
                    [
                        {"SHAPE": "dd"},
                        {"TEXT": "-"},
                        {"SHAPE": "dd"},
                        {"TEXT": "-"},
                        {"SHAPE": "dddd"},
                    ]
                ],
            },
        ]

    def test_init(self):
        try:
            PatternExtractor()
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_init_inputs(self):
        extractor = PatternExtractor(labels=self.labels, lang=LANGUAGES.ENGLISH)
        self.assertEqual(extractor.__class__, PatternExtractor)

    def test_methods(self):
        extractor = PatternExtractor(labels=self.labels, lang=LANGUAGES.ENGLISH)
        self.assertEqual(hasattr(extractor, "__call__"), True)
        self.assertEqual(hasattr(extractor, "display"), True)

    def test_extract_default(self):
        extractor = PatternExtractor(labels=self.labels, lang=LANGUAGES.ENGLISH)
        doc, entities = extractor(original_text)
        for p_entity, t_entity in zip(entities, pattern_entities):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score == 1.0, True)


class TestMultiExtractor(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore", category=ImportWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", category=FutureWarning)
        # define the labels to be extracted and anonymized
        self.ner_labels = [
            {"label": "name", "type": "string"},
            {
                "label": "social security number",
                "type": "custom",
                "regex": "[0-9]{3}-[0-9]{2}-[0-9]{4}",
            },
            {"label": "date of birth", "type": "date"},
            {"label": "date", "type": "date"},
        ]
        self.pattern_labels = [
            {
                "label": "symptoms",
                "type": "string",
                "regex": r"\((.*)\)",  # symptoms are enclosed in parentheses
            },
            {
                "label": "medicine",
                "type": "string",
                "pattern": [[{"IS_ALPHA": True}, {"LIKE_NUM": True}, {"LOWER": "mg"}]],
            },
            {
                "label": "date",
                "type": "date",
                "pattern": [  # represent the date as a sequence of digits using spacy
                    [
                        {"SHAPE": "dd"},
                        {"TEXT": "-"},
                        {"SHAPE": "dd"},
                        {"TEXT": "-"},
                        {"SHAPE": "dddd"},
                    ]
                ],
            },
        ]

    def test_init(self):
        try:
            MultiExtractor()
        except Exception as e:
            self.assertRaises(TypeError, e)

    def test_init_inputs(self):
        extractors = [
            NERExtractor(labels=self.ner_labels, lang=LANGUAGES.ENGLISH),
            PatternExtractor(labels=self.pattern_labels, lang=LANGUAGES.ENGLISH),
        ]
        extractor = MultiExtractor(extractors)
        self.assertEqual(extractor.__class__, MultiExtractor)

    def test_methods(self):
        extractors = [
            NERExtractor(labels=self.ner_labels, lang=LANGUAGES.ENGLISH),
            PatternExtractor(labels=self.pattern_labels, lang=LANGUAGES.ENGLISH),
        ]
        extractor = MultiExtractor(extractors)
        self.assertEqual(hasattr(extractor, "__call__"), True)
        self.assertEqual(hasattr(extractor, "display"), True)

    def test_extract_default(self):
        extractors = [
            NERExtractor(labels=self.ner_labels, lang=LANGUAGES.ENGLISH),
            PatternExtractor(labels=self.pattern_labels, lang=LANGUAGES.ENGLISH),
        ]
        extractor = MultiExtractor(extractors)
        extractor_outputs, joint_entities = extractor(original_text)

        # check the performance of the first extractor
        for p_entity, t_entity in zip(extractor_outputs[0][1], ner_entities):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score >= 0.5, True)

        # check the performance of the second extractor
        for p_entity, t_entity in zip(extractor_outputs[1][1], pattern_entities):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score == 1.0, True)

        # check the performance of the joint entities generation
        for p_entity, t_entity in zip(
            joint_entities, extractor._filter_entities(ner_entities + pattern_entities)
        ):
            self.assertEqual(p_entity.text, t_entity.text)
            self.assertEqual(p_entity.label, t_entity.label)
            self.assertEqual(p_entity.start_index, t_entity.start_index)
            self.assertEqual(p_entity.end_index, t_entity.end_index)
            self.assertEqual(p_entity.type, t_entity.type)
            self.assertEqual(p_entity.regex, t_entity.regex)
            self.assertEqual(p_entity.score >= 0.5, True)


if __name__ == "__main__":
    unittest.main()
