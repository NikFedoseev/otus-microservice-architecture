import asyncio
from aio_pika.abc import AbstractIncomingMessage
from src.database.core import async_session
from src.courier.schemas import OrderCreatedSchema
from src.courier.use_cases import book_courier
from src.amqp.producer import rabbit_producer
from src import config

async def consume_order_product_reserved_events(message: AbstractIncomingMessage):
    data = OrderCreatedSchema.model_validate_json(message.body)

    async with async_session() as session:
        try:
            courier = await book_courier(
                db_session=session,
                order_id=data.order_id,
                order_created_at=data.created_at
            )
        except Exception as e:
            await rabbit_producer.send_message(
                messages=data.model_dump(mode='json', include=('products', 'order_id')),
                routing_key=config.ORDER_PRODUCTS_BACKWARD_QUEUE # type: ignore
            )
            await message.ack()
            return

        await rabbit_producer.send_message(
            messages={
                'order_id': data.order_id,
                'status': 'DELIVERING',
                'courier_id': courier.id

            },
            routing_key=config.ORDER_STATE_CHANGED_QUEUE # type: ignore
        )

        await message.ack()