"""
KurdLingo Bot Handlers Package
Each module contains a register_*_handlers(bot) function
"""
from .start import register_start_handlers
from .language_test import register_language_test_handlers
from .lessons import register_lessons_handlers
from .quiz import register_quiz_handlers
from .payment_handlers import register_payment_handlers
from .admin_panel import register_admin_handlers
from .referral import register_referral_handlers
from .certificates import register_certificates_handlers

__all__ = [
    "register_start_handlers",
    "register_language_test_handlers",
    "register_lessons_handlers",
    "register_quiz_handlers",
    "register_payment_handlers",
    "register_admin_handlers",
    "register_referral_handlers",
    "register_certificates_handlers",
]
