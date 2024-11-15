from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Query
from pydantic import UUID4

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from user.repr.dependencies import (
    get_current_user,
    get_user_repository,
    validate_email_exists,
    validate_username_exists,
)
from user.repr.validations import UserCreateIn, UserOut


router = APIRouter(
    prefix="/v1/users",
    tags=["user"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=dict[str, list[UserOut] | int])
async def get_users(
    *,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    offset = (page - 1) * page_size
    result = await user_repo.find_all(
        limit=page_size,
        offset=offset
    )

    return {
        "data": result,
        "page": page,
        "page_size": page_size
    }


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID4,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    result = await user_repo.find_by_id(entity_id=user_id)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.post(
    "",
    response_model=UserOut
)
async def create_user(
    user: UserCreateIn,
    username: Annotated[str, Depends(validate_username_exists)],
    email: Annotated[str, Depends(validate_email_exists)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
):
    # Prepare the user entity
    user_dict = user.model_dump()
    user_dict.update({"username": username, "email": email})
    user_entity = UserEntity(**user_dict)

    # Save the user entity
    result = await user_repo.save(user_entity)
    return result
