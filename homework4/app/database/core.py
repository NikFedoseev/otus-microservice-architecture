from typing import AsyncGenerator
from pydantic import PostgresDsn
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

import app.config as config


DATABASE_URL = PostgresDsn.build(
    scheme='postgresql+asyncpg',
    user=config.DB_USER,
    password=config.DB_PASS,
    host=config.DB_HOST, # type: ignore
    port=config.DB_PORT,
    path=f'/{config.DB_NAME}'
)

print(DATABASE_URL)

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session: # type: ignore
        yield session