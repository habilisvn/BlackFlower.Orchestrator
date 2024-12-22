from common.base import BaseEntity


class ChatMessage(BaseEntity):
    role: str
    content: str
