from typing import List
from datetime import datetime
from src.models import ToCamelCase, PydanticBase, TimestampMixin, FromCamelCase


class CourierSchema(TimestampMixin):
    id: int
    

class CourierOut(ToCamelCase, CourierSchema):
    ...


class BookedCourierSlotSchema(PydanticBase):
    courier_id: int
    order_id: int
    date_from: datetime
    date_to: datetime


class BookedCourierSlotOutSchema(ToCamelCase, BookedCourierSlotSchema):
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


class TestBook(FromCamelCase):
    order_id: int 
    order_created_at: datetime