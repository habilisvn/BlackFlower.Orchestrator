from typing import Annotated
from fastapi import Depends

from user.use_case.create_user_use_case import CreateUserUseCase
from user.use_case.get_user_use_case import GetUserUseCase
from user.infra.repository import UserRepository
from user.representation.validations import UserOut


# def user_repository_dpd(session: SessionDependency) -> UserRepository:
#     return UserRepository(session)


def user_repository_dpd() -> UserRepository:
    return UserRepository()
