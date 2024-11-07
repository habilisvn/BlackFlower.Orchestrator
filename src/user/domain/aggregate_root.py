from typing import Optional
from user.domain.entities import User
from .value_objects import Email, UserStatus
from datetime import datetime


class UserAggregate:
    def __init__(
        self,
        user_id: int,
        email: str,
        username: str,
        created_at: Optional[datetime] = None,
    ):
        self.user = User(
            id=user_id,
            email=Email(email),
            username=username,
            created_at=created_at or datetime.now(),
        )
        self.status = (
            UserStatus.ACTIVE
        )  # Assume UserStatus is an enum in value_objects.py

    def change_email(self, new_email: str) -> None:
        """Change the user's email, ensuring the email is valid."""
        if not Email.is_valid(new_email):
            raise ValueError("Invalid email address.")
        self.user.email = Email(new_email)

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.status = UserStatus.INACTIVE

    def activate(self) -> None:
        """Activate the user account."""
        self.status = UserStatus.ACTIVE

    def is_active(self) -> bool:
        """Check if the user account is active."""
        return self.status == UserStatus.ACTIVE

    def get_user_info(self) -> dict:
        """Return a dictionary of user information."""
        return {
            "user_id": self.user.id,
            "email": self.user.email.address,
            "username": self.user.username,
            "status": self.status.name,
            "created_at": self.user.created_at.isoformat(),
        }
