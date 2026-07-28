from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuizQuestion(BaseModel):
    id: int
    language: str
    level: str
    question_type: str = "multiple_choice"
    question_text: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None
    difficulty: int = 1
    points: int = 10
    is_active: bool = True

class QuizResult(BaseModel):
    id: Optional[int] = None
    user_id: int
    language: str
    level: str
    quiz_type: str = "standard"
    total_questions: int
    correct_answers: int
    score_percentage: float
    xp_earned: int
    coins_earned: int
    passed: bool
    perfect_score: bool = False
    time_taken_seconds: int = 0
    quiz_date: Optional[datetime] = None
    answers_detail: str = "[]"
