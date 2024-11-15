# from common.alchemy import Base
# from common.dependencies import engine


async def create_db_and_tables():
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

    # DOCUMENT: migrations are managed by alembic right now
    #     await conn.run_sync(Base.metadata.create_all)
    pass
