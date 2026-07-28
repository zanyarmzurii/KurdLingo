"""
Referral System Handlers
"""
from telebot import types
from bot.database import db
from bot.config import REFERRAL_SETTINGS, BOT_USERNAME
import asyncio

def register_referral_handlers(bot):
    """Register referral handlers"""

    @bot.callback_query_handler(func=lambda call: call.data == "menu_referral")
    def referral_info(call: types.CallbackQuery):
        """Display referral info and stats"""
        user_id = call.from_user.id
        user = asyncio.run(db.get_user(user_id))
        if not user:
            return
        ref_code = user.get('referral_code', 'N/A')
        ref_count = user.get('referral_count', 0)
        link = f"https://t.me/{BOT_USERNAME}?start={ref_code}"
        text = f"""
👥 سیستەمی دەعوەت

کۆدی دەعوەتی تۆ: `{ref_code}`
لینکی دەعوەت: {link}

📊 دەعوەتکراوەکان: {ref_count}
💰 کۆینی دەعوەت: {user.get('referral_coins_earned', 0)}

🎁 خەڵاتەکان:
• بۆ هەر دەعوەتێک +{REFERRAL_SETTINGS['coins_per_referral']} کۆین
• دەعوەتی ٥ کەس: +{REFERRAL_SETTINGS['bonus_referrals_5']} کۆین
• دەعوەتی ١٠ کەس: +{REFERRAL_SETTINGS['bonus_referrals_10']} کۆین
• دەعوەتی ٢٥ کەس: +{REFERRAL_SETTINGS['bonus_referrals_25']} کۆین

🏆 بۆ دەعوەتی ٢٥ کەس پلانی پرێمیەم بێبەرامبەر!
"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📤 هاوپشککردنی لینک", url=f"https://t.me/share/url?url={link}"))
        keyboard.add(types.InlineKeyboardButton("🔙 گەڕانەوە", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
