from telebot import types
from bot.config import LANGUAGES

def language_select_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for code, info in LANGUAGES.items():
        buttons.append(types.InlineKeyboardButton(
            f"{info['emoji']} {info['name_badini']}",
            callback_data=f"lang_{code}"
        ))
    markup.add(*buttons)
    return markup
