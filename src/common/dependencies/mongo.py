from collections.abc import AsyncGenerator
from fastapi import Depends
from typing import Annotated
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from config.settings import get_settings


settings = get_settings()


async def get_mongodb(
    db_url: str = (
        f"{settings.mongo_prefix}://"
        f"{settings.mongo_username}:{settings.mongo_password}"
        f"@{settings.mongo_host}:{settings.mongo_port}"
    ),
) -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    # MongoDB setup
    mongo_client = AsyncIOMotorClient(db_url)

    async with await mongo_client.start_session(
        {
            "retryWrites": True,
            "causalConsistency": True,
        }
    ) as session:
        db = session.client[settings.mongo_db_name]
        yield db


MongoDpd = Annotated[AsyncIOMotorDatabase, Depends(get_mongodb)]
