from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REJECTED = "rejected"

class Payment(BaseModel):
    id: Optional[int] = None
    user_id: int
    plan_type: str
    duration: str
    amount: int
    currency: str = "IQD"
    payment_method: str
    transaction_id: Optional[str] = None
    receipt_message_id: Optional[str] = None
    receipt_file_id: Optional[str] = None
    status: PaymentStatus = PaymentStatus.PENDING
    admin_verified: bool = False
    verified_by: Optional[int] = None
    verified_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    notes: Optional[str] = None
