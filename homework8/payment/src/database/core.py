from typing import AsyncGenerator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.engine.url import URL

import src.config as config


DATABASE_URL = URL.create(
    drivername='postgresql+asyncpg',
    username=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST,
    port=config.DB_PORT, # type: ignore
    database=config.DB_NAME
)

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session