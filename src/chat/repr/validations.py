from pydantic import BaseModel


class ChatInput(BaseModel):
    message: str


class ChatOutput(BaseModel):
    reply: str
