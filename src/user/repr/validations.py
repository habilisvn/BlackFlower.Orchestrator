from datetime import datetime
import re
from pydantic import Field, field_validator
import hashlib

from user.base.model import UserBase


class UserGetIn(UserBase):
    username: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False, min_length=6)


class UserOut(UserBase):
    id: int


class UserCreateIn(UserBase):
    updated_at: datetime = None
    created_at: datetime = None
    password: str = Field(min_length=6)

    @field_validator("password")
    def validate_password(cls, v):
        if not re.search(r"\W", v):
            raise ValueError("Password must contain at least one special character")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")

        ### TEMPORARY: implementation to hash password
        hash_pwd = hashlib.sha512(v.encode()).hexdigest()

        return hash_pwd


class UserPublic(UserBase):
    pass
