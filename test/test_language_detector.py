import unittest

from anonipy.utils.language_detector import LanguageDetector
from anonipy.constants import LANGUAGES

# =====================================
# Test Language Detector
# =====================================


class TestLanguageDetector(unittest.TestCase):

    def test_init(self):
        language_detector = LanguageDetector()
        self.assertEqual(language_detector.__class__, LanguageDetector)

    def test_has_methods(self):
        language_detector = LanguageDetector()
        self.assertEqual(hasattr(language_detector, "detect"), True)

    def test_detect_english(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "This test verifies that the method is working correctly"
        )
        self.assertEqual(language[0], "en")
        self.assertEqual(language[1], "English")
        self.assertEqual(language, LANGUAGES.ENGLISH)

    def test_detect_slovene(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Ta test preverja, ali metoda dela pravilno"
        )
        self.assertEqual(language[0], "sl")
        self.assertEqual(language[1], "Slovene")
        self.assertEqual(language, LANGUAGES.SLOVENE)

    def test_detect_german(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Dieser Test überprüft, ob die Methode ordnungsgemäß funktioniert"
        )
        self.assertEqual(language[0], "de")
        self.assertEqual(language[1], "German")
        self.assertEqual(language, LANGUAGES.GERMAN)

    def test_detect_dutch(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Deze test verifieert dat de methode correct werkt"
        )
        self.assertEqual(language[0], "nl")
        self.assertEqual(language[1], "Dutch")
        self.assertEqual(language, LANGUAGES.DUTCH)

    def test_detect_spanish(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Esta prueba verifica que el método está funcionando correctamente"
        )
        self.assertEqual(language[0], "es")
        self.assertEqual(language[1], "Spanish")
        self.assertEqual(language, LANGUAGES.SPANISH)

    def test_detect_greek(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Αυτή η δοκιμή επαληθεύει ότι η μέθοδος λειτουργεί σωστά"
        )
        self.assertEqual(language[0], "el")
        self.assertEqual(language[1], "Greek")
        self.assertEqual(language, LANGUAGES.GREEK)

    def test_detect_italian(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Questo test verifica che il metodo funzioni correttamente"
        )
        self.assertEqual(language[0], "it")
        self.assertEqual(language[1], "Italian")
        self.assertEqual(language, LANGUAGES.ITALIAN)

    def test_detect_french(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Ce test vérifie que la méthode fonctionne correctement"
        )
        self.assertEqual(language[0], "fr")
        self.assertEqual(language[1], "French")
        self.assertEqual(language, LANGUAGES.FRENCH)

    def test_detect_ukrainian(self):
        language_detector = LanguageDetector()
        language = language_detector.detect(
            "Цей тест перевіряє, чи метод працює правильно"
        )
        self.assertEqual(language[0], "uk")
        self.assertEqual(language[1], "Ukrainian")
        self.assertEqual(language, LANGUAGES.UKRAINIAN)


if __name__ == "__main__":
    unittest.main()
