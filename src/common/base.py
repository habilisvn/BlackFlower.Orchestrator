from mongoengine.document import Document
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Any
from pydantic import BaseModel, model_validator
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {}

    created_by: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now)
    updated_by: Mapped[int | None]
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.now, onupdate=datetime.now
    )


class BaseEntity(BaseModel):
    @model_validator(mode="before")
    def _model_entry(cls, _input: Any) -> Any:
        if isinstance(_input, Base) or isinstance(_input, BaseModel):
            return jsonable_encoder(_input)
        return _input


class BaseDocument(Document):
    meta = {"abstract": True}

    created_by: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now)
    updated_by: Mapped[int | None]
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.now, onupdate=datetime.now
    )
