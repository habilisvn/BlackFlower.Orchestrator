from datetime import datetime
import re
from pydantic import UUID4, BaseModel, Field, field_validator
import hashlib


class NodeBase(BaseModel):
    label: str


class NodeGetIn(NodeBase):
    pass


class NodeOut(NodeBase):
    id: UUID4


class NodeCreateIn(NodeBase):
    updated_at: datetime | None = None  # type: ignore
    created_at: datetime | None = None  # type: ignore
    password: str = Field(min_length=6)

    @field_validator("password")
    def validate_password(cls, value: str):
        if not re.search(r"\W", value):
            raise ValueError("Password must contain at least one special character")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")

        # TEMPORARY: implementation to hash password
        hash_pwd = hashlib.sha512(value.encode()).hexdigest()

        return hash_pwd


class NodePublic(NodeBase):
    pass
