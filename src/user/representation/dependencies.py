from user.infra.repository import UserRepository
from common.dependencies import SessionDependency


async def get_user_repository(session: SessionDependency) -> UserRepository:
    return UserRepository(session)
