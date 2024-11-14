from typing import Annotated
from uuid import UUID
from fastapi import Depends
from fastapi import HTTPException

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from user.repr.dependencies import get_user_repository
from user.repr.validations import UserCreateIn, UserOut
from user.router import router


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserOut:
    result = await user_repo.find_by_id(entity_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result  # type: ignore


async def validate_username_exists(
    user: UserCreateIn,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> str:
    check = await user_repo.find_by_username(user.username)
    if check:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )
    return user.username


async def validate_email_exists(
    user: UserCreateIn,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> str:
    check = await user_repo.find_by_email(user.email)
    if check:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return user.email


@router.post("/", response_model=UserOut)
async def create_user(
    user: UserCreateIn,
    username: Annotated[str, Depends(validate_username_exists)],
    email: Annotated[str, Depends(validate_email_exists)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserOut:
    user_dict = user.model_dump()
    user_dict.update({"username": username, "email": email})
    user_entity = UserEntity(**user_dict)
    result = await user_repo.save(user_entity)
    return result  # type: ignore
