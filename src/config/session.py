from sqlalchemy.ext.asyncio import create_async_engine

from common.db import Base
from common.db import engine
        

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
