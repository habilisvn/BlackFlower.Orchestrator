from abc import ABC, abstractmethod
from datetime import datetime
from dataclasses import dataclass

from common.base import BaseEntity


@dataclass
class ChatOptions:
    temperature: float = 0.7
    max_tokens: int | None = None
    conversation_id: str | None = None
    system_prompt: str | None = None


@dataclass
class ChatResponse:
    message: str
    conversation_id: str
    timestamp: datetime


@dataclass
class ChatMessage:
    role: str  # 'user', 'assistant', or 'system'
    content: str
    timestamp: datetime


class ChatService(ABC):
    @abstractmethod
    async def send_message(self, message: BaseEntity) -> ChatResponse:
        pass
