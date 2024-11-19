from typing import Annotated
from fastapi import Depends, HTTPException

from user.infra.repository import UserRepository
from common.dependencies import SessionDependency
from user.repr.validations import UserCreateIn


async def get_node_repository(session: SessionDependency) -> UserRepository:
    return UserRepository(session)


# TEMPORARY: Remove in the future
async def validate_email_exists(
    user: UserCreateIn,
    user_repo: Annotated[UserRepository, Depends(get_node_repository)]
) -> str:
    check = await user_repo.find_by_email(user.email)
    if check:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    return user.email
