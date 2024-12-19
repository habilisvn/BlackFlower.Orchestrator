from functools import lru_cache
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from config.settings import get_settings


settings = get_settings()


def get_pg_sync_engine(db_name: str | None = None):
    connection_string = (
        f"{settings.postgresql_prefix_sync}://"
        f"{settings.postgresql_username}:"
        f"{settings.postgresql_password}@"
        f"{settings.postgresql_host}:"
        f"{settings.postgresql_port}/"
        f"{db_name if db_name else settings.postgresql_db_name}"
    )
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
