import asyncio
from aio_pika.abc import AbstractIncomingMessage
from src.database.core import async_session
from src.products.schemas import OrderCreatedSchema, OrderBackwardSchema
from src.products.use_cases import reserve_products, backward_reserved_products
from src.products.exceptions import NotEnoughProducts
from src.amqp.producer import rabbit_producer
from src import config

async def consume_paid_order_events(message: AbstractIncomingMessage):
    data = OrderCreatedSchema.model_validate_json(message.body)

    async with async_session() as session:
        try:
            await reserve_products(
                db_session=session,
                order_products_in=data.products
            )
        except Exception as e:
            await rabbit_producer.send_message(
                messages={
                    'order_id': data.order_id
                },
                routing_key=config.ORDER_REFUND_QUEUE # type: ignore
            )
            await message.ack()
            return

        await rabbit_producer.send_message(
            messages=data.model_dump(mode='json'),
            routing_key=config.ORDER_PRODUCTS_RESERVED_QUEUE # type: ignore
        )

        await message.ack()


async def consume_backward_products_events(message: AbstractIncomingMessage):
    data = OrderBackwardSchema.model_validate_json(message.body)

    async with async_session() as session:
        await backward_reserved_products(
            db_session=session,
            order_products_in=data.products
        )
        await rabbit_producer.send_message(
            messages={
                "order_id": data.order_id
            },
            routing_key=config.ORDER_REFUND_QUEUE # type: ignore
        )
        await message.ack()
    