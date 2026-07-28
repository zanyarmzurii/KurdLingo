"""
KurdLingo Bot - Fêrbûna Ziman bi Kurdî Bedhînî
Enterprise-grade Telegram Bot for Language Learning
"""

__version__ = "1.0.0"
__author__ = "KurdLingo Team"
__license__ = "MIT"

from bot.config import (
    BOT_TOKEN,
    BOT_NAME,
    ADMIN_ID,
    DEVELOPER_ID,
    PAYMENT_METHODS,
    LANGUAGES,
    LEVELS,
    PLANS,
    QUIZ_SETTINGS,
    REFERRAL_SETTINGS
)

from bot.database import Database, db

__all__ = [
    "BOT_TOKEN",
    "BOT_NAME", 
    "ADMIN_ID",
    "DEVELOPER_ID",
    "PAYMENT_METHODS",
    "LANGUAGES",
    "LEVELS",
    "PLANS",
    "QUIZ_SETTINGS",
    "REFERRAL_SETTINGS",
    "Database",
    "db"
]
