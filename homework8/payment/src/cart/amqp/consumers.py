from aio_pika.abc import AbstractIncomingMessage
from src.database.core import async_session
from src.cart.schemas import OrderCreatedSchema, OrderRefundSchema
from src.cart.use_cases import pay_order, refund_money_by_cart_transaction
from src.cart.exceptions import NotEnoughMoney
from src.amqp.core import rabbit_connection
from src import config

async def consume_created_order_events(message: AbstractIncomingMessage):
    data = OrderCreatedSchema.model_validate_json(message.body)

    async with async_session() as session:
        try:
            await pay_order(
                db_session=session,
                order_id=data.order_id,
                price=data.total_price,
                user_id=data.customer_id,
                cart_number=data.cart_number
            )
        except NotEnoughMoney:
            await rabbit_connection.send_message(
                messages={
                    "order_id": data.order_id
                },
                routing_key=config.ORDER_CANCELED_QUEUE # type: ignore
            )
            await message.ack()
            return


        await rabbit_connection.send_message(
            messages=data.model_dump(mode='json'),
            routing_key=config.ORDER_PAID_QUEUE # type: ignore
        )

        await message.ack()


async def consume_refund_payment_order_events(message: AbstractIncomingMessage):
    data = OrderRefundSchema.model_validate_json(message.body)

    async with async_session() as session:
        await refund_money_by_cart_transaction(
            db_session=session,
            order_id=data.order_id
        )
        await rabbit_connection.send_message(
            messages={
                "order_id": data.order_id
            },
            routing_key=config.ORDER_CANCELED_QUEUE # type: ignore
        )
        await message.ack()