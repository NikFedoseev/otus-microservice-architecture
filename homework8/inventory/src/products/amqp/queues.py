from aio_pika.abc import AbstractRobustChannel
import config

from .consumers import consume_paid_order_events, consume_backward_products_events


async def configure_order_queues(channel: AbstractRobustChannel):
    order_paid_queue = await channel.get_queue(
        name=config.ORDER_PAID_QUEUE,
        ensure=False
    )

    await order_paid_queue.channel.set_qos(prefetch_count=10)
    await order_paid_queue.consume(consume_paid_order_events)
    # await order_paid_queue.consume(consume_paid_order_events)

    order_products_backward_queue = await channel.declare_queue(
        name=config.ORDER_PRODUCTS_BACKWARD_QUEUE,
        durable=True
    )

    await order_products_backward_queue.channel.set_qos(prefetch_count=10)
    await order_products_backward_queue.consume(consume_backward_products_events)

    await channel.declare_queue(
        name=config.ORDER_PRODUCTS_RESERVED_QUEUE,
        durable=True
    )
