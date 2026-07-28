"""
KurdLingo Bot - Main Entry Point
Enterprise-grade Telegram Bot for Language Learning in Badini Kurdish
"""

import sys
import asyncio
import signal
import logging
from datetime import datetime
from typing import Optional

import telebot
from telebot import types, TeleBot
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

from bot.config import (
    BOT_TOKEN, BOT_NAME, ADMIN_ID, DEVELOPER_ID, ADMIN_USERNAME,
    logger, PAYMENT_METHODS, LANGUAGES, LEVELS, PLANS
)
from bot.database import db, init_database

state_storage = StateMemoryStorage()

bot = TeleBot(BOT_TOKEN, state_storage=state_storage, parse_mode=None)

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

user_context = {}

def get_user_context(user_id: int) -> dict:
    """Get or create user context"""
    if user_id not in user_context:
        user_context[user_id] = {}
    return user_context[user_id]

def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == ADMIN_ID or user_id == DEVELOPER_ID

def format_number(number: int) -> str:
    """Format number with commas"""
    return f"{number:,}"

def get_plan_price(plan_type: str, duration: str) -> Optional[int]:
    """Get plan price for given duration"""
    if plan_type not in PLANS or 'prices' not in PLANS[plan_type]:
        return None
    return PLANS[plan_type]['prices'].get(duration)

def create_inline_keyboard(buttons: list, row_width: int = 2) -> types.InlineKeyboardMarkup:
    """Create inline keyboard from button list"""
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    for row in buttons:
        if isinstance(row, list):
            markup.add(*[types.InlineKeyboardButton(**btn) if isinstance(btn, dict) 
                        else btn for btn in row])
        else:
            markup.add(types.InlineKeyboardButton(**row) if isinstance(row, dict) 
                      else row)
    return markup

def create_reply_keyboard(buttons: list, resize: bool = True) -> types.ReplyKeyboardMarkup:
    """Create reply keyboard"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=resize)
    for row in buttons:
        markup.add(*[types.KeyboardButton(btn) for btn in row])
    return markup

@bot.message_handler(commands=['start'])
def handle_start(message: types.Message):
    """Handle /start command"""
    user_id = message.from_user.id
    user = message.from_user
    
    asyncio.run(db.add_user(
        user_id=user_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    ))
    
    if len(message.text.split()) > 1:
        ref_code = message.text.split()[1]
        existing_user = asyncio.run(db.get_user(user_id))
        if existing_user and not existing_user.get('referred_by'):
            ref_user = None
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cursor = conn.execute(
                "SELECT user_id FROM users WHERE referral_code = ?", (ref_code,)
            )
            row = cursor.fetchone()
            if row:
                ref_user = row[0]
            conn.close()
            
            if ref_user and ref_user != user_id:
                asyncio.run(db.update_user(user_id, referred_by=ref_user))
                asyncio.run(db.add_referral(ref_user, user_id))
    
    welcome_text = f"""
🌟 بەخێربێی بۆ {BOT_NAME}! 

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

    keyboard = create_inline_keyboard([
        [{"text": "🚀 دەستپێبکەین", "callback_data": "start_setup"}],
        [{"text": "📞 پەیوەندی بە پشتگیری", "url": f"https://t.me/{ADMIN_USERNAME}"}]
    ])
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=keyboard)

@bot.message_handler(commands=['help'])
def handle_help(message: types.Message):
    """Handle /help command"""
    help_text = f"""
📚 ڕێنمایی بەکارهێنانی {BOT_NAME}

🎯 فەرمانە سەرەکییەکان:
/start - دەستپێکردنەوە
/help - ڕێنمایی
/lessons - وانەکان
/quiz - تاقیکردنەوە
/profile - پرۆفایلت
/plans - پلانەکان
/referral - دەعوەتی هاوڕێ
/contact - پەیوەندی بە پشتگیری

━━━━━━━━━━━━━━━━━━

📖 چۆنیەتی بەکارهێنان:
1️⃣ زمانێک هەڵبژێرە بۆ فێربوون
2️⃣ ئاستی خۆت دیاری بکە
3️⃣ وانەکان تەواو بکە
4️⃣ لە تاقیکردنەوەکان بەشداری بکە
5️⃣ بڕوانامە وەربگرە

━━━━━━━━━━━━━━━━━━

📞 بۆ یارمەتی زیاتر:
@{ADMIN_USERNAME}
"""
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['profile'])
def handle_profile(message: types.Message):
    """Show user profile"""
    user_id = message.from_user.id
    user = asyncio.run(db.get_user(user_id))
    
    if not user:
        bot.send_message(message.chat.id, "❌ پرۆفایل نەدۆزرایەوە. تکایە /start بکە.")
        return
    
    lang_code = user.get('learning_language', 'en')
    lang_name = LANGUAGES.get(lang_code, {}).get('name_badini', 'دیارینەکراوە')
    
    level = user.get('current_level', 'beginner')
    level_name = LEVELS.get(level, 'دیارینەکراوە')
    
    plan_type = user.get('plan_type', 'free')
    plan_name = PLANS.get(plan_type, {}).get('name', 'بەلاش')
    
    profile_text = f"""
👤 پرۆفایلی {user.get('first_name', 'بەکارهێنەر')}

━━━━━━━━━━━━━━━━━━

🆔 ID: {user_id}
📚 زمانی فێربوون: {lang_name}
📊 ئاست: {level_name}
💎 پلان: {plan_name}
🪙 کۆین: {format_number(user.get('total_coins', 0))}
⭐ XP: {format_number(user.get('total_xp', 0))}
🔥 زنجیرە: {user.get('current_streak', 0)} ڕۆژ
📖 وانە تەواوکراوەکان: {format_number(user.get('total_lessons_completed', 0))}
👥 دەعوەتکراوەکان: {user.get('referral_count', 0)}

━━━━━━━━━━━━━━━━━━
"""
    
    keyboard = create_inline_keyboard([
        [{"text": "📊 ئاماری زیاتر", "callback_data": "detailed_stats"}],
        [{"text": "⚙️ ڕێکخستنەکان", "callback_data": "settings"}],
        [{"text": "🏠 پێشکەشکاری سەرەکی", "callback_data": "main_menu"}]
    ])
    
    bot.send_message(message.chat.id, profile_text, reply_markup=keyboard)

@bot.message_handler(commands=['contact'])
def handle_contact(message: types.Message):
    """Contact admin"""
    contact_text = f"""
📞 پەیوەندی بە پشتگیرییەوە

━━━━━━━━━━━━━━━━━━

👨‍💻 ئەدمین: @{ADMIN_USERNAME}
📱 ژمارە: {PAYMENT_METHODS['ADMIN_PHONE']}

💳 ڕێگاکانی پارەدان:
• FIB: {PAYMENT_METHODS['FIB']}
• FastPay: {PAYMENT_METHODS['FASTPAY']}

━━━━━━━━━━━━━━━━━━

⏰ کاتی کارکردن: ٢٤/٧
"""
    bot.send_message(message.chat.id, contact_text)

@bot.callback_query_handler(func=lambda call: call.data == "main_menu")
def handle_main_menu_callback(call: types.CallbackQuery):
    """Return to main menu"""
    show_main_menu(call.message.chat.id, call.from_user.id)
    bot.answer_callback_query(call.id)

def show_main_menu(chat_id: int, user_id: int):
    """Display main menu"""
    user = asyncio.run(db.get_user(user_id))
    
    lang_code = user.get('learning_language', 'en') if user else 'en'
    lang_emoji = LANGUAGES.get(lang_code, {}).get('emoji', '🌍')
    lang_name = LANGUAGES.get(lang_code, {}).get('name_badini', 'دیارینەکراوە') if user else 'دیارینەکراوە'
    
    level = user.get('current_level', 'beginner') if user else 'beginner'
    level_name = LEVELS.get(level, 'دەستپێکی') if user else 'دەستپێکی'
    
    plan_type = user.get('plan_type', 'free') if user else 'free'
    plan_emoji = PLANS.get(plan_type, {}).get('emoji', '🌟') if user else '🌟'
    
    text = f"""
🏠 پێشکەشکاری سەرەکی

👤 بەخێربێی، {bot.get_chat(user_id).first_name if user_id else 'بەکارهێنەر'}!
{lang_emoji} زمانی فێربوون: {lang_name}
📊 ئاست: {level_name}
{plan_emoji} پلان: {plan_type.upper() if user else 'بەلاش'}
🪙 کۆین: {format_number(user.get('total_coins', 0)) if user else 0}
⭐ XP: {format_number(user.get('total_xp', 0)) if user else 0}

━━━━━━━━━━━━━━━━━━
چی دەکەیت؟ 😊
"""
    
    keyboard = create_inline_keyboard([
        [{"text": "📚 وانەکان", "callback_data": "menu_lessons"}],
        [{"text": "📝 ڕاهێنان", "callback_data": "menu_practice"},
         {"text": "🎯 تاقیکردنەوە", "callback_data": "menu_quiz"}],
        [{"text": "🏆 پلەبەندی", "callback_data": "menu_leaderboard"}],
        [{"text": "👥 دەعوەتی هاوڕێ", "callback_data": "menu_referral"},
         {"text": "🎓 بڕوانامەکان", "callback_data": "menu_certificates"}],
        [{"text": "💎 پلانەکان", "callback_data": "menu_plans"}],
        [{"text": "⚙️ ڕێکخستنەکان", "callback_data": "menu_settings"},
         {"text": "📞 پشتگیری", "callback_data": "menu_support"}],
    ])
    
    bot.send_message(chat_id, text, reply_markup=keyboard)

@bot.message_handler(commands=['admin'])
def handle_admin_command(message: types.Message):
    """Admin panel access"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ دەستڕاگەیشتن ڕێگەپێنەدراوە!")
        return
    
    stats = asyncio.run(db.get_statistics())
    
    admin_text = f"""
🔐 پانێڵی ئەدمین - {BOT_NAME}

━━━━━━━━━━━━━━━━━━

📊 ئامارەکان:
👥 بەکارهێنەران: {format_number(stats['total_users'])}
📅 چالاکی ئەمڕۆ: {format_number(stats['active_users_today'])}
👑 پرێمیەم: {format_number(stats['total_premium'])}
🏠 خێزانی: {format_number(stats['total_family'])}
💰 کۆی داهات: {format_number(stats['total_revenue'])} د.ع
⏳ پارەدانی چاوەڕوان: {format_number(stats['pending_payments'])}

━━━━━━━━━━━━━━━━━━

فەرمانەکانی ئەدمین:
/admin - پانێڵی ئەدمین
/stats - ئامارەکان
/pending - پارەدانە چاوەڕوانەکان
/broadcast - پەیام بۆ هەمووان
/users - لیستی بەکارهێنەران
/export - هەناردەکردنی داتا
"""
    
    keyboard = create_inline_keyboard([
        [{"text": "📊 ئامارەکان", "callback_data": "admin_stats"}],
        [{"text": "💳 پارەدانەکان", "callback_data": "admin_payments"}],
        [{"text": "👥 بەکارهێنەران", "callback_data": "admin_users"}],
        [{"text": "📬 پەیام", "callback_data": "admin_broadcast"}],
        [{"text": "🎓 بڕوانامەکان", "callback_data": "admin_certificates"}],
    ])
    
    bot.send_message(message.chat.id, admin_text, reply_markup=keyboard)

@bot.message_handler(commands=['stats'])
def handle_stats_command(message: types.Message):
    """Show statistics (admin only)"""
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ دەستڕاگەیشتن ڕێگەپێنەدراوە!")
        return
    
    stats = asyncio.run(db.get_statistics())
    
    stats_text = f"""
📊 ئامارەکانی {BOT_NAME}

━━━━━━━━━━━━━━━━━━

👥 کۆی بەکارهێنەران: {format_number(stats['total_users'])}
📅 چالاکی ئەمڕۆ: {format_number(stats['active_users_today'])}
👑 پرێمیەم: {format_number(stats['total_premium'])}
🏠 خێزانی: {format_number(stats['total_family'])}
💳 کۆی پارەدانەکان: {format_number(stats['total_payments'])}
💰 کۆی داهات: {format_number(stats['total_revenue'])} د.ع
⏳ چاوەڕوان: {format_number(stats['pending_payments'])}

━━━━━━━━━━━━━━━━━━
📈 بۆت بەردەوام لە گەشەکردندایە! 🚀
"""
    bot.send_message(message.chat.id, stats_text)

@bot.message_handler(commands=['pending'])
def handle_pending_payments(message: types.Message):
    """Show pending payments (admin only)"""
    if not is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "❌ دەستڕاگەیشتن ڕێگەپێنەدراوە!")
        return
    
    pending = asyncio.run(db.get_pending_payments())
    
    if not pending:
        bot.send_message(message.chat.id, "✅ هیچ پارەدانێکی چاوەڕوان نییە!")
        return
    
    for payment in pending:
        payment_text = f"""
💳 پارەدانی نوێ #{payment['id']}

━━━━━━━━━━━━━━━━━━
👤 بەکارهێنەر: {payment.get('first_name', 'نەناسراو')}
🆔 ID: {payment['user_id']}
📦 پلان: {payment['plan_type']}
💰 بڕ: {format_number(payment['amount'])} د.ع
💳 ڕێگا: {payment['payment_method']}
📅 کات: {payment['payment_date']}
━━━━━━━━━━━━━━━━━━
"""
        keyboard = create_inline_keyboard([
            [{"text": "✅ پەسەندکردن", "callback_data": f"verify_payment_{payment['id']}"}],
            [{"text": "❌ ڕەتکردنەوە", "callback_data": f"reject_payment_{payment['id']}"}],
        ])
        
        bot.send_message(message.chat.id, payment_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith("verify_payment_"))
def handle_verify_payment(call: types.CallbackQuery):
    """Verify payment callback"""
    if not is_admin(call.from_user.id):
        bot.answer_callback_query(call.id, "❌ دەستڕاگەیشتن ڕێگەپێنەدراوە!")
        return
    
    payment_id = int(call.data.split("_")[2])
    
    success = asyncio.run(db.verify_payment(payment_id, call.from_user.id))
    
    if success:
        bot.answer_callback_query(call.id, "✅ پارەدان پەسەندکرا!")
        bot.edit_message_caption(
            caption=f"{call.message.caption}\n\n✅ پەسەندکرا لەلایەن {call.from_user.first_name}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id
        )
    else:
        bot.answer_callback_query(call.id, "❌ هەڵەیەک ڕوویدا!")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message: types.Message):
    """Handle all other messages"""
    if message.text and message.text.startswith('/'):
        bot.send_message(
            message.chat.id,
            "❌ فەرمان نەناسرایەوە.\n/help بکە بۆ بینینی ڕێنمایی."
        )
        return
    
    bot.send_message(
        message.chat.id,
        "👋 بەخێربێی! تکایە /start بکە بۆ دەستپێکردن."
    )

def signal_handler(sig, frame):
    """Handle shutdown signals"""
    logger.info("Shutting down bot...")
    bot.stop_polling()
    sys.exit(0)

def main():
    """Main bot entry point"""
    logger.info(f"Starting {BOT_NAME} Bot...")
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    asyncio.run(init_database())
    
    logger.info(f"{BOT_NAME} is running...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        logger.error(f"Polling error: {e}")

if __name__ == "__main__":
    main()
