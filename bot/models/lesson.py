from pydantic import BaseModel
from typing import List, Optional

class VocabularyItem(BaseModel):
    kurdish: str
    translation: str
    example: Optional[str] = None

class Lesson(BaseModel):
    id: int
    language: str
    level: str
    lesson_number: int
    lesson_type: str
    title: str
    content: Optional[str] = None
    vocabulary: List[VocabularyItem] = []
    examples: List[str] = []
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    is_active: bool = True
