from typing import Annotated
from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from user.domain.entities import UserEntity
from user.infra.repository import UserRepository
from common.dependencies import PostgresDependency, SettingsDependency
from user.repr.validations import UserCreateIn


async def get_user_repository(session: PostgresDependency) -> UserRepository:
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


async def get_current_user(
    *,
    access_token: Annotated[str | None, Cookie()] = None,
    settings: SettingsDependency,
    user_repo: Annotated[UserRepository, Depends(get_user_repository)]
) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if access_token is None:
        raise credentials_exception

    try:
        payload = jwt.decode(  # type: ignore
            access_token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception

    user = await user_repo.find_by_username(username)
    if user is None:
        raise credentials_exception
    return user
