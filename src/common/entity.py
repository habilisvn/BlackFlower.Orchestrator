from datetime import datetime, timezone
from uuid import uuid4

from pydantic import UUID4


class BaseEntity:
    def __init__(
        self,
        id: UUID4 | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        self.id = id or str(uuid4())
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def update_timestamp(self):
        self.updated_at = datetime.now(timezone.utc)
