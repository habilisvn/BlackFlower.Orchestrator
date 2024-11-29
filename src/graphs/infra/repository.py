from common.repository import AbstractRepository
from graphs.domain import Label, NodeEntity, RelationshipEntity
from common.dependencies import MongoDBDpd


class NodeRepository(AbstractRepository[NodeEntity]):
    collection_name = "nodes"

    def __init__(self, db: MongoDBDpd):
        self.collection = db[self.collection_name]

    async def save(self, entity: NodeEntity, upsert: bool = False) -> None:
        entity_dict = entity.model_dump()
        await self.collection.insert_one(
            {"label": entity_dict["label"]},
            {"$set": entity_dict}
        )

    async def find_by_primary_key(self, label: str) -> NodeEntity | None:
        node = await self.collection.find_one({"label": label})
        if not node:
            return None
        return NodeEntity.model_validate(node)

    async def find_all(self, limit: int, offset: int) -> list[NodeEntity]:
        cursor = self.collection.find().skip(offset).limit(limit)
        nodes = await cursor.to_list(length=None)
        return [NodeEntity.model_validate(node) for node in nodes]

    async def delete(self, label: Label) -> None:
        await self.collection.delete_one({"label": label})


class RelationshipRepository(AbstractRepository[RelationshipEntity]):
    collection_name = "relationships"

    def __init__(self, db: MongoDBDpd):
        self.collection = db[self.collection_name]

    async def save(self, entity: RelationshipEntity, upsert: bool = False) -> None:
        entity_dict = entity.model_dump()
        await self.collection.insert_one(entity_dict)

    async def find_by_primary_key(self, from_node: str, to_node: str) -> RelationshipEntity | None:
        relationship = await self.collection.find_one({
            "from_node": from_node,
            "to_node": to_node
        })
        if not relationship:
            return None
        return RelationshipEntity.model_validate(relationship)

    async def find_all(self, limit: int, offset: int) -> list[RelationshipEntity]:
        cursor = self.collection.find().skip(offset).limit(limit)
        relationships = await cursor.to_list(length=None)
        return [RelationshipEntity.model_validate(rel) for rel in relationships]

    async def delete(self, from_node: str, to_node: str) -> None:
        await self.collection.delete_one({
            "from_node": from_node,
            "to_node": to_node
        })

    async def find_by_node_label(self, node_label: str) -> list[RelationshipEntity]:
        cursor = self.collection.find({
            "$or": [
                {"from_node": node_label},
                {"to_node": node_label}
            ]
        })
        relationships = await cursor.to_list(length=None)
        return [RelationshipEntity.model_validate(rel) for rel in relationships]

    async def find_relationship(self, from_node: str, to_node: str) -> RelationshipEntity | None:
        relationship = await self.collection.find_one({
            "from_node": from_node,
            "to_node": to_node
        })
        if not relationship:
            return None
        return RelationshipEntity.model_validate(relationship)
