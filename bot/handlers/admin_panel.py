"""
Admin Panel Handlers: Broadcast, Statistics, User Management
"""
from telebot import types
from bot.database import db
from bot.config import ADMIN_ID, BOT_NAME
import asyncio

def register_admin_handlers(bot):
    """Register admin-specific handlers"""

    @bot.message_handler(commands=['admin'])
    def admin_panel(message: types.Message):
        """Admin panel"""
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "❌ دەستڕاگەیشتن ڕێگەپێنەدراوە.")
            return
        stats = asyncio.run(db.get_statistics())
        text = f"""
🔐 پانێڵی ئەدمین - {BOT_NAME}

👥 بەکارهێنەران: {stats['total_users']}
📅 چالاک: {stats['active_users_today']}
👑 پرێمیەم: {stats['total_premium']}
🏠 خێزانی: {stats['total_family']}
💰 داهات: {stats['total_revenue']:,} د.ع
⏳ چاوەڕوان: {stats['pending_payments']}

📬 فەرمانەکان:
/admin - پانێڵ
/broadcast - پەیام بۆ هەمووان
/stats - ئامار
/pending - پارەدانی چاوەڕوان
"""
        bot.send_message(message.chat.id, text)

    @bot.message_handler(commands=['stats'])
    def stats_cmd(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            return
        stats = asyncio.run(db.get_statistics())
        text = f"""
📊 ئامارەکان

👥 کۆ: {stats['total_users']}
📅 ئەمڕۆ: {stats['active_users_today']}
👑 پرێمیەم: {stats['total_premium']}
🏠 خێزانی: {stats['total_family']}
💰 کۆی داهات: {stats['total_revenue']:,} د.ع
⏳ چاوەڕوان: {stats['pending_payments']}
"""
        bot.send_message(message.chat.id, text)

    @bot.message_handler(commands=['pending'])
    def pending_cmd(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            return
        pending = asyncio.run(db.get_pending_payments())
        if not pending:
            bot.send_message(message.chat.id, "✅ هیچ پارەدانێکی چاوەڕوان نییە.")
            return
        for p in pending:
            p_text = f"""
💳 پارەدانی #{p['id']}
👤 {p.get('first_name','')} (ID:{p['user_id']})
💰 {p['amount']:,} د.ع
📦 {p['plan_type']}
📅 {p['payment_date']}
            """
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("✅ پەسەندکردن", callback_data=f"verify_payment_{p['id']}"))
            keyboard.add(types.InlineKeyboardButton("❌ ڕەتکردنەوە", callback_data=f"reject_payment_{p['id']}"))
            bot.send_message(message.chat.id, p_text, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("verify_payment_"))
    def verify_callback(call: types.CallbackQuery):
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ دەستڕاگەیشتن نییە")
            return
        payment_id = int(call.data.split("_")[2])
        success = asyncio.run(db.verify_payment(payment_id, ADMIN_ID))
        if success:
            # grant plan (same as in payment handler)
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cur = conn.execute("SELECT user_id, plan_type, duration FROM payments WHERE id=?", (payment_id,))
            row = cur.fetchone()
            if row:
                user_id, plan_type, duration = row
                dur_map = {"1_month":30, "3_months":90, "6_months":180, "1_year":365}
                days = dur_map.get(duration, 30)
                asyncio.run(db.update_user_plan(user_id, plan_type, days))
                bot.send_message(user_id, f"🎉 پلانی {plan_type} چالاک کرا!")
            conn.close()
            bot.edit_message_caption(caption=call.message.caption + "\n\n✅ پەسەندکرا", chat_id=call.message.chat.id, message_id=call.message.message_id)
        else:
            bot.answer_callback_query(call.id, "❌ هەڵە")
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reject_payment_"))
    def reject_callback(call: types.CallbackQuery):
        if call.from_user.id != ADMIN_ID:
            return
        payment_id = int(call.data.split("_")[2])
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        conn.execute("UPDATE payments SET status='rejected' WHERE id=?", (payment_id,))
        conn.commit()
        conn.close()
        bot.edit_message_caption(caption=call.message.caption + "\n\n❌ ڕەتکرایەوە", chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.answer_callback_query(call.id, "ڕەتکرایەوە")

    @bot.message_handler(commands=['broadcast'])
    def broadcast_cmd(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            return
        # Simple broadcast: admins sends text and it goes to all users
        msg_text = message.text.replace('/broadcast', '').strip()
        if not msg_text:
            bot.send_message(message.chat.id, "تکایە پەیامەکەت بنووسە دوای /broadcast")
            return
        # Get all user IDs
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        cur = conn.execute("SELECT user_id FROM users WHERE is_active=1")
        users = cur.fetchall()
        count = 0
        for (uid,) in users:
            try:
                bot.send_message(uid, "📢 پەیامی ئەدمین:\n\n" + msg_text)
                count += 1
            except:
                pass
        conn.close()
        bot.send_message(message.chat.id, f"✅ پەیام بۆ {count} بەکارهێنەر نێردرا.")
