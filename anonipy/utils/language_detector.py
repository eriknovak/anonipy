from lingua import LanguageDetectorBuilder


class LanguageDetector:
    """The class for detecting the language of a text

    Attributes
    ----------
    detector : LanguageDetector
        The language detector

    Methods
    -------
    __call__(self, text: str, output_standard: str = "iso_code_639_1")
        Detect the language of a text. Calls the `detect` method.

    detect(text: str, output_standard: str = "iso_code_639_1")
        Detect the language of a text

    """

    def __init__(self, low_accuracy: bool = False):
        """
        Parameters
        ----------
        low_accuracy : bool, optional
            Whether to use the low accuracy mode. Default: False

        """

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
        """
        Detect the language of a text

        Parameters
        ----------
        text : str
            The text to detect the language of
        output_standard : str, optional
            The output standard. Default: "iso_code_639_1"

        Returns
        -------
        Tuple[str, str]
            The language code and the full name of the language

        """

        language = self.detector.detect_language_of(text)
        iso_code = getattr(language, output_standard).name.lower()
        full_name = language.name.lower().title()
        return iso_code, full_name
