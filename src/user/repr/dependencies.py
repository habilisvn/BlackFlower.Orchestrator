from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from common.dependencies import SessionDependency
from user.repr.validations import UserCreateIn


async def get_user_repository(session: SessionDependency) -> UserRepository:
    return UserRepository(session)


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


async def validate_user_exists(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserEntity:
    user = await user_repo.find_by_username(form_data.username)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


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


# async def validate_id_exists(
#     user_id: str,
#     user_repo: Annotated[UserRepository, Depends(get_user_repository)]
# ) -> str:
#     check = await user_repo.find_by_id(user_id)
#     if not check:
#         raise HTTPException(
#             status_code=404,
#             detail="User not found"
#         )
#     return user_id
