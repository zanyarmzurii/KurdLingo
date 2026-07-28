"""
Scheduler Service: Handles daily tasks like resetting lesson counts, expiring plans.
"""
import asyncio
import logging
from datetime import datetime
from bot.database import db
from bot.config import logger

async def daily_maintenance():
    """Run daily tasks."""
    # Reset daily lesson counters
    today = datetime.now().strftime("%Y-%m-%d")
    async with db.get_connection() as conn:
        await conn.execute(
            "UPDATE users SET daily_lessons_completed=0 WHERE daily_lessons_date != ?",
            (today,)
        )
        await conn.commit()
    logger.info("Daily lesson counters reset.")

    # Expire outdated plans
    expired_users = await db.check_and_expire_plans()
    if expired_users:
        logger.info(f"Expired plans for {len(expired_users)} users.")

async def scheduler_loop():
    """Run maintenance every hour, but daily tasks once a day."""
    last_run_date = None
    while True:
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")
        if today_str != last_run_date:
            await daily_maintenance()
            last_run_date = today_str
        # Could also run other periodic tasks
        await asyncio.sleep(3600)  # 1 hour

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(scheduler_loop())
