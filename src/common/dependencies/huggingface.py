from typing import Annotated
from fastapi import Depends, Header

from services.chat.base import ChatService
from services.chat.huggingface import HuggingFaceChatService
from services.chat.openai import OpenAIChatService


async def get_chat_service(
    ai_agent: str | None = Header(None, alias="ai-agent"),
) -> ChatService:
    if ai_agent is None:
        return HuggingFaceChatService()

    if ai_agent.lower() == "huggingface":
        return HuggingFaceChatService()
    elif ai_agent.lower() == "openai":
        return OpenAIChatService()
    else:
        raise ValueError(
            "Invalid ai-agent header. Must be 'huggingface' or 'openai'"
        )


ChatServiceDpd = Annotated[ChatService, Depends(get_chat_service)]
