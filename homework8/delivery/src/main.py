from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api import api_router
from src.amqp.producer import rabbit_producer

@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_producer.start()
    yield
    await rabbit_producer.stop()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)