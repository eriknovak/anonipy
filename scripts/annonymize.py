import os
import unicodedata
from argparse import ArgumentParser

import torch
import pandas as pd
from tqdm import tqdm

from gliner import GLiNER
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

from src.utils.fs import open_file, get_file_text
from src.utils.annonymize_helpers import gliner_annonymize

# ===============================================
# Load the classification model
# ===============================================


# ===============================================
# Define helper functions
# ===============================================


# ===============================================
# Define the main function
# ===============================================


def main(args):
    # prepare the file text
    f = open_file(args.input_file)
    f_txt = get_file_text(f)

    # load the model and extract the entities
    # TODO: current support only for GLiNER models
    model = GLiNER.from_pretrained(args.model)
    labels = [tag.strip() for tag in args.tags.split(",")]
    entities = model.predict_entities(f_txt, labels, threshold=args.ner_th)

    print(entities)
    # annonymize the text
    a_txt = gliner_annonymize(f_txt, entities, labels)

    # save the annonymized text
    with open(args.output_file, "w", encoding="utf-8") as f:
        f.write(a_txt)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_file", type=str, default=None, help="The input file")
    parser.add_argument(
        "--output_file",
        type=str,
        default=None,
        help="The output file containing the annonymized text",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="urchade/gliner_multi",
        help="The model used to identify the tags",
    )
    parser.add_argument(
        "--tags",
        type=str,
        default="name,date,policy number,social security number",
        help="Comma separated tags to find and replace with asterisks",
    )
    parser.add_argument(
        "--ner_th",
        default=0.3,
        type=float,
        help="The threshold for the NER model",
    )

    args = parser.parse_args()
    main(args)
