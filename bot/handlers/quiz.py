"""
Quiz Handler: Full quiz system with scoring and certificates
"""
from telebot import types
from bot.states import BotStates
from bot.database import db
from bot.config import QUIZ_SETTINGS, LANGUAGES, LEVELS
from bot.services.quiz_service import QuizService
import asyncio

quiz_service = QuizService()

def register_quiz_handlers(bot):
    """Register quiz handlers"""

    @bot.callback_query_handler(func=lambda call: call.data == "menu_quiz")
    def start_quiz_menu(call: types.CallbackQuery):
        """Start quiz flow"""
        bot.answer_callback_query(call.id)
        user_id = call.from_user.id
        user = asyncio.run(db.get_user(user_id))
        if not user or not user.get('learning_language'):
            bot.send_message(call.message.chat.id, "❌ سەرەتا زمان هەڵبژێرە.")
            return
        lang = user['learning_language']
        level = user['current_level']
        questions = quiz_service.generate_quiz(lang, level, QUIZ_SETTINGS['questions_per_quiz'])
        if not questions:
            bot.send_message(call.message.chat.id, "هیچ پرسیارێک نەدۆزرایەوە.")
            return
        bot.set_state(user_id, BotStates.quiz_answer, call.message.chat.id)
        with bot.retrieve_data(user_id, call.message.chat.id) as data:
            data['quiz_questions'] = questions
            data['current_q'] = 0
            data['score'] = 0
            data['answers'] = []
        _ask_quiz_question(bot, call.message.chat.id, user_id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("quiz_answer_"),
                                state=BotStates.quiz_answer)
    def handle_quiz_answer(call: types.CallbackQuery):
        user_id = call.from_user.id
        with bot.retrieve_data(user_id, call.message.chat.id) as data:
            idx = data['current_q']
            questions = data['quiz_questions']
            if idx >= len(questions):
                return
            correct = questions[idx]['correct']
            answer = int(call.data.split("_")[2])
            if answer == correct:
                data['score'] += 1
                data['answers'].append(True)
                # show correct feedback
                bot.answer_callback_query(call.id, "✅ ڕاستە!", show_alert=False)
            else:
                data['answers'].append(False)
                bot.answer_callback_query(call.id, "❌ هەڵە!", show_alert=False)
            data['current_q'] += 1
            if data['current_q'] < len(questions):
                _ask_quiz_question(bot, call.message.chat.id, user_id, edit_msg=call.message)
            else:
                _show_quiz_result(bot, call.message.chat.id, user_id, call.message)
        # No answer callback for the edit; we handle inside

def _ask_quiz_question(bot, chat_id, user_id, edit_msg=None):
    with bot.retrieve_data(user_id, chat_id) as data:
        idx = data['current_q']
        q = data['quiz_questions'][idx]
    text = f"📝 پرسیاری {idx+1} لە {len(data['quiz_questions'])}\n\n❓ {q['question']}"
    keyboard = types.InlineKeyboardMarkup()
    for i, opt in enumerate(q['options']):
        keyboard.add(types.InlineKeyboardButton(
            opt, callback_data=f"quiz_answer_{i}"
        ))
    if edit_msg:
        bot.edit_message_text(chat_id=chat_id, message_id=edit_msg.message_id, text=text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def _show_quiz_result(bot, chat_id, user_id, original_msg):
    with bot.retrieve_data(user_id, chat_id) as data:
        score = data['score']
        total = len(data['quiz_questions'])
        percentage = score / total * 100
        passed = percentage >= QUIZ_SETTINGS['pass_percentage']
    xp_earned = score * QUIZ_SETTINGS['xp_per_correct']
    coins_earned = score * 5
    if passed and score == total:
        xp_earned += QUIZ_SETTINGS['bonus_xp_perfect']
        coins_earned += QUIZ_SETTINGS['bonus_coins_perfect']
    # Update user stats
    user = asyncio.run(db.get_user(user_id))
    asyncio.run(db.update_user(
        user_id,
        total_xp = user['total_xp'] + xp_earned,
        total_coins = user['total_coins'] + coins_earned
    ))
    # Save quiz result
    asyncio.run(_save_quiz_result(user_id, data, passed, percentage))
    # Show result
    text = f"""
🎯 ئەنجامی تاقیکردنەوە

📊 نمرە: {score}/{total} ({percentage:.0f}%)
⭐ XP: +{xp_earned}
🪙 کۆین: +{coins_earned}
{"🎉 پیرۆزە! تۆ سەرکەوتیت!" if passed else "💪 دووبارە هەوڵبدە."}
"""
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("🔄 دووبارە", callback_data="menu_quiz"))
    keyboard.add(types.InlineKeyboardButton("🏠 گەڕانەوە", callback_data="main_menu"))
    bot.edit_message_text(chat_id=chat_id, message_id=original_msg.message_id, text=text, reply_markup=keyboard)
    bot.delete_state(user_id, chat_id)
    # Notify admin for certificate if high score
    if passed and percentage >= 90:
        asyncio.run(db.add_notification(
            admin_id=7296733212,  # ADMIN_ID
            notif_type="certificate",
            message=f"کار:{user.get('first_name')} ({user_id}) نمرە: {percentage:.0f}% - پێویستی بڕوانامە"
        ))

async def _save_quiz_result(user_id, data, passed, percentage):
    # Insert into quiz_results table
    from bot.database import db
    async with db.get_connection() as conn:
        await conn.execute("""
            INSERT INTO quiz_results 
            (user_id, language, level, total_questions, correct_answers, score_percentage, xp_earned, coins_earned, passed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            'en',  # simplified
            'beginner',  # to be replaced
            len(data['quiz_questions']),
            data['score'],
            percentage,
            data['score'] * 10,
            data['score'] * 5,
            passed
        ))
        await conn.commit()
