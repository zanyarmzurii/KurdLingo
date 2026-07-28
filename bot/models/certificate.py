from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Certificate(BaseModel):
    id: Optional[int] = None
    user_id: int
    language: str
    level: str
    score: int
    certificate_code: str
    issued_date: Optional[datetime] = None
    certificate_file_id: Optional[str] = None
    is_valid: bool = True
    revoked_date: Optional[datetime] = None
    revoked_reason: Optional[str] = None
