"""
Certificates Handler
"""
from telebot import types
from bot.database import db
import asyncio

def register_certificates_handlers(bot):
    """Register certificate handlers"""

    @bot.callback_query_handler(func=lambda call: call.data == "menu_certificates")
    def show_certificates(call: types.CallbackQuery):
        """Show user certificates"""
        user_id = call.from_user.id
        user = asyncio.run(db.get_user(user_id))
        if not user:
            return
        # Fetch certificates
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cur = conn.execute(
            "SELECT language, level, score, certificate_code, issued_date FROM certificates WHERE user_id=? AND is_valid=1",
            (user_id,))
        certs = cur.fetchall()
        conn.close()
        if not certs:
            text = "🎓 هیچ بڕوانامەیەکت نییە. تاقیکردنەوە تەواو بکە بۆ بەدەستهێنانی."
        else:
            text = "🎓 بڕوانامەکانت:\n\n"
            for lang, level, score, code, date in certs:
                text += f"📜 زمان: {lang}, ئاست: {level}, نمرە: {score}%, کۆد: {code}\n"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("🏠 گەڕانەوە", callback_data="main_menu"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=text, reply_markup=keyboard)
        bot.answer_callback_query(call.id)
