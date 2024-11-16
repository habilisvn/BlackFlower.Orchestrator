from abc import ABC, abstractmethod

from pydantic import UUID4


class AbstractRepository[T](ABC):
    @abstractmethod
    async def save(self, entity: T) -> T:
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
