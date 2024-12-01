from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from sqlalchemy import create_engine

from config.settings import Settings, get_settings as get_settings_config


settings = get_settings_config()


def get_pg_sync_engine(db_name: str | None = None):
    connection_string = (
        f"{settings.postgresql_prefix_sync}://"
        f"{settings.postgresql_username}:"
        f"{settings.postgresql_password}@"
        f"{settings.postgresql_host}:"
        f"{settings.postgresql_port}/"
        f"{db_name if db_name else settings.postgresql_db_name}"
    )
    print(connection_string)
    return create_engine(connection_string, echo=False)


# Postgres setup
@lru_cache
def get_pg_async_engine(db_name: str | None = None):
    connection_string = (
        f"{settings.postgresql_prefix_async}://"
        f"{settings.postgresql_username}:"
        f"{settings.postgresql_password}@"
        f"{settings.postgresql_host}:"
        f"{settings.postgresql_port}/"
        f"{db_name if db_name else settings.postgresql_db_name}"
    )
    return create_async_engine(connection_string, echo=False)


async def get_postgres_session(db_name: str | None = None):
    pg_engine = get_pg_async_engine(db_name)
    session_maker = async_sessionmaker[AsyncSession](
        pg_engine, expire_on_commit=False
    )
    async with session_maker() as session:
        yield session


PostgresDpd = Annotated[AsyncSession, Depends(get_postgres_session)]


async def get_mongodb() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    # MongoDB setup
    mongo_client = AsyncIOMotorClient(settings.mongo_url)

    async with await mongo_client.start_session(
        {
            "retryWrites": True,
            "causalConsistency": True,
        }
    ) as session:
        db = session.client[settings.mongo_db_name]
        yield db


MongoDBDpd = Annotated[AsyncIOMotorDatabase, Depends(get_mongodb)]


async def get_mongo_db_name() -> str:
    return settings.mongo_db_name


MongoDBNameDpd = Annotated[str, Depends(get_mongo_db_name)]


# Settings dependency
async def get_settings():
    return get_settings_config()


SettingsDpd = Annotated[Settings, Depends(get_settings)]
