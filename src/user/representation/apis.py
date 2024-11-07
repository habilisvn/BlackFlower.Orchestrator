from typing import Annotated
from fastapi import APIRouter, Depends

from user.domain.entities import UserEntity
from user.representation.dependencies import user_repository_dpd
from user.representation.validations import UserCreateIn, UserOut
from user.use_case.create_user_use_case import CreateUserUseCase
from user.use_case.get_user_use_case import GetUserUseCase


router = APIRouter(
    prefix="/api/v1/users",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int, use_case: Annotated[GetUserUseCase, Depends(user_repository_dpd)]
) -> UserOut:
    result = await use_case(user_id)
    return result


@router.post("", response_model=UserOut)
async def create_user(
    user: UserCreateIn,
    user_repo_dpd: Annotated[CreateUserUseCase, Depends(user_repository_dpd)],
):
    user_entity = UserEntity(**user.dict())
    result = await user_repo_dpd(user_entity)
    return result
