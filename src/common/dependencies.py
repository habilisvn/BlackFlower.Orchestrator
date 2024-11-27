from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config.settings import Settings, get_settings as get_settings_config


settings = get_settings_config()

# Postgres setup
pg_engine = create_async_engine(settings.postgresql_url_sync, echo=False)


async def get_postgres_session():
    session_maker = async_sessionmaker[AsyncSession](pg_engine, expire_on_commit=False)
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
