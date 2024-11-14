from dataclasses import dataclass
from enum import Enum
import re

@dataclass(frozen=True)
class Email:
    address: str

    _email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")  # Basic email regex

    def __post_init__(self):
        # Validate email format
        if not self._is_valid_email(self.address):
            raise ValueError(f"Invalid email address: {self.address}")

    @staticmethod
    def _is_valid_email(address: str) -> bool:
        return Email._email_pattern.match(address) is not None

    def __str__(self) -> str:
        return self.address
