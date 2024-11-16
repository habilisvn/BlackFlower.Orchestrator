from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from typing import Any
from pydantic import BaseModel, model_validator
from fastapi.encoders import jsonable_encoder


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {}


class BaseEntity(BaseModel):
    @model_validator(mode="before")
    def _model_entry(cls, _input: Any) -> Any:
        if isinstance(_input, Base) or isinstance(_input, BaseModel):
            return jsonable_encoder(_input)
        return _input
