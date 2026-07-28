"""Complete English course data: Beginner, Intermediate, Advanced."""

LANGUAGE_DATA = {
    "beginner": {
        "lessons": [
            {
                "title": "Greetings & Introductions",
                "vocabulary": [
                    {"kurdish": "سڵاو", "translation": "Hello", "example": "سڵاو، چۆنی؟ → Hello, how are you?"},
                    {"kurdish": "بەڵێ", "translation": "Yes", "example": "بەڵێ، من ئامادەیم → Yes, I am ready."},
                    {"kurdish": "نەخێر", "translation": "No", "example": "نەخێر، سپاس → No, thank you."},
                    {"kurdish": "تکایە", "translation": "Please", "example": "تکایە ئەمە بخوێنەوە → Please read this."},
                    {"kurdish": "سپاس", "translation": "Thank you", "example": "سپاس بۆ هاوکاریت → Thank you for your help."},
                ],
                "examples": ["Hello, how are you?", "Yes, I am ready.", "No, thank you.", "Please read this.", "Thank you for your help."],
                "quiz_questions": [
                    {"question": "وەرگێڕانی 'سڵاو' بە ئینگلیزی", "options": ["Hello", "Goodbye", "Thanks", "Sorry"], "correct": 0},
                    {"question": "وەرگێڕانی 'سپاس' بە ئینگلیزی", "options": ["Please", "Sorry", "Thank you", "Hello"], "correct": 2},
                    {"question": "بە واتای 'Yes' کامەیە؟", "options": ["نەخێر", "بەڵێ", "تکایە", "سپاس"], "correct": 1},
                ]
            },
            {
                "title": "Numbers 1-10",
                "vocabulary": [
                    {"kurdish": "یەک", "translation": "One", "example": "یەک کتێب → One book"},
                    {"kurdish": "دوو", "translation": "Two", "example": "دوو قوتابی → Two students"},
                    {"kurdish": "سێ", "translation": "Three", "example": "سێ سێو → Three apples"},
                    {"kurdish": "چوار", "translation": "Four", "example": "چوار پەنجەرە → Four windows"},
                    {"kurdish": "پێنج", "translation": "Five", "example": "پێنج ڕۆژ → Five days"},
                ],
                "examples": ["One book", "Two students", "Three apples", "Four windows", "Five days"],
                "quiz_questions": [
                    {"question": "ژمارە ٣ بە ئینگلیزی", "options": ["Two", "Three", "Four", "Five"], "correct": 1},
                    {"question": "پێنج = ?", "options": ["Four", "Five", "Six", "Seven"], "correct": 1},
                ]
            },
        ],
        "final_quiz": [
            {"question": "وەرگێڕانی 'تکایە'", "options": ["Yes", "Please", "No", "Thank you"], "correct": 1},
            {"question": "One + Two = ?", "options": ["Three", "Four", "Five", "Six"], "correct": 0},
        ]
    },
    "intermediate": {
        "lessons": [
            {
                "title": "Daily Routines",
                "vocabulary": [
                    {"kurdish": "هەستان", "translation": "Wake up", "example": "من سەعات ٧ هەڵدەستم → I wake up at 7."},
                    {"kurdish": "خواردن", "translation": "Eat", "example": "نان دەخۆم → I eat bread."},
                    {"kurdish": "چوون", "translation": "Go", "example": "دەچمە بازاڕ → I go to the market."},
                    {"kurdish": "خەوتن", "translation": "Sleep", "example": "شەو زوو دەخەوم → I sleep early at night."},
                ],
                "examples": ["I wake up at 7.", "I eat bread.", "I go to the market.", "I sleep early at night."],
                "quiz_questions": [
                    {"question": "رستەی 'من سەعات ٧ هەڵدەستم' بە ئینگلیزی", "options": ["I wake up at 7", "I sleep at 7", "I eat at 7", "I go at 7"], "correct": 0},
                ]
            },
            {
                "title": "Past Tense",
                "vocabulary": [
                    {"kurdish": "چووم", "translation": "Went", "example": "دوێنێ چوومە شار → Yesterday I went to the city."},
                    {"kurdish": "خوارد", "translation": "Ate", "example": "سێوێکم خوارد → I ate an apple."},
                ],
                "examples": ["Yesterday I went to the city.", "I ate an apple."],
                "quiz_questions": [
                    {"question": "ڕابردووی 'eat'", "options": ["Ate", "Eaten", "Eats", "Eating"], "correct": 0},
                    {"question": "چووم = ?", "options": ["Go", "Went", "Gone", "Going"], "correct": 1},
                ]
            }
        ],
        "final_quiz": [
            {"question": "I ___ to school yesterday.", "options": ["go", "went", "going", "gone"], "correct": 1},
        ]
    },
    "advanced": {
        "lessons": [
            {
                "title": "Complex Sentences",
                "vocabulary": [
                    {"kurdish": "ئەگەر", "translation": "If", "example": "ئەگەر تۆ بێی، دەچین → If you come, we will go."},
                    {"kurdish": "بەڵام", "translation": "But", "example": "باشه، بەڵام گرانه → It's good, but expensive."},
                    {"kurdish": "لەبەر ئەوەی", "translation": "Because", "example": "نەهاتم لەبەر ئەوەی نەخۆش بووم → I didn't come because I was sick."},
                ],
                "examples": ["If you come, we will go.", "It's good, but expensive.", "I didn't come because I was sick."],
                "quiz_questions": [
                    {"question": "وەرگێڕانی 'ئەگەر تۆ بێی، دەچین'", "options": ["If you come, we will go", "When you come, we go", "You come and we go", "We go if you come"], "correct": 0},
                ]
            },
            {
                "title": "Passive Voice",
                "vocabulary": [
                    {"kurdish": "نووسرا", "translation": "Was written", "example": "کتێبەکە نووسرا → The book was written."},
                    {"kurdish": "بینی", "translation": "Was seen", "example": "فیلمەکە بینرا → The film was seen."},
                ],
                "examples": ["The book was written.", "The film was seen."],
                "quiz_questions": [
                    {"question": "Passive of 'write': The book ___ yesterday.", "options": ["was written", "is written", "wrote", "written"], "correct": 0},
                ]
            }
        ],
        "final_quiz": [
            {"question": "The letter ___ by her.", "options": ["was sent", "sent", "sends", "is sending"], "correct": 0},
        ]
    }
}
