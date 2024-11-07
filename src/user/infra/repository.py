from sqlmodel import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from user.domain.entities import UserEntity
from user.infra.database import UserTable
from config.session import SessionDependency
from config.session import engine


class UserRepository:
    def __init__(self, session: SessionDependency = None):
        self.session = session

    async def create_user(self, user: UserEntity) -> UserEntity:
        new_user = UserTable(**user.dict())

        # async_session = async_sessionmaker[AsyncSession](engine)
        # Implementation to create a user in the database
        async with async_sessionmaker[AsyncSession](engine)() as session:
            async with session.begin():
                session.add(new_user)

            await session.refresh(new_user)
        return new_user

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
