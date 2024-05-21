"""
The language detector class
"""

from lingua import LanguageDetectorBuilder


class LanguageDetector:

    def __init__(self, low_accuracy: bool = False):
        # Prepare the language detector for all languages
        builder = LanguageDetectorBuilder.from_all_languages()
        builder = (
            builder.with_low_accuracy_mode()
            if low_accuracy
            else builder.with_preloaded_language_models()
        )
        self.detector = builder.build()

    def __call__(self, text: str, output_standard: str = "iso_code_639_1") -> str:
        return self.detect(text, output_standard)

    def detect(self, text: str, output_standard: str = "iso_code_639_1") -> str:
        language = self.detector.detect_language_of(text)
        iso_code = getattr(language, output_standard).name.lower()
        full_name = language.name.lower().title()
        return iso_code, full_name
