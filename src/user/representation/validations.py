from datetime import datetime
import re
from pydantic import Field, field_validator

from user.base.model import UserBase
from user.infra.repository import UserRepository


class UserGetIn(UserBase):
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False, min_length=6)

    @field_validator("username")
    def validate_username(cls, username: str, userRepository: UserRepository) -> str:
        existing_user = userRepository.get_user_by_username(username)
        if existing_user:
            raise ValueError("Username already exists")
        return username


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserCreateIn(UserBase):
    username: str
    password: str = Field(min_length=6)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"\W", v):
            raise ValueError("Password must contain at least one special character")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v


class UserPublic(UserBase):
    pass
