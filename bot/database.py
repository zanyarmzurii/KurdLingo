"""
KurdLingo Bot Database Module
Enterprise-grade database management with SQLite and async support
"""

import os
import json
import sqlite3
import asyncio
import aiosqlite
import random
import string
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
from contextlib import asynccontextmanager

from bot.config import (
    DATABASE_URL, DATA_DIR, logger,
    DEFAULT_LANGUAGE, PLANS, REFERRAL_SETTINGS
)

class Database:
    """Async database manager for KurdLingo bot"""
    
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(DATA_DIR / "kurdingo.db")
        self.db_path = db_path
        self._lock = asyncio.Lock()
        
    @asynccontextmanager
    async def get_connection(self):
        """Get async database connection with context management"""
        async with self._lock:
            db = await aiosqlite.connect(self.db_path)
            db.row_factory = aiosqlite.Row
            try:
                await db.execute("PRAGMA journal_mode=WAL")
                await db.execute("PRAGMA foreign_keys=ON")
                yield db
            finally:
                await db.close()
    
    async def init_db(self) -> None:
        """Initialize database with all required tables"""
        logger.info("Initializing database...")
        
        async with self.get_connection() as db:
            await db.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    phone TEXT,
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    native_language TEXT DEFAULT 'badini',
                    learning_language TEXT,
                    current_level TEXT DEFAULT 'beginner',
                    plan_type TEXT DEFAULT 'free',
                    plan_start_date TIMESTAMP,
                    plan_expiry TIMESTAMP,
                    trial_used BOOLEAN DEFAULT FALSE,
                    trial_start_date TIMESTAMP,
                    trial_end_date TIMESTAMP,
                    daily_lessons_completed INTEGER DEFAULT 0,
                    daily_lessons_date DATE,
                    total_lessons_completed INTEGER DEFAULT 0,
                    total_xp INTEGER DEFAULT 0,
                    total_coins INTEGER DEFAULT 0,
                    current_streak INTEGER DEFAULT 0,
                    longest_streak INTEGER DEFAULT 0,
                    last_active_date DATE,
                    referral_code TEXT UNIQUE,
                    referred_by INTEGER,
                    referral_count INTEGER DEFAULT 0,
                    referral_coins_earned INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_banned BOOLEAN DEFAULT FALSE,
                    settings TEXT DEFAULT '{}',
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (referred_by) REFERENCES users (user_id)
                );
                
                CREATE TABLE IF NOT EXISTS progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    level TEXT NOT NULL,
                    lesson_id INTEGER NOT NULL,
                    lesson_type TEXT DEFAULT 'vocabulary',
                    score INTEGER DEFAULT 0,
                    max_score INTEGER DEFAULT 100,
                    attempts INTEGER DEFAULT 1,
                    completed BOOLEAN DEFAULT FALSE,
                    completed_date TIMESTAMP,
                    time_spent_seconds INTEGER DEFAULT 0,
                    mistakes TEXT DEFAULT '[]',
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    level TEXT NOT NULL,
                    quiz_type TEXT DEFAULT 'standard',
                    total_questions INTEGER DEFAULT 20,
                    correct_answers INTEGER DEFAULT 0,
                    score_percentage REAL DEFAULT 0,
                    xp_earned INTEGER DEFAULT 0,
                    coins_earned INTEGER DEFAULT 0,
                    passed BOOLEAN DEFAULT FALSE,
                    perfect_score BOOLEAN DEFAULT FALSE,
                    time_taken_seconds INTEGER DEFAULT 0,
                    quiz_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    answers_detail TEXT DEFAULT '[]',
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    plan_type TEXT NOT NULL,
                    duration TEXT NOT NULL,
                    amount INTEGER NOT NULL,
                    currency TEXT DEFAULT 'IQD',
                    payment_method TEXT NOT NULL,
                    transaction_id TEXT,
                    receipt_message_id TEXT,
                    receipt_file_id TEXT,
                    status TEXT DEFAULT 'pending',
                    admin_verified BOOLEAN DEFAULT FALSE,
                    verified_by INTEGER,
                    verified_date TIMESTAMP,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expiry_date TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (verified_by) REFERENCES users (user_id)
                );
                
                CREATE TABLE IF NOT EXISTS certificates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    level TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    certificate_code TEXT UNIQUE NOT NULL,
                    issued_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    certificate_file_id TEXT,
                    is_valid BOOLEAN DEFAULT TRUE,
                    revoked_date TIMESTAMP,
                    revoked_reason TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS referrals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    referrer_id INTEGER NOT NULL,
                    referred_id INTEGER NOT NULL,
                    referral_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    reward_claimed BOOLEAN DEFAULT FALSE,
                    reward_type TEXT,
                    reward_amount INTEGER DEFAULT 0,
                    FOREIGN KEY (referrer_id) REFERENCES users (user_id) ON DELETE CASCADE,
                    FOREIGN KEY (referred_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    title TEXT,
                    message TEXT NOT NULL,
                    user_id INTEGER,
                    is_read BOOLEAN DEFAULT FALSE,
                    priority TEXT DEFAULT 'normal',
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    read_date TIMESTAMP,
                    action_taken TEXT,
                    FOREIGN KEY (admin_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
                
                CREATE TABLE IF NOT EXISTS daily_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL UNIQUE,
                    total_users INTEGER DEFAULT 0,
                    new_users INTEGER DEFAULT 0,
                    active_users INTEGER DEFAULT 0,
                    lessons_completed INTEGER DEFAULT 0,
                    quizzes_taken INTEGER DEFAULT 0,
                    payments_total INTEGER DEFAULT 0,
                    payments_count INTEGER DEFAULT 0,
                    coins_earned INTEGER DEFAULT 0,
                    coins_spent INTEGER DEFAULT 0,
                    referrals_made INTEGER DEFAULT 0,
                    premium_signups INTEGER DEFAULT 0,
                    family_signups INTEGER DEFAULT 0
                );
                
                CREATE TABLE IF NOT EXISTS lesson_content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT NOT NULL,
                    level TEXT NOT NULL,
                    lesson_number INTEGER NOT NULL,
                    lesson_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    vocabulary TEXT DEFAULT '[]',
                    examples TEXT DEFAULT '[]',
                    audio_url TEXT,
                    image_url TEXT,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                );
                
                CREATE TABLE IF NOT EXISTS quiz_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT NOT NULL,
                    level TEXT NOT NULL,
                    question_type TEXT DEFAULT 'multiple_choice',
                    question_text TEXT NOT NULL,
                    options TEXT NOT NULL,
                    correct_answer INTEGER NOT NULL,
                    explanation TEXT,
                    difficulty INTEGER DEFAULT 1,
                    points INTEGER DEFAULT 10,
                    is_active BOOLEAN DEFAULT TRUE
                );
                
                CREATE INDEX IF NOT EXISTS idx_users_referral ON users(referral_code);
                CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id, language, level);
                CREATE INDEX IF NOT EXISTS idx_quiz_user ON quiz_results(user_id, language);
                CREATE INDEX IF NOT EXISTS idx_payments_user ON payments(user_id, status);
                CREATE INDEX IF NOT EXISTS idx_certificates_user ON certificates(user_id, language);
                CREATE INDEX IF NOT EXISTS idx_notifications_admin ON notifications(admin_id, is_read);
                CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(date);
                CREATE INDEX IF NOT EXISTS idx_lesson_content ON lesson_content(language, level, lesson_number);
                CREATE INDEX IF NOT EXISTS idx_quiz_questions ON quiz_questions(language, level, question_type);
            """)
            await db.commit()
        
        logger.info("Database initialization completed!")
    
    async def add_user(self, user_id: int, username: str, first_name: str, 
                      last_name: Optional[str] = None) -> bool:
        """Add new user to database"""
        try:
            async with self.get_connection() as db:
                referral_code = self._generate_referral_code()
                
                await db.execute("""
                    INSERT OR IGNORE INTO users 
                    (user_id, username, first_name, last_name, referral_code, join_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, username, first_name, last_name, referral_code, 
                     datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                await db.commit()
                
                await self._update_daily_stats(new_user=True)
                return True
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            return False
    
    def _generate_referral_code(self) -> str:
        """Generate unique referral code"""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not self._referral_code_exists(code):
                return code
    
    def _referral_code_exists(self, code: str) -> bool:
        """Check if referral code exists"""
        try:
            with sqlite3.connect(self.db_path) as db:
                cursor = db.execute("SELECT 1 FROM users WHERE referral_code = ?", (code,))
                return cursor.fetchone() is not None
        except Exception:
            return False
    
    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        async with self.get_connection() as db:
            cursor = await db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = await cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    async def update_user(self, user_id: int, **kwargs) -> bool:
        """Update user fields"""
        try:
            if not kwargs:
                return False
            
            kwargs['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values()) + [user_id]
            
            async with self.get_connection() as db:
                await db.execute(
                    f"UPDATE users SET {set_clause} WHERE user_id = ?",
                    values
                )
                await db.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            return False
    
    async def update_user_plan(self, user_id: int, plan_type: str, 
                               duration_days: int) -> bool:
        """Update user plan with expiry"""
        try:
            now = datetime.now()
            expiry = now + timedelta(days=duration_days)
            
            async with self.get_connection() as db:
                await db.execute("""
                    UPDATE users 
                    SET plan_type = ?, plan_start_date = ?, plan_expiry = ?, 
                        trial_used = TRUE, last_updated = ?
                    WHERE user_id = ?
                """, (
                    plan_type,
                    now.strftime("%Y-%m-%d %H:%M:%S"),
                    expiry.strftime("%Y-%m-%d %H:%M:%S"),
                    now.strftime("%Y-%m-%d %H:%M:%S"),
                    user_id
                ))
                await db.commit()
            
            await self._update_daily_stats(premium_signup=(
                plan_type in ['premium', 'family']
            ))
            return True
        except Exception as e:
            logger.error(f"Error updating plan for user {user_id}: {e}")
            return False
    
    async def add_referral(self, referrer_id: int, referred_id: int) -> bool:
        """Add referral record and process rewards"""
        try:
            async with self.get_connection() as db:
                await db.execute("""
                    INSERT INTO referrals (referrer_id, referred_id)
                    VALUES (?, ?)
                """, (referrer_id, referred_id))
                
                await db.execute("""
                    UPDATE users 
                    SET referral_count = referral_count + 1 
                    WHERE user_id = ?
                """, (referrer_id,))
                
                await db.commit()
            
            await self._update_daily_stats(referral=True)
            
            referrer = await self.get_user(referrer_id)
            if referrer:
                bonus_coins = REFERRAL_SETTINGS['coins_per_referral']
                if referrer['referral_count'] >= 25:
                    bonus_coins += REFERRAL_SETTINGS['bonus_referrals_25']
                elif referrer['referral_count'] >= 10:
                    bonus_coins += REFERRAL_SETTINGS['bonus_referrals_10']
                elif referrer['referral_count'] >= 5:
                    bonus_coins += REFERRAL_SETTINGS['bonus_referrals_5']
                
                await self.update_user(
                    referrer_id,
                    total_coins=referrer['total_coins'] + bonus_coins,
                    referral_coins_earned=referrer['referral_coins_earned'] + bonus_coins
                )
            
            return True
        except Exception as e:
            logger.error(f"Error adding referral: {e}")
            return False
    
    async def _update_daily_stats(self, **increments) -> None:
        """Update daily statistics"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            
            async with self.get_connection() as db:
                await db.execute("""
                    INSERT OR IGNORE INTO daily_stats (date) VALUES (?)
                """, (today,))
                
                updates = []
                params = []
                for key, value in increments.items():
                    if value:
                        updates.append(f"{key} = {key} + 1")
                
                if updates:
                    query = f"UPDATE daily_stats SET {', '.join(updates)} WHERE date = ?"
                    params.append(today)
                    await db.execute(query, tuple(params))
                    await db.commit()
        except Exception as e:
            logger.error(f"Error updating daily stats: {e}")

db = Database()
