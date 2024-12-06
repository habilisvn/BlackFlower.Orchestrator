from abc import ABC, abstractmethod
from typing import Any


class AbstractRepository[T](ABC):
    @abstractmethod
    async def save(self, entity: T, upsert: bool = False) -> T:
        """Save an entity to the repository."""
        pass

    @abstractmethod
    async def find_all(self, limit: int, offset: int) -> list[T]:
        """Find all entities."""
        pass

    @abstractmethod
    async def find_by_primary_key(self, primary_value: Any) -> T | None:
        """Find an entity by its ID."""
        pass

    @abstractmethod
    async def delete(self, primary_value: Any) -> None:
        """Delete an entity from the repository by its ID."""
        pass
