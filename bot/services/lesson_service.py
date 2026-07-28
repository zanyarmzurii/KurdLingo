"""
Lesson Service: Manages lesson content delivery, progress, and limits.
"""
import random
from typing import Dict, List, Optional
from bot.database import db
from bot.config import PLANS, LEVELS, LANGUAGES, logger

class LessonService:
    def __init__(self):
        self._lesson_cache = {}

    async def get_next_lesson(self, lang_code: str, level: str, user_id: int) -> Optional[Dict]:
        """
        Retrieve the next unseen lesson for a user in the given language and level.
        """
        # Get all lessons for lang/level that are active
        lessons = await self._fetch_lessons(lang_code, level)
        if not lessons:
            logger.warning(f"No lessons found for {lang_code}/{level}")
            return None

        # Get completed lesson IDs for the user
        completed_ids = await self._get_completed_lesson_ids(user_id, lang_code, level)

        # Filter out completed lessons
        available = [l for l in lessons if l['id'] not in completed_ids]
        if not available:
            # All lessons completed; could move to next level logic
            return None

        # Return the next in order (by lesson_number)
        available.sort(key=lambda x: x['lesson_number'])
        next_lesson = available[0]
        # Structure the output to match what handlers expect
        return {
            "id": next_lesson['id'],
            "title": next_lesson['title'],
            "words": self._parse_vocabulary(next_lesson.get('vocabulary', '[]')),
            "examples": self._parse_examples(next_lesson.get('examples', '[]')),
            "content": next_lesson.get('content', ''),
            "lesson_number": next_lesson['lesson_number']
        }

    def _parse_vocabulary(self, vocab_str: str) -> List[Dict[str, str]]:
        import json
        try:
            vocab_list = json.loads(vocab_str)
            return vocab_list
        except Exception as e:
            logger.error(f"Failed to parse vocabulary: {e}")
            return []

    def _parse_examples(self, examples_str: str) -> List[Dict[str, str]]:
        import json
        try:
            return json.loads(examples_str)
        except Exception as e:
            logger.error(f"Failed to parse examples: {e}")
            return []

    async def _fetch_lessons(self, lang_code: str, level: str) -> List[Dict]:
        async with db.get_connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM lesson_content WHERE language=? AND level=? AND is_active=1 ORDER BY lesson_number",
                (lang_code, level)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def _get_completed_lesson_ids(self, user_id: int, lang_code: str, level: str) -> set:
        async with db.get_connection() as conn:
            cursor = await conn.execute(
                "SELECT lesson_id FROM progress WHERE user_id=? AND language=? AND level=? AND completed=1",
                (user_id, lang_code, level)
            )
            rows = await cursor.fetchall()
            return {row[0] for row in rows}

    async def complete_lesson(self, user_id: int, lesson_id: int, lang_code: str, level: str,
                              score: int = 100, time_spent: int = 0):
        """Mark lesson as completed and update user progress."""
        async with db.get_connection() as conn:
            await conn.execute("""
                INSERT INTO progress (user_id, language, level, lesson_id, score, completed, completed_date, time_spent_seconds)
                VALUES (?, ?, ?, ?, ?, 1, datetime('now'), ?)
                ON CONFLICT(user_id, language, level, lesson_id) DO UPDATE SET
                    completed=1, completed_date=datetime('now'), score=MAX(score, ?), time_spent_seconds=time_spent_seconds+?
            """, (user_id, lang_code, level, lesson_id, score, time_spent, score, time_spent))
            await conn.commit()
        # Update user XP, coins, daily counter (handled in handler via _finish_lesson)
