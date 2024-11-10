from common.alchemy import Base
from common.dependencies import engine
        

async def create_db_and_tables():
    async with engine.begin() as conn:
        ### DOCUMENT: don't drop tables if not necessary
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
