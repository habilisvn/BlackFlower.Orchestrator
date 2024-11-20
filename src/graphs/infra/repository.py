from pydantic import UUID4
from sqlmodel import select

from common.repository import AbstractRepository
from graphs.domain.entities import NodeEntity
from graphs.infra.orm import Node
from common.dependencies import SessionDependency


class NodeRepository(AbstractRepository[NodeEntity]):
    def __init__(self, session: SessionDependency):
        self.session = session

    # DOCUMENT: Nested class as a return type
    # The nested class is defined at the base class
    async def save(
        self, entity: NodeEntity
    ) -> NodeEntity:
        entity_dict = entity.model_dump()
        node_db = Node(**entity_dict)

        # DOCUMENT: This syntax for nested session
        async with self.session.begin():
            self.session.add(node_db)

        await self.session.refresh(node_db)

        # DOCUMENT: Must use jsonable_encoder to prevent async exception
        return NodeEntity.model_validate(node_db)

    async def find_by_id(self, entity_id: UUID4) -> NodeEntity | None:
        query = select(Node).where(Node.id == entity_id)

        async with self.session.begin():
            result = await self.session.execute(query)

        node = result.scalars().first()

        return node  # type: ignore

    async def find_by_label(self, label: str) -> NodeEntity | None:
        query = select(Node).where(Node.label == label)

        async with self.session.begin():
            result = await self.session.execute(query)

        node = result.scalars().first()

        return node  # type: ignore

    async def find_all(self, limit: int, offset: int) -> list[NodeEntity]:
        query = select(Node).offset(offset).limit(limit)

        async with self.session.begin():
            result = await self.session.execute(query)

        return result.scalars().all()  # type: ignore

    # not tested
    async def delete(self, entity_id: UUID4) -> None:
        query = select(Node).where(Node.id == entity_id)

        async with self.session.begin():
            result = await self.session.execute(query)
            node = result.scalars().first()
            if node:
                await self.session.delete(node)
