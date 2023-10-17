from typing import List
from datetime import datetime
from src.models import FromCamelCase, ToCamelCase, PydanticBase, ActiveMixin, TimestampMixin


class AddUserCartSchema(PydanticBase, FromCamelCase):
    cart_number: str
    user_id: int


class ReplenishCartSchema(PydanticBase, FromCamelCase):
    amount: float


class UserCartOut(ToCamelCase, TimestampMixin):
    id: int
    cart_number: str
    user_id: int
    money_amount: float


class OrderProductsSchema(PydanticBase):
    id: int
    quantity: int
    

class OrderCreatedSchema(PydanticBase):
    order_id: int
    total_price: float
    address: str
    customer_id: int
    created_at: datetime
    cart_number: str
    products: List[OrderProductsSchema]


class OrderRefundSchema(PydanticBase):
    order_id: int