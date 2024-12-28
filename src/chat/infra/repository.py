from common.dependencies.mongo import MongoDpd
from common.repository import AbstractRepository
from chat.domain.entities import ExternalUser


class ExternalUserRepository(AbstractRepository[ExternalUser]):
    collection_name = "external_users"

    def __init__(self, db: MongoDpd):
        self.collection = db[self.collection_name]

    async def find_by_id(self, id: str) -> ExternalUser | None:
        result = await self.collection.find_one({"id": id})
        return ExternalUser(**result) if result else None
