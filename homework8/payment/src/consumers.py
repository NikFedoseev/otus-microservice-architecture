from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
import aio_pika

from src import config
from src.cart.amqp.queues import configure_order_queues
from src.amqp.core import rabbit_connection


app = FastAPI()

async def consume(loop):
    conection = await aio_pika.connect_robust(
        host=config.RABBITMQ_HOST, # type: ignore
        port=config.RABBITMQ_PORT, # type: ignore
        login=config.RABBITMQ_USER, # type: ignore
        password=config.RABBITMQ_PASS, # type: ignore
        loop=loop
    )

    channel = await conection.channel()
    await configure_order_queues(channel)

    try:
        await asyncio.Future()
    finally:
        await conection.close()

@app.on_event('startup')
async def main():
    await rabbit_connection.connect()
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(consume(loop))

@app.on_event("shutdown")
async def shutdown():
    await rabbit_connection.disconnect()
