from user.domain.entities import UserEntity
from user.infra.repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, user: UserEntity):
        created_user = await self.user_repository.create_user(user)
        return created_user
