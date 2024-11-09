from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine

from config.settings import get_settings

settings = get_settings()
engine = create_async_engine(settings.postgresql_url, echo=False)


class Base(AsyncAttrs, DeclarativeBase):
    type_annotation_map = {}
