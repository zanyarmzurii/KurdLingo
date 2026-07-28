from .languages.english import LANGUAGE_DATA as ENGLISH_DATA
from .languages.arabic import LANGUAGE_DATA as ARABIC_DATA
from .languages.turkish import LANGUAGE_DATA as TURKISH_DATA
from .languages.persian import LANGUAGE_DATA as PERSIAN_DATA
from .languages.german import LANGUAGE_DATA as GERMAN_DATA
from .languages.french import LANGUAGE_DATA as FRENCH_DATA
from .languages.spanish import LANGUAGE_DATA as SPANISH_DATA
from .languages.chinese import LANGUAGE_DATA as CHINESE_DATA
from .languages.russian import LANGUAGE_DATA as RUSSIAN_DATA
from .languages.japanese import LANGUAGE_DATA as JAPANESE_DATA

ALL_LANGUAGE_DATA = {
    "en": ENGLISH_DATA,
    "ar": ARABIC_DATA,
    "tr": TURKISH_DATA,
    "fa": PERSIAN_DATA,
    "de": GERMAN_DATA,
    "fr": FRENCH_DATA,
    "es": SPANISH_DATA,
    "zh": CHINESE_DATA,
    "ru": RUSSIAN_DATA,
    "ja": JAPANESE_DATA,
}

def get_language_data(lang_code: str):
    return ALL_LANGUAGE_DATA.get(lang_code, ENGLISH_DATA)
