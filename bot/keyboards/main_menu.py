from telebot import types

def main_menu_keyboard():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📚 وانەکان", callback_data="menu_lessons"))
    markup.add(types.InlineKeyboardButton("📝 ڕاهێنان", callback_data="menu_practice"),
               types.InlineKeyboardButton("🎯 تاقیکردنەوە", callback_data="menu_quiz"))
    markup.add(types.InlineKeyboardButton("🏆 پلەبەندی", callback_data="menu_leaderboard"))
    markup.add(types.InlineKeyboardButton("👥 دەعوەتی هاوڕێ", callback_data="menu_referral"),
               types.InlineKeyboardButton("🎓 بڕوانامەکان", callback_data="menu_certificates"))
    markup.add(types.InlineKeyboardButton("💎 پلانەکان", callback_data="menu_plans"))
    markup.add(types.InlineKeyboardButton("⚙️ ڕێکخستنەکان", callback_data="menu_settings"),
               types.InlineKeyboardButton("📞 پشتگیری", callback_data="menu_support"))
    return markup
