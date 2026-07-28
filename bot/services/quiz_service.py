"""
Quiz Service: Generates quizzes, validates answers, and tracks results.
"""
import random
from typing import List, Dict
from bot.database import db
from bot.config import QUIZ_SETTINGS, logger

class QuizService:
    async def generate_quiz(self, lang_code: str, level: str, num_questions: int = 20) -> List[Dict]:
        """
        Generate a quiz from the question bank for the given language and level.
        Returns a list of question dicts with 'question', 'options', 'correct', 'explanation', 'id'.
        """
        questions = await self._fetch_questions(lang_code, level)
        if not questions:
            # Fallback to a set of built-in questions if DB empty
            questions = self._builtin_questions(lang_code, level)
        if len(questions) < num_questions:
            num_questions = len(questions)
        selected = random.sample(questions, num_questions)
        # Shuffle options for each question
        for q in selected:
            opts = q['options']
            correct_idx = q['correct']
            correct_text = opts[correct_idx]
            shuffled = opts[:]
            random.shuffle(shuffled)
            new_correct = shuffled.index(correct_text)
            q['options'] = shuffled
            q['correct'] = new_correct
        return selected

    async def _fetch_questions(self, lang_code: str, level: str) -> List[Dict]:
        async with db.get_connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM quiz_questions WHERE language=? AND level=? AND is_active=1",
                (lang_code, level)
            )
            rows = await cursor.fetchall()
            return [self._row_to_question(row) for row in rows]

    def _row_to_question(self, row) -> Dict:
        import json
        options = json.loads(row['options']) if isinstance(row['options'], str) else row['options']
        return {
            "id": row['id'],
            "question": row['question_text'],
            "options": options,
            "correct": row['correct_answer'],
            "explanation": row.get('explanation', ''),
            "difficulty": row.get('difficulty', 1),
            "points": row.get('points', 10)
        }

    def _builtin_questions(self, lang_code: str, level: str) -> List[Dict]:
        """Fallback built-in questions (can be extended)."""
        # Minimal set; real implementation would load from data/languages/
        sample = [
            {"id": 0, "question": "وەرگێڕانی 'سڵاو' بە ئینگلیزی", "options": ["Hello", "Goodbye", "Thanks", "Please"], "correct": 0, "explanation": "", "difficulty": 1, "points": 10},
            {"id": 1, "question": "وەرگێڕانی 'کتێب'", "options": ["Book", "Pen", "Table", "Chair"], "correct": 0, "explanation": "", "difficulty": 1, "points": 10},
            {"id": 2, "question": "وەرگێڕانی 'ئاو'", "options": ["Water", "Fire", "Air", "Earth"], "correct": 0, "explanation": "", "difficulty": 1, "points": 10},
            {"id": 3, "question": "I am a student", "options": ["من قوتابییم", "من مامۆستام", "من پزیشکم", "من ئەندازیارم"], "correct": 0, "explanation": "", "difficulty": 2, "points": 10},
            {"id": 4, "question": "ڕابردووی 'eat'", "options": ["Ate", "Eaten", "Eats", "Eating"], "correct": 0, "explanation": "", "difficulty": 2, "points": 10},
            {"id": 5, "question": "واتای 'beautiful'", "options": ["جوان", "پیسبوو", "گەورە", "بچووک"], "correct": 0, "explanation": "", "difficulty": 2, "points": 10},
            {"id": 6, "question": "She ___ to school.", "options": ["goes", "go", "going", "gone"], "correct": 0, "explanation": "", "difficulty": 3, "points": 10},
        ]
        return sample

    async def save_quiz_result(self, user_id: int, lang_code: str, level: str, score: int, total: int,
                               xp: int, coins: int, passed: bool, time_taken: int = 0,
                               answers_detail: str = '[]'):
        async with db.get_connection() as conn:
            await conn.execute("""
                INSERT INTO quiz_results 
                (user_id, language, level, total_questions, correct_answers, score_percentage, xp_earned, coins_earned, passed, time_taken_seconds, answers_detail)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, lang_code, level, total, score,
                  (score / total) * 100 if total > 0 else 0, xp, coins, passed, time_taken, answers_detail))
            await conn.commit()
