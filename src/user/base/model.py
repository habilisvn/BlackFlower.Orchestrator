from dataclasses import dataclass
from pydantic import EmailStr
from sqlmodel import Field, SQLModel


@dataclass
class UserBase(SQLModel):
    username: str = Field(index=True, unique=True, nullable=False)
    email: EmailStr = Field(index=True, unique=True, nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_by: int | None = Field(default=None)
    updated_by: int | None = Field(default=None)
