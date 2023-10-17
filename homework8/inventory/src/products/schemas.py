from typing import List
from datetime import datetime
from src.models import FromCamelCase, ToCamelCase, PydanticBase, ActiveMixin, TimestampMixin


class AddProductsShema(PydanticBase, FromCamelCase):
    name: str
    quantity: int


class ProductSchema(TimestampMixin):
    id: int
    name: str
    quantity: int


class ProductOut(ToCamelCase, ProductSchema):
    ...


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


class OrderBackwardSchema(PydanticBase):
    order_id: int
    products: List[OrderProductsSchema]