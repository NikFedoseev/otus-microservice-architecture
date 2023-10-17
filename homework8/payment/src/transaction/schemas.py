from typing import Optional
from datetime import datetime

from src.models import PydanticBase

class TransactionSchema(PydanticBase):
    id: int
    cart_id: int
    order_id: Optional[int]
    operation: str
    amount: float
    created_at: datetime
    created_by: int