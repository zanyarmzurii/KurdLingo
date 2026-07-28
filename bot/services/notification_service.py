"""
Notification Service: Sends admin notifications for important events.
"""
from bot.database import db
from bot.config import ADMIN_ID, logger

class NotificationService:
    async def notify_admin(self, notif_type: str, message: str, user_id: int = None, priority: str = 'normal'):
        await db.add_notification(
            admin_id=ADMIN_ID,
            notif_type=notif_type,
            message=message,
            user_id=user_id,
            priority=priority
        )

    async def notify_new_payment(self, user_id: int, amount: int, plan: str):
        msg = f"پارەدانی نوێ - بەکارهێنەر {user_id} بڕی {amount} د.ع بۆ پلانی {plan}"
        await self.notify_admin('payment', msg, user_id, 'high')

    async def notify_certificate_request(self, user_id: int, score: float):
        msg = f"داواکاری بڕوانامە - بەکارهێنەر {user_id} نمرە {score:.1f}%"
        await self.notify_admin('certificate', msg, user_id, 'normal')
