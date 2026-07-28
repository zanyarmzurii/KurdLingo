"""
Lessons Handler: Manage lesson delivery
"""
from telebot import types
from bot.states import BotStates
from bot.database import db
from bot.config import LANGUAGES, LEVELS, PLANS
from bot.services.lesson_service import LessonService
import asyncio

lesson_service = LessonService()

def register_lessons_handlers(bot):
    """Register lesson-related handlers"""

    @bot.callback_query_handler(func=lambda call: call.data == "menu_lessons")
    def lessons_menu(call: types.CallbackQuery):
        """Show lessons menu"""
        bot.answer_callback_query(call.id)
        user_id = call.from_user.id
        user = asyncio.run(db.get_user(user_id))
        if not user or not user.get('learning_language'):
            bot.send_message(call.message.chat.id, "❌ سەرەتا زمانێک هەڵبژێرە. /start بکە.")
            return
        lang = user['learning_language']
        level = user['current_level']
        # Check daily limit
        plan_type = user.get('plan_type', 'free')
        daily_limit = PLANS[plan_type]['daily_lessons']
        completed_today = user.get('daily_lessons_completed', 0)
        if daily_limit != "unlimited" and completed_today >= daily_limit:
            bot.send_message(call.message.chat.id,
                f"📚 ئەمڕۆ {daily_limit} وانەت تەواوکردووە. بۆ وانەی زیاتر، پلانەکەت بەرز بکەرەوە.\n💎 /plans")
            return
        # Get next lesson
        lesson = lesson_service.get_next_lesson(lang, level, user_id)
        if not lesson:
            bot.send_message(call.message.chat.id, "🎉 هەموو وانەکانی ئەم ئاستەت تەواوکردووە! ئاستی دواتر تاقیبکەرەوە.")
            return
        _present_lesson(bot, call.message.chat.id, user_id, lesson)

    @bot.callback_query_handler(func=lambda call: call.data == "menu_practice")
    def practice_menu(call: types.CallbackQuery):
        """Practice (same as lesson for now)"""
        # For now, route to lessons menu
        lessons_menu(call)

def _present_lesson(bot, chat_id, user_id, lesson):
    """Display lesson content step by step"""
    # lesson is a dict with 'title', 'words', 'examples'
    text = f"📖 {lesson['title']}\n\n"
    # Show first word
    if lesson.get('words'):
        first = lesson['words'][0]
        text += f"🔤 وشە: {first['kurdish']} = {first['translation']}\n"
        if first.get('example'):
            text += f"📝 نموونە: {first['example']}\n"
    # Add navigation
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("▶️ دواتر", callback_data=f"lesson_next_{lesson['id']}"))
    keyboard.add(types.InlineKeyboardButton("❌ تەواوکردن", callback_data="lesson_finish"))
    bot.send_message(chat_id, text, reply_markup=keyboard)
    # Save state
    bot.set_state(user_id, BotStates.quiz_answer, chat_id)  # reuse quiz state
    with bot.retrieve_data(user_id, chat_id) as data:
        data['lesson'] = lesson
        data['lesson_word_idx'] = 0

    @bot.callback_query_handler(func=lambda call: call.data.startswith("lesson_next_"),
                                state=BotStates.quiz_answer)
    def next_word(call: types.CallbackQuery):
        user_id = call.from_user.id
        with bot.retrieve_data(user_id, call.message.chat.id) as data:
            lesson = data['lesson']
            idx = data['lesson_word_idx'] + 1
            data['lesson_word_idx'] = idx
            if idx < len(lesson['words']):
                word = lesson['words'][idx]
                text = f"🔤 وشە: {word['kurdish']} = {word['translation']}\n"
                if word.get('example'):
                    text += f"📝 نموونە: {word['example']}\n"
                keyboard = types.InlineKeyboardMarkup()
                keyboard.add(types.InlineKeyboardButton("▶️ دواتر", callback_data=f"lesson_next_{lesson['id']}"))
                keyboard.add(types.InlineKeyboardButton("❌ تەواوکردن", callback_data="lesson_finish"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=text, reply_markup=keyboard)
            else:
                # Lesson complete
                _finish_lesson(bot, call.message.chat.id, user_id, lesson)
        bot.answer_callback_query(call.id)

    @bot.callback_query_handler(func=lambda call: call.data == "lesson_finish",
                                state=BotStates.quiz_answer)
    def finish_lesson_callback(call: types.CallbackQuery):
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            lesson = data.get('lesson')
        if lesson:
            _finish_lesson(bot, call.message.chat.id, call.from_user.id, lesson)
        else:
            bot.send_message(call.message.chat.id, "وانە تەواو بوو.")
        bot.answer_callback_query(call.id)

def _finish_lesson(bot, chat_id, user_id, lesson):
    """Mark lesson as completed and reward user"""
    # Update progress
    asyncio.run(db.update_user(
        user_id,
        daily_lessons_completed = asyncio.run(_get_today_lessons(user_id)) + 1,
        total_lessons_completed = asyncio.run(db.get_user(user_id))['total_lessons_completed'] + 1,
        total_xp = asyncio.run(db.get_user(user_id))['total_xp'] + 50,
        total_coins = asyncio.run(db.get_user(user_id))['total_coins'] + 10
    ))
    bot.send_message(chat_id, "✅ وانە تەواو بوو! +50 XP, +10 کۆین")
    bot.delete_state(user_id, chat_id)

async def _get_today_lessons(user_id):
    from datetime import date
    user = await db.get_user(user_id)
    today = str(date.today())
    if user and user.get('daily_lessons_date') == today:
        return user['daily_lessons_completed']
    return 0
