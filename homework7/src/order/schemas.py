from typing import List

from src.models import (
    FromCamelCase, ToCamelCase, PydanticBase, ActiveMixin, TimestampMixin
)


class OrderProductsSchema(PydanticBase):
    id: int
    qty: int


class OrderSchema(ActiveMixin, TimestampMixin):
    id: int
    status: str
    data: dict


class CreateOrderSchema(FromCamelCase):
    products: List[OrderProductsSchema]


class OrderOutSchema(OrderSchema, ToCamelCase):
    pass


class OrdersOutSchema(PydanticBase, ToCamelCase):
    orders: List[OrderOutSchema]
    idempotency_key: str
        