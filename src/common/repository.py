from abc import ABC, abstractmethod
from uuid import UUID


class AbstractRepository[T](ABC):
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save an entity to the repository."""
        pass

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> T | None:
        """Find an entity by its ID."""
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> None:
        """Delete an entity from the repository by its ID."""
        pass
