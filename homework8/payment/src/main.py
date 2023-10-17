from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api import api_router
from src.amqp.core import rabbit_connection

@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    yield
    await rabbit_connection.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(api_router)