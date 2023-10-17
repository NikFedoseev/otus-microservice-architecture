from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio

from src import config
from src.products.amqp.queues import configure_order_queues
from src.amqp.consumer import RabbitConsumer
from src.amqp.producer import rabbit_producer


app = FastAPI()

async def consume(loop: asyncio.AbstractEventLoop):
    rabbit_consumer = RabbitConsumer(
        host=config.RABBITMQ_HOST, # type: ignore
        port=config.RABBITMQ_PORT, # type: ignore
        login=config.RABBITMQ_USER, # type: ignore
        password=config.RABBITMQ_PASS, # type: ignore
        loop=loop
    )

    await rabbit_consumer.start()
    await rabbit_producer.start()
    
    await configure_order_queues(rabbit_consumer.channel)


@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(consume(loop))
