"""Arabic language data for KurdLingo."""

LANGUAGE_DATA = {
    "beginner": {
        "lessons": [
            {
                "title": "التحيات والتعارف",
                "vocabulary": [
                    {"kurdish": "سڵاو", "translation": "مرحباً", "example": "سڵاو، چۆنی؟ → مرحباً، كيف حالك؟"},
                    {"kurdish": "بەڵێ", "translation": "نعم", "example": "بەڵێ، من ئامادەیم → نعم، أنا جاهز."},
                    {"kurdish": "نەخێر", "translation": "لا", "example": "نەخێر، سپاس → لا، شكراً."},
                    {"kurdish": "تکایە", "translation": "من فضلك", "example": "تکایە ئەمە بخوێنەوە → من فضلك اقرأ هذا."},
                    {"kurdish": "سپاس", "translation": "شكراً", "example": "سپاس بۆ هاوکاریت → شكراً على مساعدتك."},
                ],
                "examples": ["مرحباً، كيف حالك؟", "نعم، أنا جاهز.", "لا، شكراً.", "من فضلك اقرأ هذا.", "شكراً على مساعدتك."],
                "quiz_questions": [
                    {"question": "وشەی 'سڵاو' بە عەرەبی", "options": ["مرحباً", "وداعاً", "شكراً", "آسف"], "correct": 0},
                    {"question": "بە واتای 'شكراً' کامەیە؟", "options": ["تکایە", "سپاس", "بەڵێ", "نەخێر"], "correct": 1},
                ]
            },
            {
                "title": "الأرقام 1-10",
                "vocabulary": [
                    {"kurdish": "یەک", "translation": "واحد", "example": "یەک کتێب → كتاب واحد"},
                    {"kurdish": "دوو", "translation": "اثنان", "example": "دوو قوتابی → طالبان اثنان"},
                    {"kurdish": "سێ", "translation": "ثلاثة", "example": "سێ سێو → ثلاث تفاحات"},
                    {"kurdish": "چوار", "translation": "أربعة", "example": "چوار پەنجەرە → أربع نوافذ"},
                    {"kurdish": "پێنج", "translation": "خمسة", "example": "پێنج ڕۆژ → خمسة أيام"},
                ],
                "examples": ["كتاب واحد", "طالبان اثنان", "ثلاث تفاحات", "أربع نوافذ", "خمسة أيام"],
                "quiz_questions": [
                    {"question": "٣ بە عەرەبی", "options": ["اثنان", "ثلاثة", "أربعة", "خمسة"], "correct": 1},
                ]
            },
        ],
        "final_quiz": [
            {"question": "مرحباً" ": بە کوردی", "options": ["سڵاو", "سپاس", "بەڵێ", "تکایە"], "correct": 0},
        ]
    },
    "intermediate": {
        "lessons": [
            {
                "title": "الروتين اليومي",
                "vocabulary": [
                    {"kurdish": "هەستان", "translation": "الاستيقاظ", "example": "أستيقظ الساعة 7 → من سەعات ٧ هەڵدەستم"},
                    {"kurdish": "خواردن", "translation": "الأكل", "example": "آكل الخبز → نان دەخۆم"},
                ],
                "examples": ["أستيقظ الساعة 7", "آكل الخبز"],
                "quiz_questions": [
                    {"question": "أستيقظ = ?", "options": ["هەستان", "خواردن", "چوون", "خەوتن"], "correct": 0},
                ]
            },
        ],
        "final_quiz": [
            {"question": "آكل التفاح → بە کوردی", "options": ["سێو دەخۆم", "نان دەخۆم", "شیر دەخۆم", "گوێز دەخۆم"], "correct": 0},
        ]
    },
    "advanced": {
        "lessons": [
            {
                "title": "الجمل المعقدة",
                "vocabulary": [
                    {"kurdish": "ئەگەر", "translation": "إذا", "example": "إذا جئت، سنذهب → ئەگەر تۆ بێی، دەچین"},
                ],
                "examples": ["إذا جئت، سنذهب"],
                "quiz_questions": [
                    {"question": "وەرگێڕانی 'إذا جئت، سنذهب'", "options": ["ئەگەر تۆ بێی، دەچین", "کاتێک تۆ دێی، دەچین", "تۆ دێی و دەچین", "ئەگەر دەچین، تۆ دێی"], "correct": 0},
                ]
            },
        ],
        "final_quiz": []
    }
}
