from aio_pika.abc import AbstractRobustChannel
import config

from .consumers import consume_order_cancelled_events, consume_order_state_changed_events


async def configure_order_queues(channel: AbstractRobustChannel):
    await channel.declare_queue(
        name=config.ORDER_CREATED_QUEUE,
        durable=True
    )

    order_cancelled_queue = await channel.declare_queue(
        name=config.ORDER_CANCELLED_QUEUE,
        durable=True
    )
    await order_cancelled_queue.channel.set_qos(prefetch_count=10)
    await order_cancelled_queue.consume(consume_order_cancelled_events)

    order_state_changed_queue = await channel.declare_queue(
        name=config.ORDER_STATE_CHANGED_QUEUE,
        durable=True
    )
    await order_state_changed_queue.consume(consume_order_state_changed_events)

    



