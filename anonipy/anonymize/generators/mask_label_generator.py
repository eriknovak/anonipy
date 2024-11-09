import re
import random
import warnings
import itertools

from typing import List, Tuple

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline

from .interface import GeneratorInterface
from ...definitions import Entity


STOPWORDS = [".", ",", ":", ";", "-", "<s>", "</s>"]


# =====================================
# Main class
# =====================================


class MaskLabelGenerator(GeneratorInterface):
    """The class representing the mask label generator.

    Examples:
        >>> from anonipy.anonymize.generators import MaskLabelGenerator
        >>> generator = MaskLabelGenerator(model_name, context_window=100, use_gpu=False)
        >>> generator.generate(entity)


    Attributes:
        pipeline (Pipeline): The transformers pipeline used to generate the label substitutes.
        context_window (int): The context window size to use to generate the label substitutes.
        mask_token (str): The mask token to use to replace the masked words.

    Methods:
        generate(entity, text):
            Generate the substitute for the entity based on it's location in the text.

    """

    def __init__(
        self,
        *args,
        model_name: str = "FacebookAI/xlm-roberta-large",
        use_gpu: bool = False,
        context_window: int = 100,
        **kwargs,
    ):
        """Initializes the mask label generator.

        Examples:
            >>> from anonipy.anonymize.generators import MaskLabelGenerator
            >>> generator = MaskLabelGenerator(context_window=120, use_gpu=True)

        Args:
            model_name: The name of the masking model to use.
            use_gpu: Whether to use GPU/CUDA, if available.
            context_window: The context window size.

        """

        super().__init__(*args, **kwargs)
        self.context_window = context_window
        if use_gpu and not torch.cuda.is_available():
            warnings.warn(
                "The use_gpu=True flag requires GPU/CUDA, but it is not available. Setting use_gpu=False."
            )
            use_gpu = False

        # prepare the fill-mask pipeline and store the mask token
        model, tokenizer, device = self._prepare_model_and_tokenizer(
            model_name, use_gpu
        )
        self.mask_token = tokenizer.mask_token
        self.pipeline = pipeline(
            "fill-mask", model=model, tokenizer=tokenizer, top_k=40, device=device
        )

    def generate(self, entity: Entity, text: str, *args, **kwargs) -> str:
        """Generate the substitute for the entity using the masking model.

        Examples:
            >>> from anonipy.anonymize.generators import MaskLabelGenerator
            >>> generator = MaskLabelGenerator(context_window=120, use_gpu=True)
            >>> generator.generate(entity, text)
            label

        Args:
            entity: The entity used to generate the substitute.
            text: The original text in which the entity is located; used to get the entity's context.

        Returns:
            The generated substitute text.

        """

        masks = self._create_masks(entity)
        input_texts = self._prepare_generate_inputs(masks, text)
        suggestions = self.pipeline(input_texts)
        return self._create_substitute(entity, masks, suggestions)

    # =================================
    # Private methods
    # =================================

    def _prepare_model_and_tokenizer(
        self, model_name: str, use_gpu: bool
    ) -> Tuple[AutoModelForMaskedLM, AutoTokenizer]:
        """Prepares the model and tokenizer.

        Args:
            model_name: The name of the model to use.
            use_gpu: Whether to use GPU/CUDA, if available.

        Returns:
            The huggingface model.
            The huggingface tokenizer.
            The device to use.

        """

        # prepare the model
        device = torch.device(
            "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        )
        model = AutoModelForMaskedLM.from_pretrained(model_name).to(device)
        # prepare the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        return model, tokenizer, device

    def _create_masks(self, entity: Entity) -> List[dict]:
        """Creates the masks for the provided entity.

        Args:
            entity: The entity to create the masks for.

        Returns:
            The list of masks attributes, including the true text, mask text, start index, and end index within the original text.

        """

        masks = []
        chunks = re.split(r"\s+", entity.text)
        for idx in range(len(chunks)):
            masks.append(
                {
                    "true_text": chunks[idx],
                    "mask_text": " ".join(
                        chunks[0:idx] + [self.mask_token] + chunks[idx + 1 :]
                    ),
                    "start_index": entity.start_index,
                    "end_index": entity.end_index,
                }
            )
        return masks

    def _get_context_text(self, text: str, start_index: int, end_index: int) -> str:
        """Get the context text.

        Args:
            text: The text to get the context from.
            start_index: The start index of the context window.
            end_index: The end index of the context window.

        Returns:
            The context window text.

        """

        min_index = max(0, start_index - self.context_window)
        max_index = min(end_index + self.context_window, len(text))
        return text[min_index:max_index]

    def _prepare_generate_inputs(self, masks: List[dict], text: str) -> List[str]:
        """Prepares the generate inputs.

        Args:
            masks: The list of masks attributes.
            text: The text to prepare the generate inputs for.

        Returns:
            The list of generate inputs.

        """
        return [
            self._get_context_text(
                text[: m["start_index"]] + m["mask_text"] + text[m["end_index"] :],
                m["start_index"],
                m["end_index"],
            )
            for m in masks
        ]

    def _create_substitute(
        self, entity: Entity, masks: List[dict], suggestions: List[dict]
    ) -> str:
        """Create a substitute for the entity.

        Args:
            entity: The entity to create the substitute for.
            masks: The list of masks attributes.
            suggestions: The list of substitute suggestions.

        Returns:
            The created and selected substitute text.

        """

        substitute_chunks = []
        for mask, suggestion in zip(masks, suggestions):
            suggestion = suggestion if type(suggestion) == list else [suggestion]
            viable_suggestions = list(
                filter(
                    lambda x: x["token_str"] != mask["true_text"]
                    and re.match(entity.regex, x["token_str"])
                    and x["token_str"] not in STOPWORDS,
                    suggestion,
                )
            )
            substitute_chunks.append([s["token_str"] for s in viable_suggestions[:3]])
        combinations = list(itertools.product(*substitute_chunks))
        combinations = list(map(lambda x: " ".join(set(x)), combinations))
        return random.choice(combinations) if len(combinations) > 0 else "None"
