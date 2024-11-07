from typing import Annotated

from fastapi import Depends
from sqlmodel import Session
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)
from sqlalchemy.ext.declarative import declarative_base

from config.settings import get_settings


# Database setup
connect_args = {}
settings = get_settings()
engine = create_async_engine(
    settings.postgresql_url, connect_args=connect_args, echo=False
)
# engine = create_async_engine(settings.postgresql_url, connect_args=connect_args)
# CHECK autoflush again
session_maker = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


async def get_session():
    async with engine.begin() as conn:
        yield conn


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)


SessionDependency = Annotated[Session, Depends(get_session)]
