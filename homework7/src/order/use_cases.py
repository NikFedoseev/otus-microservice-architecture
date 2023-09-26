import sqlalchemy as sa
import hashlib
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from src.order.schemas import OrderSchema, CreateOrderSchema
from src.order.exceptions import OrderConflict
from src.order.models import OrderModel
from src.order.constants import OrderStatus


async def get_orders(db_session: AsyncSession) -> List[OrderSchema]:
    orders = await db_session.scalars(
        sa.select(OrderModel)
    )

    return [OrderSchema.model_validate(order) for order in orders]


async def create_order(
    db_session: AsyncSession, 
    order_in: CreateOrderSchema,
    client_idempotency_key: str
) -> OrderSchema:
    orders = await get_orders(db_session)
    server_idempotency_key = get_idempotency_key(orders)

    if client_idempotency_key != server_idempotency_key:
        raise OrderConflict
    
    data = {
        **order_in.model_dump()
    }
    
    order = OrderModel(
        data=data,
        status=OrderStatus.CREATED.value
    )

    db_session.add(order)
    await db_session.commit()

    return OrderSchema.model_validate(order)


def get_idempotency_key(orders: List[OrderSchema]) -> str:
    serialized_orders = [order.model_dump_json() for order in orders]

    idempotency_key = hashlib.sha256()
    idempotency_key.update(str(serialized_orders).encode('utf-8'))

    return idempotency_key.hexdigest()
