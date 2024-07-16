import re
from typing import Tuple

import torch
from tokenizers import pre_tokenizers
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from guidance import models, gen, select

from .interface import GeneratorInterface
from ...definitions import Entity


# =====================================
# Helper functions
# =====================================


def prepare_llama3_byte_decoder() -> dict:
    """Prepares the byte decoder.

    This is an implementation of a workaround, such that the guidance module
    can be used with the LLaMa-3 model from Hugging Face. Once the issue is resolved,
    we will remove this function.

    Link to the guidance issue: https://github.com/guidance-ai/guidance/issues/782

    Returns:
        The byte decoder.

    """
    byte_decoder = {}
    # alphabet = pre_tokenizers.ByteLevel(False, False).alphabet()
    known_vals = set([])

    for j in range(256):
        for k in range(256):
            for l in range(256):
                if len(byte_decoder.keys()) < 256:
                    b = b""
                    vals = [j, k, l]
                    if not set(vals).issubset(known_vals):
                        for d in range(3):
                            b = b + vals[d].to_bytes(1, "little", signed=False)
                        try:
                            c = b.decode()
                            t = pre_tokenizers.ByteLevel(False, False).pre_tokenize_str(
                                c
                            )[0][0]
                            for m in range(3):
                                if t[m] not in byte_decoder.keys():
                                    byte_decoder[t[m]] = vals[m]
                                    known_vals.add(vals[m])
                        except UnicodeDecodeError:
                            pass

    byte_decoder["À"] = 192
    byte_decoder["Á"] = 193
    byte_decoder["ð"] = 240
    byte_decoder["ñ"] = 241
    byte_decoder["ò"] = 242
    byte_decoder["ó"] = 243
    byte_decoder["ô"] = 244
    byte_decoder["õ"] = 245
    byte_decoder["ö"] = 246
    byte_decoder["÷"] = 247
    byte_decoder["ø"] = 248
    byte_decoder["ù"] = 249
    byte_decoder["ú"] = 250
    byte_decoder["û"] = 251
    byte_decoder["ü"] = 252
    byte_decoder["ý"] = 253
    byte_decoder["þ"] = 254
    byte_decoder["ÿ"] = 255

    return byte_decoder


# =====================================
# Main class
# =====================================


class LLMLabelGenerator(GeneratorInterface):
    """The class representing the LLM label generator.

    !!! info "GPU Requirements"
        The `LLMLabelGenerator` utilizes the open source LLMs, specifically the [Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) model. Because the model is quite large, we utilize quantization using the `bitsandbytes` package to reduce its size. Therefore, the `LLMLabelGenerator` requires at least 8GB GPU and CUDA drivers to be available. If these resources are not available on your machine, you can use the `MaskLabelGenerator` instead.

    Examples:
        >>> from anonipy.anonymize.generators import LLMLabelGenerator
        >>> generator = LLMLabelGenerator()
        >>> generator.generate(entity)

    Attributes:
        model (models.Transformers): The model used to generate the label substitutes.

    Methods:
        generate(entity, entity_prefix, temperature):
            Generate the label based on the entity.

        validate(entity):
            [EXPERIMENTAL] Validate if the entity text corresponds to the entity label.

    """

    def __init__(self, *args, **kwargs):
        """Initializes the LLM label generator.

        Examples:
            >>> from anonipy.anonymize.generators import LLMLabelGenerator
            >>> generator = LLMLabelGenerator()
            LLMLabelGenerator()

        """

        super().__init__(*args, **kwargs)
        # TODO: make this configurable
        model_name = "meta-llama/Meta-Llama-3-8B-Instruct"

        if not torch.cuda.is_available():
            raise RuntimeError(
                "The LabelGenerator requires GPU/CUDA, but it is not available."
            )

        model, tokenizer = self._prepare_model_and_tokenizer(model_name)
        self.model = models.Transformers(model=model, tokenizer=tokenizer, echo=False)

    def generate(
        self,
        entity: Entity,
        add_entity_attrs: str = "",
        temperature: float = 0.0,
        use_regex: bool = True,
        *args,
        **kwargs,
    ) -> str:
        """Generate the substitute for the entity based on it's attributes.

        Examples:
            >>> from anonipy.anonymize.generators import LLMLabelGenerator
            >>> generator = LLMLabelGenerator()
            >>> generator.generate(entity)
            label

        Args:
            entity: The entity to generate the label from.
            add_entity_attrs: Additional entity attribute description to add to the generation.
            temperature: The temperature to use for the generation.
            use_regex: Whether to use regex to determine the generated substitute.

        Returns:
            The generated entity label substitute.

        """

        user_prompt = f"What is a random {add_entity_attrs} {entity.label} replacement for {entity.text}? Respond only with the replacement."
        # prepare the regex for the entity if needed
        regex = None if not use_regex else entity.get_regex_group() or entity.regex
        assistant_prompt = gen(
            name="replacement",
            stop="<|eot_id|>",
            regex=regex,
            temperature=temperature,
        )
        # generate the replacement for the entity
        lm = (
            self.model
            + self._system_prompt()
            + self._user_prompt(user_prompt)
            + self._assistant_prompt(assistant_prompt)
        )
        return lm["replacement"]

    def validate(self, entity: Entity) -> bool:
        """[EXPERIMENTAL] Validate the appropriateness of the entity.

        Examples:
            >>> from anonipy.anonymize.generators import LLMLabelGenerator
            >>> generator = LLMLabelGenerator()
            >>> generator.validate(entity)
            True

        Args:
            entity: The entity to be validated.

        Returns:
            The validation result.

        """

        user_prompt = f"Is {entity.text} a {entity.label}?"
        assistant_prompt = select(["True", "False"], name="validation")
        # validate the entity with the validation prompt
        lm = (
            self.model
            + self._system_prompt()
            + self._user_prompt(user_prompt)
            + self._assistant_prompt(assistant_prompt)
        )
        return bool(lm["validation"])

    # =================================
    # Private methods
    # =================================

    def _prepare_model_and_tokenizer(
        self, model_name: str
    ) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        """Prepares the model and tokenizer.

        Args:
            model_name: The name of the model to use.

        Returns:
            The huggingface model.
            The huggingface tokenizer.

        """

        # prepare the model
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name, quantization_config=bnb_config, low_cpu_mem_usage=True
        )
        # prepare the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, padding_side="right", use_fast=False
        )
        # use the workaround for the LLaMa-3 model
        tokenizer.byte_decoder = prepare_llama3_byte_decoder()
        return model, tokenizer

    def _system_prompt(self) -> str:
        """Returns the system prompt."""
        return "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\nYou are a helpful AI assistant for generating replacements for text entities.<|eot_id|>"

    def _user_prompt(self, prompt: str) -> str:
        """Returns the user prompt.

        Args:
            prompt: The prompt to use.

        Returns:
            The user part of the prompt.

        """

        return f"<|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|>"

    def _assistant_prompt(self, prompt: str) -> str:
        """Returns the assistant prompt.

        Args:
            prompt: The prompt to use.

        Returns:
            The assistant part of the prompt.

        """

        return f"<|start_header_id|>assistant<|end_header_id|>\n\n{prompt}"
