"""Turkish language data."""

LANGUAGE_DATA = {
    "beginner": {
        "lessons": [
            {
                "title": "Tanışma ve Selamlaşma",
                "vocabulary": [
                    {"kurdish": "سڵاو", "translation": "Merhaba", "example": "Merhaba, nasılsın?"},
                    {"kurdish": "بەڵێ", "translation": "Evet", "example": "Evet, hazırım."},
                    {"kurdish": "نەخێر", "translation": "Hayır", "example": "Hayır, teşekkürler."},
                    {"kurdish": "تکایە", "translation": "Lütfen", "example": "Lütfen bunu oku."},
                    {"kurdish": "سپاس", "translation": "Teşekkürler", "example": "Yardımın için teşekkürler."},
                ],
                "examples": ["Merhaba, nasılsın?", "Evet, hazırım.", "Hayır, teşekkürler.", "Lütfen bunu oku.", "Yardımın için teşekkürler."],
                "quiz_questions": [
                    {"question": "'سڵاو' Türkçesi", "options": ["Merhaba", "Güle güle", "Teşekkürler", "Üzgünüm"], "correct": 0},
                ]
            },
            {
                "title": "Sayılar 1-5",
                "vocabulary": [
                    {"kurdish": "یەک", "translation": "Bir", "example": "Bir kitap"},
                    {"kurdish": "دوو", "translation": "İki", "example": "İki öğrenci"},
                    {"kurdish": "سێ", "translation": "Üç", "example": "Üç elma"},
                ],
                "examples": ["Bir kitap", "İki öğrenci", "Üç elma"],
                "quiz_questions": [
                    {"question": "2 sayısı Türkçe", "options": ["Bir", "İki", "Üç", "Dört"], "correct": 1},
                ]
            },
        ],
        "final_quiz": []
    },
    "intermediate": {
        "lessons": [
            {
                "title": "Geçmiş Zaman",
                "vocabulary": [
                    {"kurdish": "چووم", "translation": "Gittim", "example": "Dün şehre gittim."},
                    {"kurdish": "خوارد", "translation": "Yedim", "example": "Elma yedim."},
                ],
                "examples": ["Dün şehre gittim.", "Elma yedim."],
                "quiz_questions": [
                    {"question": "Gitmek geçmiş zaman 1.tekil: Ben ____", "options": ["gittim", "gidiyorum", "giderim", "gideceğim"], "correct": 0},
                ]
            },
        ],
        "final_quiz": []
    },
    "advanced": {
        "lessons": [
            {
                "title": "Koşullu Cümleler",
                "vocabulary": [
                    {"kurdish": "ئەگەر", "translation": "Eğer", "example": "Eğer gelirsen, gideriz."},
                ],
                "examples": ["Eğer gelirsen, gideriz."],
                "quiz_questions": []
            },
        ],
        "final_quiz": []
    }
}
