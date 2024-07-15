"""The module containing the `language_detector` utilities.

The `language_detector` module contains the `LanguageDetector` class, which is
used to detect the language of a text.

Classes:
    LanguageDetector: The class representing the language detector.

"""

from typing import Tuple

from lingua import LanguageDetectorBuilder

# =====================================
# Main class
# =====================================


class LanguageDetector:
    """The class representing the language detector.

    Examples:
        >>> from anonipy.utils.language_detector import LanguageDetector
        >>> detector = LanguageDetector()
        >>> detector.detect(text)

    Attributes:
        detector (lingua.LanguageDetector): The language detector.

    Methods:
        __call__(text, output_standard):
            Detect the language of a text. Calls the `detect` method.

        detect(text, output_standard):
            Detect the language of a text.

    """

    def __init__(self, low_accuracy: bool = False):
        """Initializes the language detector.

        Examples:
            >>> from anonipy.utils.language_detector import LanguageDetector
            >>> detector = LanguageDetector()

        Args:
            low_accuracy: Whether to use the low accuracy mode.

        """

        # Prepare the language detector for all languages
        builder = LanguageDetectorBuilder.from_all_languages()
        builder = (
            builder.with_low_accuracy_mode()
            if low_accuracy
            else builder.with_preloaded_language_models()
        )
        self.detector = builder.build()

    def __call__(
        self, text: str, output_standard: str = "iso_code_639_1"
    ) -> Tuple[str, str]:
        """Detects the language of a text by calling the `detect` method.

        Examples:
            >>> from anonipy.utils.language_detector import LanguageDetector
            >>> detector = LanguageDetector()
            >>> detector(text)

        Args:
            text: The text to detect the language of.
            output_standard: The output standard.

        Returns:
            The language code.
            The full name of the language.

        """

        return self.detect(text, output_standard)

    def detect(
        self, text: str, output_standard: str = "iso_code_639_1"
    ) -> Tuple[str, str]:
        """Detects the language of a text.

        Examples:
            >>> from anonipy.utils.language_detector import LanguageDetector
            >>> detector = LanguageDetector()
            >>> detector.detect(text)

        Args:
            text: The text to detect the language of.
            output_standard: The output standard.

        Returns:
            The language code.
            The full name of the language.

        """

        language = self.detector.detect_language_of(text)
        iso_code = getattr(language, output_standard).name.lower()
        full_name = language.name.lower().title()
        return iso_code, full_name
