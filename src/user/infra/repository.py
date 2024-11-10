from uuid import UUID
from sqlmodel import or_, select

from common.exceptions import MissingParameterException
from common.repository import AbstractRepository
from user.domain.entities import UserEntity
from user.infra.orm import UserTable
from common.dependencies import SessionDependency


class UserRepository(AbstractRepository[UserEntity]):
    def __init__(self, session: SessionDependency):
        self.session = session

    async def save(self, user: UserEntity) -> UserEntity:
        user_db = UserTable(**user.dict())

        ### DOCUMENT: This syntax for nested session
        async with self.session.begin():
            self.session.add(user_db)

        await self.session.refresh(user_db)

        return user_db

    async def get_user_by_unique_key(
        self,
        id: str | None = None,
        email: str | None = None,
        username: str | None = None,
    ) -> UserTable:
        if id is None and email is None and username is None:
            raise MissingParameterException(valid_params=["id", "email", "username"])

        query = select(UserTable).where(
            or_(
                UserTable.email == email if email else False,
                UserTable.username == username if username else False,
            )
        )

        ### DOCUMENT: Must begin nested session or commit changes
        async with self.session.begin():
            users = await self.session.execute(query)

        user = users.first()
        return user

    async def delete(self, user_id) -> None:
        pass

    async def find_by_id(self, entity_id: UUID) -> UserEntity | None:
        pass
