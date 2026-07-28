from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class UserSettings(BaseModel):
    notifications: bool = True
    sound: bool = True
    theme: str = "default"

class User(BaseModel):
    user_id: int
    username: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    phone: Optional[str] = None
    join_date: Optional[datetime] = None
    native_language: str = "badini"
    learning_language: Optional[str] = None
    current_level: str = "beginner"
    plan_type: str = "free"
    plan_start_date: Optional[datetime] = None
    plan_expiry: Optional[datetime] = None
    trial_used: bool = False
    trial_start_date: Optional[datetime] = None
    trial_end_date: Optional[datetime] = None
    daily_lessons_completed: int = 0
    daily_lessons_date: Optional[str] = None
    total_lessons_completed: int = 0
    total_xp: int = 0
    total_coins: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_active_date: Optional[str] = None
    referral_code: Optional[str] = None
    referred_by: Optional[int] = None
    referral_count: int = 0
    referral_coins_earned: int = 0
    is_active: bool = True
    is_banned: bool = False
    settings: UserSettings = Field(default_factory=UserSettings)
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True
