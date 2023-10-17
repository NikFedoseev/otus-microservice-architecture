import sqlalchemy as sa
import hashlib
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.order.schemas import OrderSchema, CreateOrderSchema
from src.order.exceptions import OrderConflict, OrderNotFound
from src.order.models import OrderModel
from src.order.constants import OrderStatus
from src.amqp.core import RabbitConnection
from src import config


async def get_orders(db_session: AsyncSession) -> List[OrderSchema]:
    orders = await db_session.scalars(
        sa.select(OrderModel)
    )

    return [OrderSchema.model_validate(order) for order in orders]


async def create_order(
    db_session: AsyncSession, 
    order_in: CreateOrderSchema,
    client_idempotency_key: str,
    rabbit_connection: RabbitConnection
) -> OrderSchema:
    # orders = await get_orders(db_session)
    # server_idempotency_key = get_idempotency_key(orders)

    # if client_idempotency_key != server_idempotency_key:
    #     raise OrderConflict
    
    data = {
        **order_in.model_dump()
    }
    
    order = OrderModel(
        data=data,
        status=OrderStatus.CREATED.value,
        created_by=1
    )

    db_session.add(order)
    await db_session.commit()


    total_price = sum([
        product.price * product.quantity 
        for product in order_in.products
    ])

    await rabbit_connection.send_message(
        messages={
            "order_id": order.id,
            "total_price": total_price,
            "address": order.data.get('address'),
            "products": [
                {
                    "id": product["id"],
                    "quantity": product["quantity"],
                }
                for product in order.data.get('products')
            ],
            "customer_id": order.created_by,
            "created_at": order.created_at.isoformat(),
            "cart_number": order.data.get('cart_number')
        },
        routing_key=config.ORDER_CREATED_QUEUE # type: ignore
    )


    return OrderSchema.model_validate(order)


async def change_order_status_by_id(
    db_session: AsyncSession,
    order_id: int,
    status: str
):
    order = await db_session.scalar(
        sa.select(OrderModel).where(OrderModel.id == order_id)
    )
    if not order:
        raise OrderNotFound
    
    order.status = status
    order.updated_at = datetime.utcnow()
    await db_session.commit()


async def cancel_order(
    db_session: AsyncSession,
    order_id: int
):
    await change_order_status_by_id(
        db_session=db_session,
        status=OrderStatus.CANCEL.value,
        order_id=order_id
    )
    


def get_idempotency_key(orders: List[OrderSchema]) -> str:
    serialized_orders = [order.model_dump_json() for order in orders]

    idempotency_key = hashlib.sha256()
    idempotency_key.update(str(serialized_orders).encode('utf-8'))

    return idempotency_key.hexdigest()
