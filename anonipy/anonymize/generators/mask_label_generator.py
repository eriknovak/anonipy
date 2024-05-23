import re
import random
import warnings
import itertools

import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer, pipeline

from .interface import GeneratorInterface
from ...definitions import Entity


STOPWORDS = [".", ",", ":", ";", "-", "<s>", "</s>"]

# =====================================
# Main class
# =====================================


class MaskLabelGenerator(GeneratorInterface):

    def __init__(
        self,
        model_name="FacebookAI/xlm-roberta-large",
        use_gpu: bool = False,
        context_window: int = 100,
        *args,
        **kwargs,
    ):
        self.context_window = context_window
        if use_gpu and not torch.cuda.is_available():
            warnings.warn(
                "The use_gpu=True flag requires GPU/CUDA, but it is not available. Setting use_gpu=False."
            )
            use_gpu = False

        # prepare the fill-mask pipeline and store the mask token
        model, tokenizer = self._prepare_model_and_tokenizer(model_name, use_gpu)
        self.mask_token = tokenizer.mask_token
        self.pipeline = pipeline(
            "fill-mask", model=model, tokenizer=tokenizer, top_k=40
        )

    def generate(self, entity: Entity, text: str, *args, **kwargs):
        masks = self._create_masks(entity)
        input_texts = self._prepare_generate_inputs(masks, text)
        suggestions = self.pipeline(input_texts)
        return self._create_substitute(entity, masks, suggestions)

    # =================================
    # Private methods
    # =================================

    def _prepare_model_and_tokenizer(self, model_name: str, use_gpu: bool):
        # prepare the model
        device = torch.device(
            "cuda" if use_gpu and torch.cuda.is_available() else "cpu"
        )
        model = AutoModelForMaskedLM.from_pretrained(model_name).to(device)
        # prepare the tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return model, tokenizer

    def _create_masks(self, entity: Entity):
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

    def _get_context_text(self, text, start_index, end_index):
        min_index = max(0, start_index - self.context_window)
        max_index = min(end_index + self.context_window, len(text))
        return text[min_index:max_index]

    def _prepare_generate_inputs(self, masks, text):
        return [
            self._get_context_text(
                text[: m["start_index"]] + m["mask_text"] + text[m["end_index"] :],
                m["start_index"],
                m["end_index"],
            )
            for m in masks
        ]

    def _create_substitute(self, entity: Entity, masks, suggestions):
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
