from uuid import UUID
from sqlmodel import select

from common.repository import AbstractRepository
from user.domain.entities import UserEntity
from user.infra.orm import UserTable
from common.dependencies import SessionDependency


class UserRepository(AbstractRepository[UserEntity]):
    def __init__(self, session: SessionDependency):
        self.session = session

    async def save(self, entity: UserEntity) -> UserEntity:
        user_db = UserTable(**entity.model_dump())

        # DOCUMENT: This syntax for nested session
        async with self.session.begin():
            self.session.add(user_db)

        await self.session.refresh(user_db)

        return user_db  # type: ignore

    async def find_by_id(self, entity_id: UUID) -> UserEntity | None:
        query = select(UserTable).where(UserTable.id == entity_id)

        async with self.session.begin():
            result = await self.session.execute(query)

        user = result.scalars().first()

        return user  # type: ignore

    async def find_by_username(self, username: str) -> UserEntity | None:
        query = select(UserTable).where(UserTable.username == username)

        async with self.session.begin():
            result = await self.session.execute(query)

        user = result.scalars().first()

        return user  # type: ignore

    async def find_by_email(self, email: str) -> UserEntity | None:
        query = select(UserTable).where(UserTable.email == email)

        async with self.session.begin():
            result = await self.session.execute(query)

        user = result.scalars().first()

        return user  # type: ignore

    # not tested
    async def delete(self, entity_id: UUID) -> None:
        query = select(UserTable).where(UserTable.id == entity_id)

        async with self.session.begin():
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                await self.session.delete(user)
