from typing import Annotated
from uuid import UUID
from fastapi import Depends, HTTPException, APIRouter

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from user.repr.dependencies import (
    get_user_repository,
    validate_email_exists,
    validate_username_exists,
)
from user.repr.validations import UserCreateIn, UserOut


router = APIRouter(prefix="/users", tags=["user"])


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserOut:
    result = await user_repo.find_by_id(entity_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result  # type: ignore


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
