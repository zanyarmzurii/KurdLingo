"""Persian (Farsi) language data."""

LANGUAGE_DATA = {
    "beginner": {
        "lessons": [
            {
                "title": "احوالپرسی",
                "vocabulary": [
                    {"kurdish": "سڵاو", "translation": "سلام", "example": "سلام، چطوری؟"},
                    {"kurdish": "بەڵێ", "translation": "بله", "example": "بله، من آمادهام."},
                    {"kurdish": "نەخێر", "translation": "نه", "example": "نه، متشکرم."},
                    {"kurdish": "تکایە", "translation": "لطفاً", "example": "لطفاً این را بخوان."},
                    {"kurdish": "سپاس", "translation": "متشکرم", "example": "متشکرم از کمکت."},
                ],
                "examples": ["سلام، چطوری؟", "بله، من آمادهام.", "نه، متشکرم.", "لطفاً این را بخوان.", "متشکرم از کمکت."],
                "quiz_questions": [
                    {"question": "سلام" ": بە کوردی", "options": ["سڵاو", "سپاس", "بەڵێ", "تکایە"], "correct": 0},
                ]
            },
        ],
        "final_quiz": []
    },
    "intermediate": {
        "lessons": [
            {
                "title": "زمان گذشته",
                "vocabulary": [
                    {"kurdish": "چووم", "translation": "رفتم", "example": "دیروز به شهر رفتم."},
                    {"kurdish": "خوارد", "translation": "خوردم", "example": "سیب خوردم."},
                ],
                "examples": ["دیروز به شهر رفتم.", "سیب خوردم."],
                "quiz_questions": []
            },
        ],
        "final_quiz": []
    },
    "advanced": {
        "lessons": [
            {
                "title": "جملات شرطی",
                "vocabulary": [
                    {"kurdish": "ئەگەر", "translation": "اگر", "example": "اگر بیایی، میرویم."},
                ],
                "examples": ["اگر بیایی، میرویم."],
                "quiz_questions": []
            },
        ],
        "final_quiz": []
    }
}
