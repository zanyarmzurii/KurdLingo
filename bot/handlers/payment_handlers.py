"""
Payment Handlers: Plan purchase flow with IQD pricing and receipt upload
"""
from telebot import types
from bot.states import BotStates
from bot.database import db
from bot.config import PLANS, PAYMENT_METHODS, ADMIN_ID, DURATION_MAP, DURATION_NAMES, ADMIN_USERNAME
from bot.keyboards.plans import plans_keyboard, plan_duration_keyboard, payment_method_keyboard
import asyncio

def register_payment_handlers(bot):
    """Register payment related handlers"""

    @bot.callback_query_handler(func=lambda call: call.data == "menu_plans")
    def show_plans(call: types.CallbackQuery):
        """Show all plans"""
        bot.answer_callback_query(call.id)
        text = "💎 پلانەکانی KurdLingo\n\nپلانێک هەڵبژێرە بۆ بینینی نرخ و تایبەتمەندییەکان:"
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=plans_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
    def buy_plan(call: types.CallbackQuery):
        """Select plan type"""
        plan_type = call.data.split("_")[1]  # plus, premium, family
        bot.answer_callback_query(call.id)
        text = f"📦 پلانی {PLANS[plan_type]['name']}\n\nماوەی پلانەکە هەڵبژێرە:"
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=plan_duration_keyboard(plan_type)
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("duration_"))
    def select_duration(call: types.CallbackQuery):
        """Select duration and go to payment method"""
        _, plan_type, dur_key = call.data.split("_", 2)
        duration = DURATION_MAP.get(dur_key, "1_month")
        price = PLANS[plan_type]['prices'][duration]
        bot.answer_callback_query(call.id)
        bot.set_state(call.from_user.id, BotStates.payment_method, call.message.chat.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['plan_type'] = plan_type
            data['duration'] = duration
            data['amount'] = price
        text = f"""
💳 هەڵبژاردنی ڕێگای پارەدان

📦 پلان: {PLANS[plan_type]['name']}
📅 ماوە: {DURATION_NAMES.get(duration, duration)}
💰 بڕ: {price:,} د.ع

ڕێگایەک هەڵبژێرە:
"""
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=payment_method_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"),
                                state=BotStates.payment_method)
    def payment_method_selected(call: types.CallbackQuery):
        """Show payment details based on selected method"""
        method = call.data.split("_")[1]  # fib, fastpay, ton, usdt
        bot.answer_callback_query(call.id)
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            amount = data['amount']
        if method == "fib":
            detail = f"ژمارەی FIB: {PAYMENT_METHODS['FIB']}\nناو: {ADMIN_USERNAME}"
        elif method == "fastpay":
            detail = f"ژمارەی FastPay: {PAYMENT_METHODS['FASTPAY']}\nناو: {ADMIN_USERNAME}"
        elif method == "ton":
            detail = f"ناونیشانی TON:\n`{PAYMENT_METHODS['TON']}`"
        elif method == "usdt":
            detail = f"ناونیشانی USDT (TRC20):\n`{PAYMENT_METHODS['USDT_TRC20']}`"
        else:
            detail = "ڕێگایەکی تر هەڵبژێرە"
        text = f"""
💳 پارەدان بە {method.upper()}

💰 بڕی پارە: {amount:,} د.ع

{detail}

━━━━━━━━━━━━━━━━━━
📸 دوای ناردنی پارەکە، وێنەی پسوڵەکە بنێرە ئێرە.
"""
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("📸 ناردنی وێنەی پسوڵە", callback_data="send_receipt"))
        keyboard.add(types.InlineKeyboardButton("🔙 گەڕانەوە", callback_data="menu_plans"))
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=None
        )
        bot.set_state(call.from_user.id, BotStates.payment_receipt, call.message.chat.id)

    @bot.callback_query_handler(func=lambda call: call.data == "send_receipt",
                                state=BotStates.payment_receipt)
    def ask_receipt(call: types.CallbackQuery):
        """Prompt to send photo"""
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "📸 تکایە وێنەی پسوڵەی پارەدان بنێرە.")
        # Keep state payment_receipt to catch photo

    @bot.message_handler(content_types=['photo'], state=BotStates.payment_receipt)
    def handle_receipt(message: types.Message):
        """Process receipt photo"""
        user_id = message.from_user.id
        with bot.retrieve_data(user_id, message.chat.id) as data:
            plan_type = data.get('plan_type')
            amount = data.get('amount')
            duration = data.get('duration')
        if not plan_type or not amount:
            bot.send_message(message.chat.id, "❌ زانیاری پارەدان نەدۆزرایەوە. دووبارە هەوڵبدە /plans")
            bot.delete_state(user_id, message.chat.id)
            return
        # Save payment to DB
        file_id = message.photo[-1].file_id
        payment_id = asyncio.run(db.add_payment(
            user_id=user_id,
            plan_type=plan_type,
            amount=amount,
            payment_method="manual",
            receipt_file_id=file_id,
            receipt_message_id=str(message.message_id)
        ))
        # Notify admin
        admin_text = f"""
🔔 پارەدانی نوێ #{payment_id}

👤 بەکارهێنەر: {message.from_user.first_name} (ID: {user_id})
📦 پلان: {plan_type}
💰 بڕ: {amount:,} د.ع
📅 ماوە: {duration}

📸 وێنەکە لە خوارەوە:
"""
        bot.send_photo(ADMIN_ID, file_id, caption=admin_text)
        bot.send_message(ADMIN_ID, f"بۆ پەسەندکردن: /verify_{payment_id} یان /reject_{payment_id}")
        bot.send_message(message.chat.id, "✅ وێنەکەت نێردرا. ئەدمین پشتڕاستی دەکاتەوە (١٥-٣٠ خولەک).")
        bot.delete_state(user_id, message.chat.id)

    # Admin verification commands
    @bot.message_handler(commands=['verify'])
    def verify_payment_cmd(message: types.Message):
        """Admin: verify payment"""
        if message.from_user.id != ADMIN_ID:
            bot.send_message(message.chat.id, "❌ دەستڕاگەیشتن ڕێگەپێنەدراوە")
            return
        try:
            payment_id = int(message.text.split("_")[1])
        except:
            bot.send_message(message.chat.id, "فەرمانی ڕاست: /verify_ID")
            return
        success = asyncio.run(db.verify_payment(payment_id, ADMIN_ID))
        if success:
            # Grant plan to user
            import sqlite3
            conn = sqlite3.connect(db.db_path)
            cur = conn.execute("SELECT user_id, plan_type, duration FROM payments WHERE id=?", (payment_id,))
            row = cur.fetchone()
            if row:
                user_id, plan_type, duration = row
                # Calculate days
                dur_map = {"1_month":30, "3_months":90, "6_months":180, "1_year":365}
                days = dur_map.get(duration, 30)
                asyncio.run(db.update_user_plan(user_id, plan_type, days))
                bot.send_message(user_id, f"🎉 پیرۆزە! پلانی {plan_type} بۆ ماوەی {days} ڕۆژ چالاک کرا!")
            conn.close()
            bot.send_message(message.chat.id, f"✅ پارەدان #{payment_id} پەسەندکرا.")
        else:
            bot.send_message(message.chat.id, "❌ نەتوانرا پەسەند بکرێت.")

    @bot.message_handler(commands=['reject'])
    def reject_payment_cmd(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            return
        try:
            payment_id = int(message.text.split("_")[1])
        except:
            bot.send_message(message.chat.id, "فەرمان: /reject_ID")
            return
        # Update payment status to rejected
        import sqlite3
        conn = sqlite3.connect(db.db_path)
        conn.execute("UPDATE payments SET status='rejected' WHERE id=?", (payment_id,))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, f"❌ پارەدان #{payment_id} ڕەتکرایەوە.")
