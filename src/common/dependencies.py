from typing import Annotated, Any
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


PostgresDependency = Annotated[AsyncSession, Depends(get_postgres_session)]

# MongoDB setup
mongo_client = AsyncIOMotorClient(settings.mongodb_url)  # type: ignore
mongo_db = mongo_client[settings.mongodb_database]  # type: ignore


async def get_mongodb() -> AsyncIOMotorDatabase[Any]:
    try:
        yield mongo_client
    finally:
        mongo_client.close()


MongoDBDependency = Annotated[AsyncIOMotorDatabase, Depends(get_mongodb)]


# Settings dependency
async def get_settings():
    return get_settings_config()


SettingsDependency = Annotated[Settings, Depends(get_settings)]
