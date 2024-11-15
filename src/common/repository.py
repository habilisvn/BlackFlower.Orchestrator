from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pydantic import UUID4


class AbstractRepository[T](ABC):
    @dataclass(kw_only=True)
    class WriteInfo[T2]:
        entity: T2
        write_info: dict[str, Any]

    @abstractmethod
    async def save(self, entity: T) -> 'WriteInfo[T]':
        """Save an entity to the repository."""
        pass

    @abstractmethod
    async def find_all(self, limit: int, offset: int) -> list[T]:
        """Find all entities."""
        pass

    @abstractmethod
    async def find_by_id(self, entity_id: UUID4) -> T | None:
        """Find an entity by its ID."""
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID4) -> None:
        """Delete an entity from the repository by its ID."""
        pass
