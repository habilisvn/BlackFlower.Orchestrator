from datetime import datetime
from uuid import UUID

from common.base import BaseEntity


class UserEntity(BaseEntity):
    id: UUID | None = None
    email: str
    username: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    created_by: int | None
    created_at: datetime | None = None
    updated_by: int | None
    updated_at: datetime | None = None
    password: str | None

    def update_email(self, new_email: str):
        if "@" not in new_email:
            raise ValueError("Invalid email")
        self.email = new_email
        self.updated_at = datetime.now()

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.now()

    def activate(self):
        self.is_active = True
        self.updated_at = datetime.now()

