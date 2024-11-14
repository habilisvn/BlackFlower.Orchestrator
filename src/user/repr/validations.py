from datetime import datetime
import re
from pydantic import Field, field_validator
import hashlib

from user.base.model import UserBase


class UserGetIn(UserBase):
    pass


class UserOut(UserBase):
    id: int


class UserCreateIn(UserBase):
    updated_at: datetime | None = None  # type: ignore
    created_at: datetime | None = None  # type: ignore
    password: str = Field(min_length=6)

    @field_validator("password")
    def validate_password(cls, value: str):
        if not re.search(r"\W", value):
            raise ValueError(
                "Password must contain at least one special character"
            )
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        # TEMPORARY: implementation to hash password
        hash_pwd = hashlib.sha512(value.encode()).hexdigest()

        return hash_pwd


class UserPublic(UserBase):
    pass
