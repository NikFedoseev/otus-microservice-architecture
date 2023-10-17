from aio_pika.abc import AbstractRobustChannel
import config

from .consumers import consume_order_product_reserved_events


async def configure_order_queues(channel: AbstractRobustChannel):
    order_reserved_queue = await channel.get_queue(
        name=config.ORDER_PRODUCTS_RESERVED_QUEUE,
        ensure=False
    )

    await order_reserved_queue.channel.set_qos(prefetch_count=10)
    await order_reserved_queue.consume(consume_order_product_reserved_events)