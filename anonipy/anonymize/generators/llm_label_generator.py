import re
import warnings
from typing import Tuple, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from .interface import GeneratorInterface
from ...definitions import Entity


# =====================================
# Main class
# =====================================


class LLMLabelGenerator(GeneratorInterface):
    """The class representing the LLM label generator.

    Examples:
        >>> from anonipy.anonymize.generators import LLMLabelGenerator
        >>> generator = LLMLabelGenerator()
        >>> generator.generate(entity)

    Attributes:
        model (models.Transformers): The model used to generate the label substitutes.

    Methods:
        generate(entity, entity_prefix, temperature):
            Generate the label based on the entity.

    """

    def __init__(
        self,
        *args,
        model_name: str = "HuggingFaceTB/SmolLM2-1.7B-Instruct",
        use_gpu: bool = False,
        **kwargs,
    ):
        """Initializes the LLM label generator.

        Args:
            model_name: The name of the model to use.
            use_gpu: Whether to use GPU or not.

        Examples:
            >>> from anonipy.anonymize.generators import LLMLabelGenerator
            >>> generator = LLMLabelGenerator()
            LLMLabelGenerator()

        """

        super().__init__(*args, **kwargs)

        if use_gpu and not torch.cuda.is_available():
            warnings.warn(
                "The use_gpu=True flag requires GPU/CUDA, but it is not available. Setting use_gpu=False."
            )
            use_gpu = False

        self.model, self.tokenizer = self._prepare_model_and_tokenizer(
            model_name, use_gpu
        )

    def generate(
        self,
        entity: Entity,
        *args,
        add_entity_attrs: str = "",
        temperature: float = 1.0,
        top_p: float = 0.95,
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
            top_p: The top p to use for the generation.

        Returns:
            The generated entity label substitute.

        """

        message = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant for generating replacements for text entities.",
            },
            {
                "role": "user",
                "content": f"What is a random {add_entity_attrs} {entity.label} replacement for {entity.text}? Respond only with the replacement.",
            },
        ]
        return self._generate_response(message, temperature, top_p)

    # =================================
    # Private methods
    # =================================

    def _prepare_model_and_tokenizer(
        self, model_name: str, use_gpu: bool
    ) -> Tuple[AutoModelForCausalLM, AutoTokenizer]:
        """Prepares the model and tokenizer.

        Args:
            model_name: The name of the model to use.

        Returns:
            The huggingface model.
            The huggingface tokenizer.

        """

        # prepare the model
        device = torch.device(
            "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        )
        model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
        # prepare the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            model_name, padding_side="right", use_fast=False
        )
        return model, tokenizer

    def _generate_response(
        self, message: List[dict], temperature: float, top_p: float
    ) -> str:
        """Generate the response from the LLM.

        Args:
            message: The message to generate the response from.
            temperature: The temperature to use for the generation.
            top_p: The top p to use for the generation.

        Returns:
            The generated response.

        """

        # tokenize the message
        input_ids = self.tokenizer.apply_chat_template(
            message, tokenize=True, return_tensors="pt"
        ).to(self.model.device)

        # generate the response
        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_new_tokens=50,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
            )

        # decode the response
        response = self.tokenizer.decode(
            output_ids[0][len(input_ids[0]) :], skip_special_tokens=True
        )
        return self._parse_response(response)

    def _parse_response(self, response: str) -> str:
        """Parse the response from the LLM.

        Args:
            response: The response to parse.

        Returns:
            The parsed response.

        """

        match = re.search(r"assistant\s*(.*)", response, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip() if match else response
