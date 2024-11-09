from uuid import UUID
from sqlmodel import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from common.repository import AbstractRepository
from user.domain.entities import UserEntity
from user.infra.orm import UserTable
from common.db import engine
from common.dependencies import SessionDependency


class UserRepository(AbstractRepository[UserEntity]):
    def __init__(self, session: SessionDependency):
        self.session = session
    
    async def save(self, user: UserEntity) -> UserEntity:
        user_db = UserTable(**user.dict())
        
        # async_session = async_sessionmaker[AsyncSession](engine)
        # Implementation to create a user in the database
        async with self.session.begin():
            self.session.add(user_db)

        await self.session.refresh(user_db)
        return user_db

    async def get_user_by_id(self, user_id) -> UserTable:
        query = select(UserTable).where(UserTable.id == user_id)
        users = await self.session.execute(query)
        user = users.first()
        return user

    async def get_user_by_username(self, username) -> UserTable:
        query = select(UserTable).where(UserTable.username == username)
        users = await self.session.exec(query)
        # NOTE: what is scalars
        user = users.scalars().first()
        return user

    async def delete(self, user_id) -> None:
        pass
    
    async def find_by_id(self, entity_id: UUID) -> UserEntity|None:
        pass
