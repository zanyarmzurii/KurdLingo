from telebot import types
from bot.config import PLANS, DURATION_NAMES, DURATION_MAP

def plans_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🌟 پلانی بەلاش - بێبەرامبەر", callback_data="buy_free"))
    markup.add(types.InlineKeyboardButton("⭐ پلانی پڵەس", callback_data="buy_plus"))
    markup.add(types.InlineKeyboardButton("👑 پلانی پرێمیەم", callback_data="buy_premium"))
    markup.add(types.InlineKeyboardButton("🏠 پلانی خێزانی (٥ کەس)", callback_data="buy_family"))
    markup.add(types.InlineKeyboardButton("🔙 گەڕانەوە", callback_data="main_menu"))
    return markup

def plan_duration_keyboard(plan_type):
    markup = types.InlineKeyboardMarkup()
    for key, name in DURATION_NAMES.items():
        dur_num = key.split("_")[0]  # "1", "3", etc.
        markup.add(types.InlineKeyboardButton(
            f"{name} - {PLANS[plan_type]['prices'][key]:,} د.ع",
            callback_data=f"duration_{plan_type}_{dur_num}"
        ))
    markup.add(types.InlineKeyboardButton("🔙 گەڕانەوە", callback_data="menu_plans"))
    return markup

def payment_method_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 FIB", callback_data="pay_fib"))
    markup.add(types.InlineKeyboardButton("💳 FastPay", callback_data="pay_fastpay"))
    markup.add(types.InlineKeyboardButton("💎 TON", callback_data="pay_ton"))
    markup.add(types.InlineKeyboardButton("💵 USDT", callback_data="pay_usdt"))
    markup.add(types.InlineKeyboardButton("🔙 گەڕانەوە", callback_data="menu_plans"))
    return markup
