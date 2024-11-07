from user.domain.entities import UserEntity
from user.infra.repository import UserRepository


class GetUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(
        self,
        user_id: str,
    ) -> UserEntity:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
