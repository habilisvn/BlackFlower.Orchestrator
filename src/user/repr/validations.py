from datetime import datetime
import re
from typing_extensions import Annotated
from pydantic import Field, ValidationError, field_validator
from pydantic.functional_validators import AfterValidator

from user.base.model import UserBase
from user.infra.repository import UserRepository
from common.dependencies import SessionDependency


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
        return v


class UserPublic(UserBase):
    pass
