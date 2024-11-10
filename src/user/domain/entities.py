from datetime import datetime

from pydantic import BaseModel


class UserEntity(BaseModel):
    email: str
    username: str
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
        self.updated_at = datetime.datetime.now()

    def deactivate(self):
        self.is_active = False
        self.updated_at = datetime.datetime.now()

    def activate(self):
        self.is_active = True
        self.updated_at = datetime.datetime.now()
