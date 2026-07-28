import telebot
from telebot import types
import config
import database

bot = telebot.TeleBot(config.BOT_TOKEN)
database.init_db()

# 🚀 1. /start Command
@bot.message_handler(commands=['start'])
def start_cmd(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username or "N/A"
    
    args = message.text.split()
    referrer_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None

    user = database.get_user(user_id)
    if not user:
        database.add_user(user_id, first_name, username, referrer_id)
        if referrer_id and referrer_id != user_id:
            bot.send_message(user_id, "🎁 تۆ ب لێنکا هەڤالەکێ خۆ هاتییە ناڤ بۆتی! **١ هەفتی پلانا پریمیۆم** دیاری بۆ تە هاتە چالاکرن.")
            
            ref_user = database.get_user(referrer_id)
            if ref_user and ref_user[5] == 25:
                database.update_user_field(referrer_id, "plan", "Premium")
                bot.send_message(referrer_id, "🎉 تە ٢٥ هەڤالێن خۆ داعوەت کرن! **١ مەهـ پلانا پریمیۆم** دیاری بۆ تە هاتە چالاکرن.")

    welcome_msg = f"""
🌹 **ب خێر هاتی {first_name} بۆ بۆتێ KurdLingo (کوردلینگۆ)!**

ئەڤ بۆتە ب ژیڕیا دەستکرد و ب **کوردییا بەهدینی یا پەتی** هاتییە ئامادەکرن دا کو فێری ۱۰ زمانێن سەرەکی یێن جیهانێ ببی.

---
💎 **پلان و ئاشتراکێن بۆتی (دگەل ٧ ڕۆژێن تێستێ بەلاش):**

🟢 **پلانا بەلاش:** ٥ پرسیارێن ڕۆژانە.
🔵 **پلانا پڵاس (٥,٠٠٠ IQD/مەهـ):** پرسیارێن بێ سنور + فێربوونا دەنگی.
🟣 **پلانا پریمیۆم (١٠,٠٠٠ IQD/مەهـ):** هەمی تایبەتمەندی + AI + بڕوانامە ل داویا هەر ئاستەکی.
👨‍👩‍👧‍👦 **پلانا خێزانی (٢٥,٠٠٠ IQD/مەهـ):** بۆ ٥ ئەکاونتان ب هەمی تایبەتمەندییان.

🎁 **دیاریا ڤەخوێندنی:** ٢٥ کەسان ب لێنکا خۆ داخاز بکە $\rightarrow$ **١ مەهـ پریمیۆم دیاری وەربگرە!**
🔗 **لینکێ تە یێ تایبەت:** `https://t.me/KurdLingoBot?start={user_id}`

---
💳 **ژ بۆ کڕین و چالاکرنێ (پارتەدانا راستەوخۆ):**
📞 **FastPay / FIB:** `{config.FASTPAY_NUMBER}`
💎 **TON:** `{config.TON_WALLET}`
💵 **USDT (TRC20):** `{config.USDT_TRC20}`
👤 **پەیوەندی ب ئادمنی بکه:** {config.ADMIN_USERNAME}

---
لطفاً زمانێ کو تۆ دڤێی فێر ببی هەڵبژێڕە:
"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    for code, name in config.LANGUAGES.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=f"setlang_{code}"))
        
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup)

# 🎯 2. Choose Level
@bot.callback_query_handler(func=lambda call: call.data.startswith('setlang_'))
def choose_level(call):
    lang_code = call.data.split('_')[1]
    lang_name = config.LANGUAGES[lang_code]
    
    database.update_user_field(call.from_user.id, "current_lang", lang_name)

    level_msg = f"""
🎯 **زمانێ هەڵبژارتی:** {lang_name}

لطفاً ئاستێ خۆ دیار بکە دا کو پرسیار و وانە بۆ تە بهێنە ڕێکخستن:
"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🌱 ژ دەستپێکێ (پیت، خواندن، نڤێسین)", callback_data=f"lvl_start_{lang_code}"),
        types.InlineKeyboardButton("📈 ژ ئاستێ تە (پشکنینا ئاستی)", callback_data=f"lvl_test_{lang_code}"),
        types.InlineKeyboardButton("⚡ باشترکرنێ (پەیڤ و ڕێزمانا پێشکەفتی)", callback_data=f"lvl_adv_{lang_code}"),
        types.InlineKeyboardButton("🏆 تەمامکرنا تەواو (فێربوونا کامل دگەل بڕوانامێ)", callback_data=f"lvl_full_{lang_code}")
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=level_msg, reply_markup=markup)

# 📝 3. Quiz Engine
@bot.callback_query_handler(func=lambda call: call.data.startswith('lvl_'))
def start_quiz(call):
    data = call.data.split('_')
    level_type = data[1]
    lang_code = data[2]
    
    quiz_msg = """
📚 **وانەیا ١: ڕستە و پەیڤێن سەرەکی**

❓ پرسیار: وەرگێڕانا ڕستەیا **"Good Morning"** بۆ کوردییا بەهدینی چییە؟
"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("A) شەڤ باش", callback_data="ans_wrong"),
        types.InlineKeyboardButton("B) سپێدە باش / ڕۆژباش", callback_data=f"ans_correct_{lang_code}_{level_type}"),
        types.InlineKeyboardButton("C) ب خێر هاتی", callback_data="ans_wrong"),
        types.InlineKeyboardButton("D) دەستخۆش", callback_data="ans_wrong")
    )
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=quiz_msg, reply_markup=markup)

# ✅ 4. Check Answer & Certificate Alert to Admin
@bot.callback_query_handler(func=lambda call: call.data.startswith('ans_'))
def handle_answer(call):
    user_id = call.from_user.id
    first_name = call.from_user.first_name
    username = call.from_user.username or "N/A"

    if call.data == "ans_wrong":
        bot.answer_callback_query(call.id, "❌ بەرسڤا تە شاشە! دیسان تاقیبکە.", show_alert=True)
    else:
        data = call.data.split('_')
        lang_code = data[2]
        level_type = data[3]
        
        bot.answer_callback_query(call.id, "✅ بەرسڤا تە ڕاستە! +١٠ خال (XP)", show_alert=True)
        
        cert_msg_user = f"""
🎉 **پیرۆزە {first_name}!**

تۆ ب سەرکەفتن ئاستێ **[{level_type.upper()}]** د زمانێ **[{config.LANGUAGES[lang_code]}]** دا ب دوماهیک ئینا.

📜 **داخوازیا بڕوانامەیێ:**
داخوازیا تە شاندرا بۆ ئادمنی. ئادمن دێ ب جوانترین دیزاین بڕوانامەیا تە ب ناڤێ تە ئامادەکەت و بۆ تە ڕوانێت!
"""
        bot.send_message(user_id, cert_msg_user)

        # 📩 ئاگاداری بۆ تە (ئادمنی)
        admin_alert = f"""
🎓 **داخوازیا بڕوانامەییا نوی د ناڤ KurdLingo دا!**

👤 **ناڤ:** {first_name} (@{username})
🆔 **User ID:** `{user_id}`
🌍 **زمان:** {config.LANGUAGES[lang_code]}
📊 **ئاست:** {level_type.upper()}

لطفاً بڕوانامەیێ ب ناڤێ **{first_name}** ئامادە بکە و بڕوانە ب فەرمانا:
`/activate {user_id} Premium`
"""
        bot.send_message(config.ADMIN_ID, admin_alert)

# ⚙️ 5. Admin Activation
@bot.message_handler(commands=['activate'])
def manual_activate(message):
    if message.from_user.id != config.ADMIN_ID:
        return
    try:
        args = message.text.split()
        target_user = int(args[1])
        plan_name = args[2]
        
        database.update_user_field(target_user, "plan", plan_name)
        bot.send_message(target_user, f"🎉 ئاشتراکا تە ب سەرکەفتن بۆ پلانا **[{plan_name}]** هاتە چالاکرن!")
        bot.reply_to(message, f"✅ پلان ب سەرکەفتن بۆ `{target_user}` هاتە چالاکرن.")
    except Exception:
        bot.reply_to(message, "❌ شاشی! فۆرمات: `/activate USER_ID PLAN_NAME`")

print("🤖 بۆتێ KurdLingo ئامادەیە و ب سەرکەفتن کار دکەت...")
bot.polling(none_stop=True)
