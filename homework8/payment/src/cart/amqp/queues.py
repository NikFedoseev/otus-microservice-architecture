from aio_pika.abc import AbstractRobustChannel
import config

from .consumers import consume_created_order_events, consume_refund_payment_order_events


async def configure_order_queues(channel: AbstractRobustChannel):
    order_created_queue = await channel.get_queue(
        name=config.ORDER_CREATED_QUEUE,
        ensure=False
    )

    await order_created_queue.channel.set_qos(prefetch_count=10)
    await order_created_queue.consume(consume_created_order_events)

    order_refund_queue = await channel.declare_queue(
        name=config.ORDER_REFUND_QUEUE,
        durable=True
    )

    await order_refund_queue.channel.set_qos(prefetch_count=10)
    await order_refund_queue.consume(consume_refund_payment_order_events)

    await channel.declare_queue(
        name=config.ORDER_PAID_QUEUE,
        durable=True
    )


    



