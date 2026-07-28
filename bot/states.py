"""
KurdLingo Bot States
Defines conversation states for multi-step flows
"""
from telebot.handler_backends import State, StatesGroup

class BotStates(StatesGroup):
    """States for bot conversations"""
    main_menu = State()
    select_language = State()
    select_level = State()
    level_test = State()
    quiz_answer = State()
    payment_method = State()
    payment_receipt = State()
    referral_code = State()
    admin_broadcast = State()
    admin_verify = State()
    settings = State()
    feedback = State()
