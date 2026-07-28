"""
Certificate Service: Issues and manages certificates for completed levels.
"""
import uuid
from datetime import datetime
from bot.database import db
from bot.config import logger

class CertificateService:
    async def issue_certificate(self, user_id: int, lang_code: str, level: str, score: int) -> str:
        """
        Create a new certificate for a user.
        Returns the certificate code.
        """
        cert_code = self._generate_code()
        async with db.get_connection() as conn:
            await conn.execute("""
                INSERT INTO certificates (user_id, language, level, score, certificate_code, issued_date, is_valid)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (user_id, lang_code, level, score, cert_code, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            await conn.commit()
        return cert_code

    def _generate_code(self) -> str:
        return f"KURD-{uuid.uuid4().hex[:8].upper()}"

    async def get_user_certificates(self, user_id: int) -> list:
        async with db.get_connection() as conn:
            cursor = await conn.execute(
                "SELECT * FROM certificates WHERE user_id=? AND is_valid=1 ORDER BY issued_date DESC",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    async def revoke_certificate(self, cert_id: int, reason: str = "") -> bool:
        async with db.get_connection() as conn:
            await conn.execute(
                "UPDATE certificates SET is_valid=0, revoked_date=?, revoked_reason=? WHERE id=?",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), reason, cert_id)
            )
            await conn.commit()
            return True
