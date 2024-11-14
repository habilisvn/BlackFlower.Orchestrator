from datetime import datetime
from sqlalchemy.orm import mapped_column, Mapped
from uuid import uuid4
from sqlalchemy import UUID

from common.alchemy import Base


class UserTable(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(insert_default=datetime.now)
    updated_by: Mapped[int | None]
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=datetime.now, onupdate=datetime.now
    )
