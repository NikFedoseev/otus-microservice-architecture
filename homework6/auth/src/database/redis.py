from typing import AsyncGenerator
from pydantic import RedisDsn

from redis.asyncio import from_url, Redis

from src.config import REDIS_HOST, REDIS_PORT

async def get_redis_pool() -> AsyncGenerator[Redis, None]:
    redis_url = RedisDsn.build(
        scheme='redis',
        host=REDIS_HOST, # type: ignore
        port=int(REDIS_PORT) # type: ignore
    )
    session = from_url(str(redis_url), encoding="utf-8", decode_responses=True)
    yield session
    await session.close()