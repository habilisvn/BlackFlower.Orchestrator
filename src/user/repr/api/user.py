from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Query
from pydantic import UUID4

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from user.infra.services.notify import notify_user_created
from user.repr.dependencies import (
    get_current_user,
    get_user_repository,
    validate_email_exists,
    validate_username_exists,
)
from user.repr.validations import UserCreateIn, UserOut


router = APIRouter(
    prefix="/v1/users", tags=["user"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=dict[str, list[UserOut] | int])
async def get_users(
    *,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    offset = (page - 1) * page_size
    result = await user_repo.find_all(limit=page_size, offset=offset)

    return {"data": result, "page": page, "page_size": page_size}


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID4,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    result = await user_repo.find_by_primary_key(entity_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post("", response_model=UserOut, status_code=201)
async def create_user(
    user: UserCreateIn,
    username: Annotated[str, Depends(validate_username_exists)],
    email: Annotated[str, Depends(validate_email_exists)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    # Prepare the user entity
    user.username = username
    user.email = email

    user_entity = UserEntity.model_validate(user)

    # Save the user entity and get the new user entity
    user_entity = await user_repo.save(user_entity)

    # Send the user created event
    await notify_user_created(user_entity)

    return user_entity


@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: UUID4,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    await user_repo.delete(entity_id=user_id)
