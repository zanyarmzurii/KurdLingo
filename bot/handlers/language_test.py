"""
Language Level Placement Test Handler
"""
from telebot import types
from bot.states import BotStates
from bot.database import db
from bot.config import LANGUAGES, LEVELS, QUIZ_SETTINGS
import asyncio
import random

def register_language_test_handlers(bot):
    """Register level test handlers"""

    @bot.callback_query_handler(func=lambda call: call.data == "level_test",
                                state=BotStates.select_level)
    def start_level_test(call: types.CallbackQuery):
        """Start level test"""
        bot.answer_callback_query(call.id)
        user_id = call.from_user.id
        user = asyncio.run(db.get_user(user_id))
        if not user:
            return
        lang_code = user.get('learning_language', 'en')
        # Get placement test questions (simplified: 10 questions from mixed levels)
        questions = _generate_placement_test(lang_code, 10)
        bot.set_state(user_id, BotStates.level_test, call.message.chat.id)
        with bot.retrieve_data(user_id, call.message.chat.id) as data:
            data['test_questions'] = questions
            data['current_q'] = 0
            data['score'] = 0
            data['answers'] = []
        _ask_question(bot, call.message.chat.id, user_id)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("test_answer_"),
                                state=BotStates.level_test)
    def handle_test_answer(call: types.CallbackQuery):
        """Process answer in level test"""
        user_id = call.from_user.id
        with bot.retrieve_data(user_id, call.message.chat.id) as data:
            if 'current_q' not in data:
                return
            q_idx = data['current_q']
            questions = data['test_questions']
            if q_idx >= len(questions):
                return
            correct = questions[q_idx]['correct']
            answer = int(call.data.split("_")[2])
            if answer == correct:
                data['score'] += 1
                data['answers'].append(True)
            else:
                data['answers'].append(False)
            data['current_q'] += 1
            if data['current_q'] < len(questions):
                _ask_question(bot, call.message.chat.id, user_id, edit_msg=call.message)
            else:
                _show_test_result(bot, call.message.chat.id, user_id, call.message)
        bot.answer_callback_query(call.id)

def _generate_placement_test(lang_code, num_questions=10):
    """Generate placement test questions (mocked; would come from database)"""
    # This should be fetched from DB or language data files
    # For now, use hardcoded sample for English
    sample = [
        {"q": "وەرگێڕانی 'سڵاو' بە ئینگلیزی:", "opts": ["Hello", "Goodbye", "Thanks", "Please"], "correct": 0, "level": "beginner"},
        {"q": "وەرگێڕانی 'کتێب':", "opts": ["Book", "Pen", "Table", "Chair"], "correct": 0, "level": "beginner"},
        {"q": "وەرگێڕانی 'ئاو':", "opts": ["Water", "Fire", "Air", "Earth"], "correct": 0, "level": "beginner"},
        {"q": "رستەی 'I am a student' بە کوردی:", "opts": ["من قوتابییم", "من مامۆستام", "من پزیشکم", "من ئەندازیارم"], "correct": 0, "level": "intermediate"},
        {"q": "ڕابردووی 'eat':", "opts": ["Ate", "Eaten", "Eats", "Eating"], "correct": 0, "level": "intermediate"},
        {"q": "واتای 'beautiful':", "opts": ["جوان", "پیسبوو", "گەورە", "بچووک"], "correct": 0, "level": "intermediate"},
        {"q": "هەڵبژاردنی ڕاستی ڕێزمانی: 'She ___ to school.'", "opts": ["goes", "go", "going", "gone"], "correct": 0, "level": "advanced"},
        {"q": "وەرگێڕانی 'حکومەت':", "opts": ["Government", "Parliament", "Minister", "President"], "correct": 0, "level": "advanced"},
        {"q": "هاومانای 'happy':", "opts": ["Glad", "Sad", "Angry", "Tired"], "correct": 0, "level": "advanced"},
        {"q": "پرسیاری پێکەوەبەستن: 'If I ___ rich, I would travel.'", "opts": ["were", "was", "am", "be"], "correct": 0, "level": "advanced"},
    ]
    random.shuffle(sample)
    return sample[:num_questions]

def _ask_question(bot, chat_id, user_id, edit_msg=None):
    with bot.retrieve_data(user_id, chat_id) as data:
        idx = data['current_q']
        q = data['test_questions'][idx]
    text = f"❓ پرسیاری {idx+1} لە {len(data['test_questions'])}\n\n{q['q']}"
    keyboard = types.InlineKeyboardMarkup()
    for i, opt in enumerate(q['opts']):
        keyboard.add(types.InlineKeyboardButton(
            opt, callback_data=f"test_answer_{i}"
        ))
    if edit_msg:
        bot.edit_message_text(chat_id=chat_id, message_id=edit_msg.message_id,
                              text=text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, reply_markup=keyboard)

def _show_test_result(bot, chat_id, user_id, original_msg):
    with bot.retrieve_data(user_id, chat_id) as data:
        score = data['score']
        total = len(data['test_questions'])
    percentage = score / total * 100 if total > 0 else 0
    # Determine level based on score: 0-3 beginner, 4-6 intermediate, 7+ advanced
    if score >= 7:
        level = "advanced"
    elif score >= 4:
        level = "intermediate"
    else:
        level = "beginner"
    
    asyncio.run(db.update_user(user_id, current_level=level))
    level_name = LEVELS.get(level, level)
    
    text = f"""
🎯 ئەنجامی تاقیکردنەوەی ئاست

📊 نمرە: {score}/{total} ({percentage:.0f}%)
🏅 ئاستی پێشنیارکراو: {level_name}

✅ ئێستا دەتوانیت بەم ئاستە دەست بە فێربوون بکەیت!
"""
    bot.edit_message_text(chat_id=chat_id, message_id=original_msg.message_id, text=text)
    bot.delete_state(user_id, chat_id)
    from .start import show_main_menu
    show_main_menu(bot, chat_id, user_id)
