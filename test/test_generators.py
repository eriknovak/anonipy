"""Tests for anonipy.anonymize.generators."""

import re
import warnings
from types import SimpleNamespace

import pytest
import torch
from transformers import logging

from anonipy.anonymize.generators import (
    DateGenerator,
    LLMLabelGenerator,
    MaskLabelGenerator,
    NumberGenerator,
)
from anonipy.anonymize.generators import llm_label_generator as llm_module
from anonipy.anonymize.generators import mask_label_generator as mask_module
from anonipy.definitions import Entity
from test.conftest import HAS_GPU

# disable transformers logging
logging.set_verbosity_error()

# =====================================
# Test Cases
# =====================================

DATETIME_STRS = [
    "2023-06-17 14:30:00",
    "17-06-2023 14:30:00",
    "06-17-2023 14:30:00",
    "2023/06/17 14:30:00",
    "17/06/2023 14:30:00",
    "06/17/2023 14:30:00",
    "2023.06.17 14:30:00",
    "17.06.2023 14:30:00",
    "06.17.2023 14:30:00",
    "2023 06 17 14:30:00",
    "17 06 2023 14:30:00",
    "06 17 2023 14:30:00",
    "2023-06-17 14:30",
    "17-06-2023 14:30",
    "06-17-2023 14:30",
    "2023/06/17 14:30",
    "17/06/2023 14:30",
    "06/17/2023 14:30",
    "2023.06.17 14:30",
    "17.06.2023 14:30",
    "06.17.2023 14:30",
    "2023 06 17 14:30",
    "17 06 2023 14:30",
    "06 17 2023 14:30",
    "2023-06-17 02:30 PM",
    "17-06-2023 02:30 PM",
    "06-17-2023 02:30 PM",
    "2023/06/17 02:30 PM",
    "17/06/2023 02:30 PM",
    "06/17/2023 02:30 PM",
    "2023.06.17 02:30 PM",
    "17.06.2023 02:30 PM",
    "06.17.2023 02:30 PM",
    "2023 06 17 02:30 PM",
    "17 06 2023 02:30 PM",
    "06 17 2023 02:30 PM",
    "June 17, 2023 14:30:00",
    "17 June 2023 14:30:00",
    "Jun 17, 2023 14:30:00",
    "17 Jun 2023 14:30:00",
    "June 17, 2023 02:30 PM",
    "17 June 2023 02:30 PM",
    "Jun 17, 2023 02:30 PM",
    "17 Jun 2023 02:30 PM",
    "Saturday, 17 June 2023 14:30:00",
    "Saturday, June 17, 2023 14:30:00",
    "Saturday, 17 June 2023 02:30 PM",
    "Saturday, June 17, 2023 02:30 PM",
    "2023-06-17",
    "17-06-2023",
    "06-17-2023",
    "2023/06/17",
    "17/06/2023",
    "06/17/2023",
    "2023.06.17",
    "17.06.2023",
    "06.17.2023",
    "2023 06 17",
    "17 06 2023",
    "06 17 2023",
    "June 17, 2023",
    "17 June 2023",
    "Jun 17, 2023",
    "17 Jun 2023",
    "Saturday, 17 June 2023",
    "Saturday, June 17, 2023",
]

# =====================================
# Test Data
# =====================================

TEST_ORIGINAL_TEXT = """\
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

TEST_ENTITIES = {
    "name": Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
    ),
    "name:pattern": Entity(
        text="John Doe",
        label="name",
        start_index=30,
        end_index=38,
        type="string",
        regex="Person: (.*)",
    ),
    "date": [
        Entity(
            text="20-05-2024",
            label="date",
            start_index=86,
            end_index=96,
            type="date",
        )
    ]
    + [
        Entity(
            text=str,
            label="date",
            start_index=86,
            end_index=86 + len(str),
            type="date",
        )
        for str in DATETIME_STRS
    ],
    "integer": Entity(
        text="123456789",
        label="integer",
        start_index=121,
        end_index=132,
        type="integer",
    ),
    "float": Entity(
        text="123,456,789.000",
        label="float",
        start_index=121,
        end_index=132,
        type="float",
    ),
    "custom": Entity(
        text="123-45-6789",
        label="custom",
        start_index=121,
        end_index=132,
        type="custom",
        regex="\\d{3}-\\d{2}-\\d{4}",
    ),
}

# =====================================
# Fake Models
# =====================================

PROMPT_IDS = torch.tensor([[11, 12, 13]])
REPLY_IDS = torch.tensor([[21, 22]])
FAKE_REPLY = "Jane Smith"
MASK_TOKEN = "<mask>"


class FakeCausalLM:
    """Stands in for a causal LM by appending fixed reply ids to the prompt."""

    device = torch.device("cpu")

    def __init__(self):
        self.generate_kwargs = {}

    def generate(self, input_ids, **kwargs):
        self.generate_kwargs = kwargs
        return torch.cat([input_ids, REPLY_IDS], dim=1)


class FakeChatTokenizer:
    """Stands in for a chat tokenizer: encodes any chat to fixed ids and decodes only the reply."""

    pad_token_id = None
    eos_token_id = 0

    def __init__(self):
        self.encoding = PROMPT_IDS
        self.messages = []

    def apply_chat_template(self, messages, **kwargs):
        self.messages = messages
        return self.encoding

    def decode(self, ids, skip_special_tokens=False):
        return FAKE_REPLY if torch.equal(ids, REPLY_IDS[0]) else "<prompt>"


class FakeMaskedLM:
    """Stands in for a masked LM; only the device move is called on it."""

    def to(self, device):
        return self


class FakeFillMask:
    """Stands in for a fill-mask pipeline, giving each masked input its own suggestions."""

    def __init__(self):
        self.suggestions = []
        self.inputs = []

    def __call__(self, inputs):
        self.inputs = inputs
        outputs = [[{"token_str": token} for token in tokens] for tokens in self.suggestions]
        # like transformers, a single input gets its suggestions unwrapped
        return outputs[0] if len(inputs) == 1 else outputs


@pytest.fixture
def fake_llm(monkeypatch):
    """Replace causal LM loading with fakes; returns the keyword arguments of each model load."""

    loads = []

    def load_model(model_name, **kwargs):
        loads.append({"model_name": model_name, **kwargs})
        return FakeCausalLM()

    monkeypatch.setattr(llm_module, "AutoModelForCausalLM", SimpleNamespace(from_pretrained=load_model))
    monkeypatch.setattr(
        llm_module, "AutoTokenizer", SimpleNamespace(from_pretrained=lambda *a, **k: FakeChatTokenizer())
    )
    return loads


@pytest.fixture
def fake_fill_mask(monkeypatch):
    """Replace the masked LM and its pipeline with fakes; returns the fake pipeline."""

    fill_mask = FakeFillMask()
    tokenizer = SimpleNamespace(mask_token=MASK_TOKEN)
    monkeypatch.setattr(
        mask_module, "AutoModelForMaskedLM", SimpleNamespace(from_pretrained=lambda *a, **k: FakeMaskedLM())
    )
    monkeypatch.setattr(mask_module, "AutoTokenizer", SimpleNamespace(from_pretrained=lambda *a, **k: tokenizer))
    monkeypatch.setattr(mask_module, "pipeline", lambda *a, **k: fill_mask)
    return fill_mask


# =====================================
# Test LLM Label Generator
# =====================================


@pytest.fixture(scope="module")
def llm_label_generator():
    return LLMLabelGenerator()


@pytest.mark.slow
def test_llm_label_generator_has_methods(llm_label_generator):
    """Test that LLMLabelGenerator has generate method."""
    assert hasattr(llm_label_generator, "generate")


@pytest.mark.slow
def test_llm_label_generator_generate_default(llm_label_generator):
    """Test LLM generation with default parameters."""
    entity = TEST_ENTITIES["name"]
    generated_text = llm_label_generator.generate(entity)
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


@pytest.mark.slow
def test_llm_label_generator_generate_custom(llm_label_generator):
    """Test LLM generation with custom entity attributes."""
    entity = TEST_ENTITIES["name"]
    generated_text = llm_label_generator.generate(entity, add_entity_attrs="Spanish", temperature=0.5)
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


@pytest.mark.slow
def test_llm_label_generator_generate_custom_user_prompt(llm_label_generator):
    """Test LLM generation with custom user prompt."""
    entity = TEST_ENTITIES["name"]
    generated_text = llm_label_generator.generate(
        entity, add_entity_attrs="Spanish", temperature=0.5, user_prompt="Respond with the text 'TEST' only."
    )
    assert "TEST" in generated_text


@pytest.mark.slow
def test_llm_label_generator_generate_custom_system_prompt(llm_label_generator):
    """Test LLM generation with custom system prompt."""
    entity = TEST_ENTITIES["name"]
    generated_text = llm_label_generator.generate(
        entity,
        add_entity_attrs="Spanish",
        temperature=0.5,
        system_prompt="You are a helpful AI assistant for replying 'TEST'.",
    )
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


@pytest.mark.slow
def test_llm_label_generator_generate_pattern(llm_label_generator):
    """Test LLM generation with pattern-based entity."""
    entity = TEST_ENTITIES["name:pattern"]
    generated_text = llm_label_generator.generate(entity)
    regex = entity.get_regex_group() or entity.regex
    match = re.match(regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


# =====================================
# Test LLM Label Generator With Fake Models
# =====================================


def test_llm_label_generator_fake_returns_only_the_reply(fake_llm):
    """Test that the generator decodes the new tokens, not the prompt."""
    generator = LLMLabelGenerator()
    assert generator.generate(TEST_ENTITIES["name"]) == FAKE_REPLY


def test_llm_label_generator_fake_fills_default_prompts(fake_llm):
    """Test that the default prompts carry the entity and its extra attributes."""
    generator = LLMLabelGenerator()
    generator.generate(TEST_ENTITIES["name"], add_entity_attrs="Spanish")
    system, user = generator.tokenizer.messages
    assert system["role"] == "system"
    assert user == {
        "role": "user",
        "content": "What is a random Spanish name replacement for John Doe? Respond only with the replacement.",
    }


def test_llm_label_generator_fake_uses_custom_prompts(fake_llm):
    """Test that custom prompts replace the defaults."""
    generator = LLMLabelGenerator()
    generator.generate(TEST_ENTITIES["name"], system_prompt="Be brief.", user_prompt="Replace {entity.text}.")
    assert generator.tokenizer.messages == [
        {"role": "system", "content": "Be brief."},
        {"role": "user", "content": "Replace John Doe."},
    ]


def test_llm_label_generator_fake_forwards_sampling_settings(fake_llm):
    """Test that temperature and top_p reach the model, with the pad token set to EOS."""
    generator = LLMLabelGenerator()
    generator.generate(TEST_ENTITIES["name"], temperature=0.3, top_p=0.8)
    kwargs = generator.model.generate_kwargs
    assert (kwargs["temperature"], kwargs["top_p"], kwargs["do_sample"]) == (0.3, 0.8, True)
    assert kwargs["pad_token_id"] == FakeChatTokenizer.eos_token_id


@pytest.mark.parametrize("encoding", [PROMPT_IDS, {"input_ids": PROMPT_IDS}], ids=["tensor", "batch_encoding"])
def test_llm_label_generator_fake_attends_to_all_prompt_tokens_by_default(fake_llm, encoding):
    """Test that a chat encoding without an attention mask attends to every token."""
    generator = LLMLabelGenerator()
    generator.tokenizer.encoding = encoding
    assert generator.generate(TEST_ENTITIES["name"]) == FAKE_REPLY
    assert torch.equal(generator.model.generate_kwargs["attention_mask"], torch.ones_like(PROMPT_IDS))


def test_llm_label_generator_fake_uses_the_tokenizer_attention_mask(fake_llm):
    """Test that an attention mask from the tokenizer reaches the model."""
    attention_mask = torch.tensor([[1, 1, 0]])
    generator = LLMLabelGenerator()
    generator.tokenizer.encoding = {"input_ids": PROMPT_IDS, "attention_mask": attention_mask}
    generator.generate(TEST_ENTITIES["name"])
    assert torch.equal(generator.model.generate_kwargs["attention_mask"], attention_mask)


def test_llm_label_generator_fake_loads_model_on_cpu(fake_llm):
    """Test that the default load is full precision on the CPU, without quantization."""
    LLMLabelGenerator(model_name="some/llm")
    assert fake_llm == [{"model_name": "some/llm", "device_map": torch.device("cpu"), "torch_dtype": torch.float32}]


@pytest.mark.skipif(HAS_GPU, reason="GPU available")
def test_llm_label_generator_fake_gpu_without_cuda_falls_back_to_cpu(fake_llm):
    """Test that requesting a missing GPU warns and loads on the CPU."""
    with pytest.warns(UserWarning, match="GPU/CUDA"):
        LLMLabelGenerator(use_gpu=True)
    assert fake_llm[0]["device_map"] == torch.device("cpu")


def test_llm_label_generator_fake_quant_without_extra_is_disabled(fake_llm, monkeypatch):
    """Test that quantization without the quant extra warns and loads unquantized."""
    monkeypatch.setattr(llm_module, "is_installed_with", lambda extra: False)
    with pytest.warns(UserWarning, match="'quant' extra"):
        LLMLabelGenerator(use_quant=True)
    assert "quantization_config" not in fake_llm[0]


@pytest.mark.skipif(HAS_GPU, reason="GPU available")
def test_llm_label_generator_fake_quant_on_cpu_is_disabled(fake_llm):
    """Test that quantization on the CPU warns and loads unquantized."""
    with pytest.warns(UserWarning, match="only supported on GPU"):
        LLMLabelGenerator(use_quant=True)
    assert "quantization_config" not in fake_llm[0]


def test_llm_label_generator_fake_quant_on_gpu_loads_8bit(fake_llm, monkeypatch):
    """Test that quantization on a GPU loads the model in 8-bit half precision."""
    monkeypatch.setattr(torch.cuda, "is_available", lambda: True)
    monkeypatch.setattr(llm_module, "is_installed_with", lambda extra: True)
    monkeypatch.setattr(llm_module, "BitsAndBytesConfig", lambda **kwargs: kwargs)
    LLMLabelGenerator(use_gpu=True, use_quant=True)
    assert fake_llm[0]["torch_dtype"] == torch.float16
    assert fake_llm[0]["quantization_config"]["load_in_8bit"] is True


# =====================================
# Test Mask Label Generator
# =====================================


@pytest.fixture(scope="module")
def mask_label_generator():
    return MaskLabelGenerator()


@pytest.fixture(autouse=True)
def suppress_warnings():
    warnings.filterwarnings("ignore", category=ImportWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)


@pytest.mark.slow
def test_mask_label_generator_has_methods(mask_label_generator):
    """Test that MaskLabelGenerator has generate method."""
    assert hasattr(mask_label_generator, "generate")


@pytest.mark.slow
def test_mask_label_generator_generate_default(mask_label_generator):
    """Test mask generation with default parameters."""
    entity = TEST_ENTITIES["name"]
    generated_text = mask_label_generator.generate(entity, text=TEST_ORIGINAL_TEXT)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


# =====================================
# Test Mask Label Generator With Fake Models
# =====================================


def test_mask_label_generator_fake_masks_one_word_per_input(fake_fill_mask):
    """Test that each word of the entity is masked in its own input."""
    fake_fill_mask.suggestions = [["Jane"], ["Smith"]]
    MaskLabelGenerator().generate(TEST_ENTITIES["name"], text=TEST_ORIGINAL_TEXT)
    first, second = fake_fill_mask.inputs
    assert f"{MASK_TOKEN} Doe" in first
    assert f"John {MASK_TOKEN}" in second


def test_mask_label_generator_fake_trims_inputs_to_context_window(fake_fill_mask):
    """Test that the inputs hold only the text around the entity."""
    fake_fill_mask.suggestions = [["Jane"], ["Smith"]]
    MaskLabelGenerator(context_window=10).generate(TEST_ENTITIES["name"], text=TEST_ORIGINAL_TEXT)
    for masked_input in fake_fill_mask.inputs:
        assert MASK_TOKEN in masked_input
        assert "Medical Record" not in masked_input


def test_mask_label_generator_fake_skips_original_words_and_stopwords(fake_fill_mask):
    """Test that the substitute uses neither the masked word nor punctuation."""
    fake_fill_mask.suggestions = [["John", ".", "Jane"], ["Doe", ",", "Smith"]]
    substitute = MaskLabelGenerator().generate(TEST_ENTITIES["name"], text=TEST_ORIGINAL_TEXT)
    assert sorted(substitute.split()) == ["Jane", "Smith"]


def test_mask_label_generator_fake_without_viable_suggestions_returns_none_text(fake_fill_mask):
    """Test that the generator returns the text "None" when every suggestion is rejected."""
    fake_fill_mask.suggestions = [["John"], ["Doe"]]
    assert MaskLabelGenerator().generate(TEST_ENTITIES["name"], text=TEST_ORIGINAL_TEXT) == "None"


def test_mask_label_generator_fake_single_word_uses_top_suggestion(fake_fill_mask):
    """Test that a one-word entity is replaced by the top suggestion."""
    entity = Entity(text="John", label="name", start_index=30, end_index=34, type="string")
    fake_fill_mask.suggestions = [["Jane", "Mary"]]
    assert MaskLabelGenerator().generate(entity, text=TEST_ORIGINAL_TEXT) == "Jane"


@pytest.mark.skipif(HAS_GPU, reason="GPU available")
def test_mask_label_generator_fake_gpu_without_cuda_warns(fake_fill_mask):
    """Test that requesting a missing GPU warns instead of failing."""
    with pytest.warns(UserWarning, match="GPU/CUDA"):
        MaskLabelGenerator(use_gpu=True)


# =====================================
# Test Date Generator
# =====================================


@pytest.fixture(scope="module")
def date_generator():
    return DateGenerator(lang="en")


def test_date_generator_has_methods(date_generator):
    """Test that DateGenerator has generate method."""
    assert hasattr(date_generator, "generate")


def test_date_generator_generate_default(date_generator):
    """Test date generation with default parameters."""
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_date_generator_generate_custom_date_format():
    """Test date generation with custom format."""
    entity = TEST_ENTITIES["date"][0]
    generator = DateGenerator(date_format="dd-MM-yyyy")
    generated_text = generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_date_generator_generate_non_matching_date_format():
    """Test date generation with non-matching format."""
    entity = TEST_ENTITIES["date"][0]
    generator = DateGenerator(date_format="yyyy-MM-dd")
    custom_date = generator.generate(entity, sub_variant="FIRST_DAY_OF_THE_MONTH")
    assert custom_date == "2024-05-01"


def test_date_generator_generate_first_day_of_the_month(date_generator):
    """Test date generation for first day of the month."""
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="FIRST_DAY_OF_THE_MONTH")
    assert generated_text == "01-05-2024"


def test_date_generator_generate_last_day_of_the_month(date_generator):
    """Test date generation for last day of the month."""
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="LAST_DAY_OF_THE_MONTH")
    assert generated_text == "31-05-2024"


def test_date_generator_generate_middle_of_the_month(date_generator):
    """Test date generation for middle of the month."""
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_MONTH")
    assert generated_text == "15-05-2024"


def test_date_generator_generate_middle_of_the_year(date_generator):
    """Test date generation for middle of the year."""
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="MIDDLE_OF_THE_YEAR")
    assert generated_text == "01-07-2024"


def test_date_generator_generate_random(date_generator):
    """Test date generation with random variant."""
    entity = TEST_ENTITIES["date"][0]
    generated_text = date_generator.generate(entity, sub_variant="RANDOM")
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_date_generator_generate_uncorrect_type(date_generator):
    """Test that non-date entity raises ValueError."""
    entity = TEST_ENTITIES["name"]
    with pytest.raises(ValueError):
        date_generator.generate(entity)


def test_date_generator_process_different_formats(date_generator):
    """Test date generation across all supported formats."""
    for entity in TEST_ENTITIES["date"]:
        try:
            date_generator.generate(entity, sub_variant="RANDOM")
        except ValueError:
            pytest.fail(f"date_generator.generate() raised ValueError unexpectedly for date: {entity.text}")


# =====================================
# Test Number Generator
# =====================================


@pytest.fixture(scope="module")
def number_generator():
    return NumberGenerator()


def test_number_generator_has_methods(number_generator):
    """Test that NumberGenerator has generate method."""
    assert hasattr(number_generator, "generate")


def test_number_generator_generate_integer(number_generator):
    """Test number generation for integer type."""
    entity = TEST_ENTITIES["integer"]
    generated_text = number_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_number_generator_generate_float(number_generator):
    """Test number generation for float type."""
    entity = TEST_ENTITIES["float"]
    generated_text = number_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_number_generator_generate_custom(number_generator):
    """Test number generation for custom regex type."""
    entity = TEST_ENTITIES["custom"]
    generated_text = number_generator.generate(entity)
    match = re.match(entity.regex, generated_text)
    assert match is not None
    assert match.group(0) == generated_text


def test_number_generator_generate_uncorrect_type(number_generator):
    """Test that non-numeric entity raises ValueError."""
    entity = TEST_ENTITIES["name"]
    with pytest.raises(ValueError):
        number_generator.generate(entity)
