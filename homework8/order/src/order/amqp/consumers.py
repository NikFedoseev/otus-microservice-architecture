from aio_pika.abc import AbstractIncomingMessage
from src.order.schemas import OrderCancelledMessageSchema, OrderStatusChangedMessageSchema
from src.database.core import async_session
from src.order.use_cases import cancel_order, change_order_status_by_id
from src.order.exceptions import OrderNotFound

async def consume_order_cancelled_events(message: AbstractIncomingMessage):
    data = OrderCancelledMessageSchema.model_validate_json(message.body)

    async with async_session() as session:
        try:
            await cancel_order(
                db_session=session,
                order_id=data.order_id
            )
        except OrderNotFound:
            pass
    
    await message.ack()


async def consume_order_state_changed_events(message: AbstractIncomingMessage):
    data = OrderStatusChangedMessageSchema.model_validate_json(message.body)

    async with async_session() as session:
        try:
            await change_order_status_by_id(
                db_session=session,
                order_id=data.order_id,
                status=data.status
            )
        except OrderNotFound:
            pass

    await message.ack()