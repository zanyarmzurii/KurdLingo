"""
Start Handler: Welcome, language selection, level placement, main menu
"""
from telebot import types
from telebot.handler_backends import State, StatesGroup
from bot.states import BotStates
from bot.config import LANGUAGES, LEVELS, LEVEL_ORDER, ADMIN_USERNAME
from bot.database import db
from bot.keyboards.main_menu import main_menu_keyboard
from bot.keyboards.language_select import language_select_keyboard
from bot.keyboards.plans import plans_keyboard
import asyncio

def register_start_handlers(bot):
    """Register all start-related handlers"""

    @bot.message_handler(commands=['start'])
    def handle_start(message: types.Message):
        """Handle /start command"""
        user_id = message.from_user.id
        user = message.from_user
        # Add user to database
        asyncio.run(db.add_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        ))
        
        # Check for referral code in deep link
        ref_code = None
        if len(message.text.split()) > 1:
            ref_code = message.text.split()[1]
            # Process referral
            asyncio.run(_process_referral(bot, user_id, ref_code))
        
        # Check if user already completed setup
        existing = asyncio.run(db.get_user(user_id))
        if existing and existing.get('learning_language'):
            # Show main menu
            show_main_menu(bot, message.chat.id, user_id)
            return

        # New user flow: welcome and language selection
        welcome_text = f"""
🌟 بەخێربێی بۆ KurdLingo!

👋 سڵاو {user.first_name}ی ئازیز!

ئەمە یەکەم بۆتی فێرکاری زمانە بە کوردی بەهدینی! 🚀

📚 لەم بۆتەدا دەتوانیت:
• ١٠ زمانی جیهانی فێربیت
• بە شێوازی یاری و ڕاهێنان
• بڕوانامەی فەرمی وەربگریت
• لەگەڵ هاوڕێکانت ڕکابەری بکەیت

━━━━━━━━━━━━━━━━━━

🎯 با دەستپێبکەین!
"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            "🚀 دەستپێبکەین", callback_data="start_setup"
        ))
        keyboard.add(types.InlineKeyboardButton(
            "📞 پەیوەندی", url=f"https://t.me/{ADMIN_USERNAME}"
        ))
        bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)


    @bot.callback_query_handler(func=lambda call: call.data == "start_setup")
    def start_setup(call: types.CallbackQuery):
        """Language selection"""
        bot.answer_callback_query(call.id)
        text = "🌍 **کام زمان دەتەوێت فێربیت؟**\n\nزمانێک هەڵبژێرە:"
        keyboard = language_select_keyboard()
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=keyboard
        )
        bot.set_state(call.from_user.id, BotStates.select_language, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"),
                                state=BotStates.select_language)
    def select_language(call: types.CallbackQuery):
        """Save selected language and go to level selection"""
        lang_code = call.data.split("_")[1]
        user_id = call.from_user.id
        asyncio.run(db.update_user(user_id, learning_language=lang_code))
        
        text = "✅ زمان هەڵبژێردرا!\n\n📊 ئێستا با ئاستی خۆت دیاری بکەین:"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(
            "🌱 دەستپێکی - Beginner", callback_data="level_beginner"
        ))
        keyboard.add(types.InlineKeyboardButton(
            "🌿 ناوەندی - Intermediate", callback_data="level_intermediate"
        ))
        keyboard.add(types.InlineKeyboardButton(
            "🌳 پێشکەوتوو - Advanced", callback_data="level_advanced"
        ))
        keyboard.add(types.InlineKeyboardButton(
            "🎯 تاقیکردنەوەی ئاست", callback_data="level_test"
        ))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=keyboard
        )
        bot.set_state(user_id, BotStates.select_level, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("level_"),
                                state=BotStates.select_level)
    def select_level(call: types.CallbackQuery):
        """Process level selection or level test request"""
        if call.data == "level_test":
            # Forward to language_test handler (just change state)
            bot.set_state(call.from_user.id, BotStates.level_test, call.message.chat.id)
            from .language_test import start_level_test
            start_level_test(bot, call)
            return
        
        level = call.data.split("_")[1]
        user_id = call.from_user.id
        asyncio.run(db.update_user(user_id, current_level=level))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ ئاستی {LEVELS.get(level, level)} هەڵبژێردرا!\n\n🎉 دەست بە فێربوون دەکەیت!"
        )
        bot.delete_state(user_id, call.message.chat.id)
        show_main_menu(bot, call.message.chat.id, user_id)

    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def main_menu_callback(call: types.CallbackQuery):
        """Return to main menu"""
        show_main_menu(bot, call.message.chat.id, call.from_user.id)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data == "back_main")
    def back_main(call: types.CallbackQuery):
        """Back to main menu from various places"""
        show_main_menu(bot, call.message.chat.id, call.from_user.id)
        bot.answer_callback_query(call.id)

def show_main_menu(bot_instance, chat_id, user_id):
    """Display the main menu"""
    user = asyncio.run(db.get_user(user_id))
    if user is None:
        # Should not happen, but fallback
        bot_instance.send_message(chat_id, "❌ تکایە /start بکە.")
        return

    lang_code = user.get('learning_language', 'en')
    lang_emoji = LANGUAGES.get(lang_code, {}).get('emoji', '🌍')
    lang_name = LANGUAGES.get(lang_code, {}).get('name_badini', 'دیارینەکراوە')
    level = user.get('current_level', 'beginner')
    level_name = LEVELS.get(level, 'دەستپێکی')
    plan_type = user.get('plan_type', 'free')
    plan_emoji = {'free': '🌟', 'plus': '⭐', 'premium': '👑', 'family': '🏠'}.get(plan_type, '🌟')

    text = f"""
🏠 پێشکەشکاری سەرەکی

👤 بەخێربێی، {bot_instance.get_chat(user_id).first_name}!
{lang_emoji} زمان: {lang_name}
📊 ئاست: {level_name}
{plan_emoji} پلان: {plan_type.upper()}
🪙 کۆین: {user.get('total_coins', 0):,}
⭐ XP: {user.get('total_xp', 0):,}

━━━━━━━━━━━━━━━━━━
چی دەکەیت؟ 😊
"""
    keyboard = main_menu_keyboard()
    bot_instance.send_message(chat_id, text, reply_markup=keyboard)

async def _process_referral(bot, user_id, ref_code):
    """Process referral link"""
    import sqlite3
    from bot.config import REFERRAL_SETTINGS
    conn = sqlite3.connect(db.db_path)
    cursor = conn.execute("SELECT user_id FROM users WHERE referral_code = ?", (ref_code,))
    row = cursor.fetchone()
    if row:
        referrer_id = row[0]
        if referrer_id != user_id:
            await db.update_user(user_id, referred_by=referrer_id)
            await db.add_referral(referrer_id, user_id)
    conn.close()
