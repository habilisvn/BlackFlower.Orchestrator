from pydantic import UUID4
from sqlmodel import select

from common.repository import AbstractRepository
from user.domain.entities import UserEntity
from user.infra.orm import UserTable
from common.dependencies import SessionDependency


class UserRepository(AbstractRepository[UserEntity]):
    def __init__(self, session: SessionDependency):
        self.session = session

    # DOCUMENT: Nested class as a return type
    # The nested class is defined at the base class
    async def save(
        self, entity: UserEntity
    ) -> 'UserRepository.WriteInfo[UserEntity]':
        entity_dict = entity.model_dump()
        user_db = UserTable(**entity_dict)

        # DOCUMENT: This syntax for nested session
        async with self.session.begin():
            self.session.add(user_db)

        await self.session.refresh(user_db)

        return UserRepository.WriteInfo(
            entity=UserEntity.model_validate(user_db),
            write_info={}
        )

    async def find_by_id(self, entity_id: UUID4) -> UserEntity | None:
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

    async def find_all(self, limit: int, offset: int) -> list[UserEntity]:
        query = select(UserTable).offset(offset).limit(limit)

        async with self.session.begin():
            result = await self.session.execute(query)

        return result.scalars().all()  # type: ignore

    # not tested
    async def delete(self, entity_id: UUID4) -> None:
        query = select(UserTable).where(UserTable.id == entity_id)

        async with self.session.begin():
            result = await self.session.execute(query)
            user = result.scalars().first()
            if user:
                await self.session.delete(user)
