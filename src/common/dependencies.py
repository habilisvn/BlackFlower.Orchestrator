from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import get_settings

settings = get_settings()
engine = create_async_engine(settings.postgresql_url, echo=False)


async def get_session():
    async with async_sessionmaker[AsyncSession](engine, expire_on_commit=False)() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]
