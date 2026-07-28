"""
User Service: Manages user-related business logic like plan limits, streaks, XP.
"""
from datetime import date, datetime, timedelta
from bot.database import db
from bot.config import PLANS, logger

class UserService:
    async def can_take_lesson(self, user_id: int) -> bool:
        """Check if user is under daily lesson limit."""
        user = await db.get_user(user_id)
        if not user:
            return False
        plan_type = user.get('plan_type', 'free')
        daily_limit = PLANS[plan_type]['daily_lessons']
        if daily_limit == "unlimited":
            return True
        today = str(date.today())
        # Reset counter if date changed
        if user.get('daily_lessons_date') != today:
            await db.update_user(user_id, daily_lessons_completed=0, daily_lessons_date=today)
            return True
        completed = user.get('daily_lessons_completed', 0)
        return completed < daily_limit

    async def update_daily_lesson_count(self, user_id: int) -> None:
        today = str(date.today())
        user = await db.get_user(user_id)
        if not user:
            return
        if user.get('daily_lessons_date') != today:
            await db.update_user(user_id, daily_lessons_completed=1, daily_lessons_date=today)
        else:
            await db.update_user(user_id,
                                 daily_lessons_completed=user['daily_lessons_completed'] + 1)

    async def add_xp(self, user_id: int, xp: int) -> None:
        user = await db.get_user(user_id)
        if user:
            await db.update_user(user_id, total_xp=user['total_xp'] + xp)

    async def add_coins(self, user_id: int, coins: int) -> None:
        user = await db.get_user(user_id)
        if user:
            await db.update_user(user_id, total_coins=user['total_coins'] + coins)

    async def update_streak(self, user_id: int) -> int:
        """Update login streak and return current streak."""
        user = await db.get_user(user_id)
        if not user:
            return 0
        today = date.today()
        last_active = user.get('last_active_date')
        if last_active:
            last_date = datetime.strptime(last_active, "%Y-%m-%d").date()
            if last_date == today:
                return user.get('current_streak', 0)
            elif last_date == today - timedelta(days=1):
                new_streak = user.get('current_streak', 0) + 1
                longest = max(new_streak, user.get('longest_streak', 0))
                await db.update_user(user_id, current_streak=new_streak, longest_streak=longest,
                                     last_active_date=str(today))
                return new_streak
            else:
                await db.update_user(user_id, current_streak=1, last_active_date=str(today))
                return 1
        else:
            await db.update_user(user_id, current_streak=1, last_active_date=str(today))
            return 1

    async def is_premium(self, user_id: int) -> bool:
        user = await db.get_user(user_id)
        if not user:
            return False
        if user.get('plan_type', 'free') in ['premium', 'family']:
            # Also check expiry
            plan_expiry = user.get('plan_expiry')
            if plan_expiry:
                expiry_date = datetime.strptime(plan_expiry, "%Y-%m-%d %H:%M:%S")
                if expiry_date >= datetime.now():
                    return True
                else:
                    # Expired, revert to free
                    await db.update_user(user_id, plan_type='free', plan_expiry=None)
                    return False
            return True
        return False
