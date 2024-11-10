from typing import Annotated
from fastapi import Depends
from fastapi.responses import JSONResponse

from common.utils import iterate_validate
from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from user.repr.dependencies import get_user_repository
from user.repr.validations import UserCreateIn, UserOut
from user.router import router


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int, user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserOut:
    result = await user_repo.get_user_by_unique_key(id=user_id)

    # TEMPORARY: refactor to only one response in the future
    return result or JSONResponse(status_code=404, content={"detail": "User not found"})


@router.post("", response_model=UserOut)
async def create_user(
    user: UserCreateIn,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    # validate user email exists
    await iterate_validate(
        func=user_repo.get_user_by_unique_key, input=user.model_dump()
    )

    user_entity = UserEntity(**user.model_dump())
    result = await user_repo.save(user_entity)
    return result
