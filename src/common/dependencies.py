from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import Settings, get_settings as get_settings_config

settings = get_settings_config()
engine = create_async_engine(settings.postgresql_url, echo=False)


async def get_session():
    session_maker = async_sessionmaker[AsyncSession](
        engine, expire_on_commit=False
    )
    async with session_maker() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]


async def get_settings():
    return get_settings_config()

SettingsDependency = Annotated[Settings, Depends(get_settings)]
