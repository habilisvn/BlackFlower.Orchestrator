from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlmodel import Field  # type: ignore


class UserBase(BaseModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    full_name: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_by: int | None = Field(default=None)
    created_at: datetime
    updated_by: int | None = Field(default=None)
    updated_at: datetime
