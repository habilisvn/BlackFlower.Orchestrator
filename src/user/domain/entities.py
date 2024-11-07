from dataclasses import dataclass

from common.entity import BaseEntity
from user.base.model import UserBase

@dataclass
class UserEntity(UserBase, BaseEntity):
    password: str | None
    
    @classmethod
    def create(cls) -> "UserEntity":
        pass
