from typing import Annotated
from fastapi import APIRouter, Depends

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from user.representation.dependencies import get_user_repository
from user.representation.validations import UserCreateIn, UserOut


router = APIRouter(
    prefix="/api/v1/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int, user_repo_dpd: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserOut:
    result = await user_repo_dpd.get_user_by_id(user_id)
    return result


@router.post("", response_model=UserOut)
async def create_user(
    user: UserCreateIn,
    user_repo_dpd: Annotated[UserRepository, Depends(get_user_repository)]
):
    user_entity = UserEntity(**user.model_dump())
    result = await user_repo_dpd.save(user_entity)
    return result
