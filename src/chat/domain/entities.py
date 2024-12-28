from common.base import BaseEntity


class ChatMessage(BaseEntity):
    role: str
    content: str


class ExternalUser(BaseEntity):
    id: str
    assistant_id: str
    thread_id: str
