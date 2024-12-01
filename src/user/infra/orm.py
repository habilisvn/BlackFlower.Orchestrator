from sqlalchemy.orm import mapped_column, Mapped
from uuid import uuid4
from sqlalchemy import UUID

from common.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    full_name: Mapped[str]
    phone_number: Mapped[str | None]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
