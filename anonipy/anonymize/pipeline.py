"""Module containing the `pipeline`.

The `pipeline` module provides a class for anonymizing files using a pipeline of
extractors and strategies.

Classes:
    Pipeline: The class representing the anonymization pipeline.

"""

import os
import warnings
from typing import Union, List

from .extractors import ExtractorInterface, MultiExtractor
from .strategies import StrategyInterface
from ..utils.file_system import open_file, write_file


# =====================================
# Pipeline class
# =====================================


class Pipeline:
    """A class for anonymizing files using a pipeline of extractors and strategies.

    Examples:
        >>> from anonipy.anonymize.pipeline import Pipeline
        >>> extractor = NERExtractor(labels, lang=LANGUAGES.ENGLISH)
        >>> strategy = RedactionStrategy()
        >>> pipeline = Pipeline(extractor, strategy)
        >>> pipeline.anonymize("/path/to/input_dir", "/path/to/output_dir", flatten=True)

    Attributes:
        extractor (ExtractorInterface, MultiExtractor, List[ExtractorInterface]): The extractor to use for entity extraction.
        strategy (StrategyInterface): The strategy to use for anonymization.

    Methods:
        anonymize(input_dir, output_dir, flatten=False):
            Anonymize files in the input directory and save the anonymized files to the output directory.

    """

    def __init__(
        self,
        extractor: Union[ExtractorInterface, MultiExtractor, List[ExtractorInterface]],
        strategy: StrategyInterface,
    ):
        """Initialize the pipeline.

        Examples:
            >>> from anonipy.anonymize.pipeline import Pipeline
            >>> extractor = NERExtractor(labels, lang=LANGUAGES.ENGLISH)
            >>> strategy = RedactionStrategy()
            >>> pipeline = Pipeline(extractor, strategy)

        Args:
            extractor: The extractor to use for entity extraction.
            strategy: The strategy to use for anonymization.

        """

        if isinstance(extractor, ExtractorInterface) or isinstance(
            extractor, MultiExtractor
        ):
            self.extractor = extractor
        elif isinstance(extractor, list):
            self.extractor = MultiExtractor(extractor)
        else:
            raise ValueError(
                "Extractor must be an ExtractorInterface or a list of ExtractorInterface."
            )

        if not isinstance(strategy, StrategyInterface):
            raise ValueError("Strategy must be a StrategyInterface.")

        self.strategy = strategy

    def anonymize(self, input_dir: str, output_dir: str, flatten: bool = False) -> dict:
        """Anonymize files in the input directory and save the anonymized files to the output directory.

        Args:
            input_dir: The path to the input directory containing files to be anonymized.
            output_dir: The path to the output directory where anonymized files will be saved.
            flatten: Whether to flatten the output directory structure. Defaults to False.

        Raises:
            ValueError: If the input directory does not exist or if the input and output directories are the same.

        Returns:
            A dictionary mapping the original file paths to the anonymized file paths.

        """

        if not os.path.exists(input_dir):
            raise ValueError(f"Input directory '{input_dir}' does not exist.")

        if os.path.abspath(input_dir) == os.path.abspath(output_dir):
            raise ValueError("Input and output directories cannot be the same.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        anonymized_files_count = 1
        file_name_mapping = {}

        for root, _, files in os.walk(input_dir):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                try:
                    anonymized_text = self._anonymize_file(file_path)
                    if anonymized_text is None:
                        continue
                except Exception as e:
                    warnings.warn(f"Problems while processing file {file_path}: {e}")
                    continue

                _, ext = os.path.splitext(file_name)
                output_file_name = f"file{anonymized_files_count}_anony{ext}"
                anonymized_files_count += 1

                relative_path = os.path.relpath(file_path, input_dir)

                if flatten:
                    output_file_path = os.path.join(output_dir, output_file_name)
                else:
                    output_file_path = os.path.join(
                        output_dir, os.path.dirname(relative_path), output_file_name
                    )
                    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                write_file(anonymized_text, output_file_path)

                file_path_before = os.path.join(
                    input_dir.split(os.sep)[-1], relative_path
                )
                file_path_after = os.path.relpath(output_file_path, output_dir)
                file_name_mapping[file_path_before] = os.path.join(
                    output_dir.split(os.sep)[-1], file_path_after
                )

        return file_name_mapping

    def _anonymize_file(self, file_path: str) -> Union[str, None]:
        """Anonymize a single file.

        Args:
            file_path: The path to the file to be anonymized.

        Returns:
            The anonymized text or None if the file is empty or if entity extraction fails.

        """

        original_text = open_file(file_path)
        if original_text is None or not original_text.strip():
            warnings.warn(
                f"Skipping file {file_path}: Failed to read or file is empty."
            )
            return None

        _, entities = self.extractor(original_text)

        if not entities:
            warnings.warn(
                f"Skipping file {file_path}: Entity extraction returned None."
            )
            return None

        anonymized_text, _ = self.strategy.anonymize(original_text, entities)

        return anonymized_text
