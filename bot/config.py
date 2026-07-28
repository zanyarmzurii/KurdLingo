"""
KurdLingo Bot Configuration
Central configuration module for all bot settings
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
BOT_NAME: str = os.getenv("BOT_NAME", "KurdLingo")
BOT_USERNAME: str = os.getenv("BOT_USERNAME", "KurdLingoBot")

ADMIN_ID: int = int(os.getenv("ADMIN_ID", "7296733212"))
DEVELOPER_ID: int = int(os.getenv("DEVELOPER_ID", "7296733212"))
ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "z_14x")

DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/data/kurdingo.db")
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "badini")
BOT_LANGUAGE: str = os.getenv("BOT_LANGUAGE", "badini")

PAYMENT_METHODS: Dict[str, str] = {
    "FIB": os.getenv("FIB", "+9647506045491"),
    "FASTPAY": os.getenv("FASTPAY", "+9647506045491"),
    "TON": os.getenv("TON_WALLET", "UQAd90pxOXqVTZ04Nv6c2F1FCfd3dVJGxCrnuCm_6Mavz5Ua"),
    "USDT_TRC20": os.getenv("USDT_TRC20", "TKUfVwnjyT2KUa9xnBreT32YLLJEwACHpc"),
    "ADMIN_PHONE": os.getenv("ADMIN_PHONE", "+9647506045491")
}

LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": {"name": "English", "name_badini": "ئینگلیزی", "flag": "🇬🇧", "emoji": "🇬🇧"},
    "ar": {"name": "Arabic", "name_badini": "عەرەبی", "flag": "🇮🇶", "emoji": "🇮🇶"},
    "tr": {"name": "Turkish", "name_badini": "تورکی", "flag": "🇹🇷", "emoji": "🇹🇷"},
    "fa": {"name": "Persian", "name_badini": "فارسی", "flag": "🇮🇷", "emoji": "🇮🇷"},
    "de": {"name": "German", "name_badini": "ئەڵمانی", "flag": "🇩🇪", "emoji": "🇩🇪"},
    "fr": {"name": "French", "name_badini": "فەرەنسی", "flag": "🇫🇷", "emoji": "🇫🇷"},
    "es": {"name": "Spanish", "name_badini": "ئیسپانی", "flag": "🇪🇸", "emoji": "🇪🇸"},
    "zh": {"name": "Chinese", "name_badini": "چینی", "flag": "🇨🇳", "emoji": "🇨🇳"},
    "ru": {"name": "Russian", "name_badini": "ڕووسی", "flag": "🇷🇺", "emoji": "🇷🇺"},
    "ja": {"name": "Japanese", "name_badini": "ژاپۆنی", "flag": "🇯🇵", "emoji": "🇯🇵"}
}

LEVELS: Dict[str, str] = {
    "beginner": "دەستپێکی",
    "elementary": "سەرەتایی",
    "intermediate": "ناوەندی",
    "upper_intermediate": "ناوەندی پێشکەوتوو",
    "advanced": "پێشکەوتوو",
    "master": "شارەزا",
    "complete": "تەواوکاری"
}

LEVEL_ORDER: list = [
    "beginner",
    "elementary", 
    "intermediate",
    "upper_intermediate",
    "advanced",
    "master",
    "complete"
]

LEVEL_EMOJI: Dict[str, str] = {
    "beginner": "🌱",
    "elementary": "🌿",
    "intermediate": "🌳",
    "upper_intermediate": "🌲",
    "advanced": "⭐",
    "master": "🌟",
    "complete": "👑"
}

PLANS: Dict[str, Any] = {
    "free": {
        "name": "بەلاش",
        "name_en": "Free",
        "emoji": "🌟",
        "price": 0,
        "daily_lessons": int(os.getenv("DAILY_LESSONS_FREE", "3")),
        "daily_coins": int(os.getenv("DAILY_COINS_FREE", "100")),
        "ads": True,
        "trial_days": 0,
        "features": [
            "٣ وانە لە ڕۆژێکدا",
            "١٠٠ کۆینی ڕۆژانە",
            "بەشداری لە کلان",
            "خشتەی پلەبەندی"
        ]
    },
    "plus": {
        "name": "پڵەس",
        "name_en": "Plus",
        "emoji": "⭐",
        "prices": {
            "1_month": 14990,
            "3_months": 39990,
            "6_months": 69990,
            "1_year": 119990
        },
        "daily_lessons": int(os.getenv("DAILY_LESSONS_PLUS", "10")),
        "daily_coins": int(os.getenv("DAILY_COINS_PLUS", "300")),
        "ads": "کەمتر",
        "trial_days": int(os.getenv("TRIAL_DAYS", "7")),
        "features": [
            "١٠ وانە لە ڕۆژێکدا",
            "٣٠٠ کۆینی ڕۆژانە",
            "وانەی تایبەتی هەفتانە",
            "پشتگیری بە کوردی و ئینگلیزی",
            "ئەنجامی تایبەت",
            "بەدجی تایبەت"
        ]
    },
    "premium": {
        "name": "پرێمیەم",
        "name_en": "Premium",
        "emoji": "👑",
        "prices": {
            "1_month": 24990,
            "3_months": 64990,
            "6_months": 119990,
            "1_year": 199990
        },
        "daily_lessons": "unlimited",
        "daily_coins": int(os.getenv("DAILY_COINS_PREMIUM", "1000")),
        "ads": False,
        "trial_days": int(os.getenv("TRIAL_DAYS", "7")),
        "features": [
            "وانەی بێسنوور",
            "١٠٠٠ کۆینی ڕۆژانە",
            "بێ ڕیکلام",
            "پشتگیری VIP 24/7",
            "وانەی ڕاستەوخۆ (٢ جار/مانگ)",
            "ئەنالیتیکسی تایبەت",
            "ڕەنگی تایبەتی پرۆفایل",
            "بەدجی ئەڵماسی"
        ]
    },
    "family": {
        "name": "خێزانی",
        "name_en": "Family",
        "emoji": "🏠",
        "prices": {
            "1_month": 49990,
            "3_months": 129990,
            "6_months": 239990,
            "1_year": 399990
        },
        "daily_lessons": "unlimited",
        "daily_coins": int(os.getenv("DAILY_COINS_FAMILY", "2000")),
        "ads": False,
        "trial_days": int(os.getenv("TRIAL_DAYS", "7")),
        "members": 5,
        "features": [
            "بۆ ٥ ئەندام",
            "٢٠٠٠ کۆینی ڕۆژانە بۆ هەر کەس",
            "کلانی تایبەتی خێزانی",
            "پێشبڕکێی تایبەتی خێزانی",
            "ئەدمینی خێزان",
            "ڕاپۆرتی پێشکەوتنی خێزان",
            "چاتی تایبەتی خێزانی",
            "وانەی ڕاستەوخۆ (٤ جار/مانگ)"
        ]
    }
}

DURATION_MAP: Dict[str, str] = {
    "1": "1_month",
    "3": "3_months",
    "6": "6_months",
    "12": "1_year"
}

DURATION_NAMES: Dict[str, str] = {
    "1_month": "١ مانگ",
    "3_months": "٣ مانگ",
    "6_months": "٦ مانگ",
    "1_year": "١ ساڵ"
}

QUIZ_SETTINGS: Dict[str, Any] = {
    "questions_per_quiz": 20,
    "pass_percentage": int(os.getenv("QUIZ_PASS_PERCENTAGE", "70")),
    "xp_per_correct": 10,
    "coins_per_quiz": 50,
    "bonus_xp_perfect": 100,
    "bonus_coins_perfect": 200,
    "time_limit_minutes": 15
}

REFERRAL_SETTINGS: Dict[str, Any] = {
    "max_daily": int(os.getenv("MAX_REFERRALS_PER_DAY", "25")),
    "premium_reward_days": int(os.getenv("REFERRAL_PREMIUM_DAYS", "30")),
    "referred_premium_days": int(os.getenv("REFERRED_PREMIUM_DAYS", "7")),
    "coins_per_referral": 500,
    "bonus_referrals_5": 5000,
    "bonus_referrals_10": 10000,
    "bonus_referrals_25": 25000
}

XPTABLE: Dict[str, int] = {
    "lesson_complete": 50,
    "quiz_pass": 100,
    "perfect_quiz": 200,
    "daily_streak_3": 150,
    "daily_streak_7": 350,
    "daily_streak_30": 1500,
    "referral": 500,
    "level_up": 1000,
    "certificate_earned": 2000
}

COIN_TABLE: Dict[str, int] = {
    "lesson_complete": 25,
    "quiz_pass": 50,
    "perfect_quiz": 100,
    "daily_login": 10,
    "daily_streak_bonus": 25,
    "referral": 250,
    "level_up": 500
}

SUPPORTED_LANGUAGES_LEARNING: list = list(LANGUAGES.keys())

MAX_LESSON_LENGTH: int = 50
MAX_QUIZ_OPTIONS: int = 4
MIN_QUIZ_OPTIONS: int = 2

CACHE_TTL: int = 3600
SESSION_TIMEOUT: int = 1800
MAX_RETRY_ATTEMPTS: int = 3
RETRY_DELAY: int = 5

DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_SHORT: str = "%Y-%m-%d"
TIME_FORMAT: str = "%H:%M:%S"

PAGINATION_SIZE: int = 10
MAX_BUTTONS_PER_ROW: int = 2
MAX_INLINE_ROWS: int = 10

DATA_DIR: Path = BASE_DIR / "data"
LOG_DIR: Path = BASE_DIR / "logs"
TEMP_DIR: Path = BASE_DIR / "temp"

for directory in [DATA_DIR, LOG_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
logger.info(f"Bot Configuration loaded: {BOT_NAME}")
