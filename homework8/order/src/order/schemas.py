from typing import List

from src.models import (
    FromCamelCase, ToCamelCase, PydanticBase, ActiveMixin, TimestampMixin
)


class OrderProductsSchema(PydanticBase):
    id: int
    quantity: int
    price: int


class OrderSchema(TimestampMixin):
    id: int
    status: str
    data: dict
    created_by: int


class CreateOrderSchema(FromCamelCase):
    products: List[OrderProductsSchema]
    address: str
    cart_number: str


class OrderOutSchema(OrderSchema, ToCamelCase):
    pass


class OrdersOutSchema(PydanticBase, ToCamelCase):
    orders: List[OrderOutSchema]
    idempotency_key: str


class OrderCancelledMessageSchema(PydanticBase):
    order_id: int


class OrderStatusChangedMessageSchema(PydanticBase):
    order_id: int
    status: str
        