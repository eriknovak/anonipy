import warnings

import pytest

from anonipy.utils.language_detector import LanguageDetector
from anonipy.constants import LANGUAGES

# =====================================
# Test Language Detector
# =====================================


@pytest.fixture(scope="module", autouse=True)
def suppress_warnings():
    warnings.filterwarnings("ignore", category=ImportWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)


@pytest.fixture
def language_detector():
    return LanguageDetector()


def test_init(language_detector):
    assert isinstance(language_detector, LanguageDetector)


def test_has_methods(language_detector):
    assert hasattr(language_detector, "detect")


def test_detect_english(language_detector):
    language = language_detector.detect(
        "This test verifies that the method is working correctly"
    )
    assert language[0] == "en"
    assert language[1] == "English"
    assert language == LANGUAGES.ENGLISH


def test_detect_slovenian(language_detector):
    language = language_detector.detect("Ta test preverja, ali metoda dela pravilno")
    assert language[0] == "sl"
    assert language[1] == "Slovenian"
    assert language == LANGUAGES.SLOVENIAN


def test_detect_german(language_detector):
    language = language_detector.detect(
        "Dieser Test überprüft, ob die Methode ordnungsgemäß funktioniert"
    )
    assert language[0] == "de"
    assert language[1] == "German"
    assert language == LANGUAGES.GERMAN


def test_detect_dutch(language_detector):
    language = language_detector.detect(
        "Deze test verifieert dat de methode correct werkt"
    )
    assert language[0] == "nl"
    assert language[1] == "Dutch"
    assert language == LANGUAGES.DUTCH


def test_detect_spanish(language_detector):
    language = language_detector.detect(
        "Esta prueba verifica que el método está funcionando correctamente"
    )
    assert language[0] == "es"
    assert language[1] == "Spanish"
    assert language == LANGUAGES.SPANISH


def test_detect_greek(language_detector):
    language = language_detector.detect(
        "Αυτή η δοκιμή επαληθεύει ότι η μέθοδος λειτουργεί σωστά"
    )
    assert language[0] == "el"
    assert language[1] == "Greek"
    assert language == LANGUAGES.GREEK


def test_detect_italian(language_detector):
    language = language_detector.detect(
        "Questo test verifica che il metodo funzioni correttamente"
    )
    assert language[0] == "it"
    assert language[1] == "Italian"
    assert language == LANGUAGES.ITALIAN


def test_detect_french(language_detector):
    language = language_detector.detect(
        "Ce test vérifie que la méthode fonctionne correctement"
    )
    assert language[0] == "fr"
    assert language[1] == "French"
    assert language == LANGUAGES.FRENCH


def test_detect_ukrainian(language_detector):
    language = language_detector.detect("Цей тест перевіряє, чи метод працює правильно")
    assert language[0] == "uk"
    assert language[1] == "Ukrainian"
    assert language == LANGUAGES.UKRAINIAN
