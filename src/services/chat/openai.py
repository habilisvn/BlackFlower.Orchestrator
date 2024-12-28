from openai import OpenAI

from chat.domain.entities import ChatMessage
from services.chat.base import ChatService
from common.mixins import SettingsMixin


class OpenAIChatService(ChatService, SettingsMixin):
    openai_api_key: str = "openai_api_key"

    def __init__(self):
        super().__init__()

        self.client = OpenAI(api_key=self.openai_api_key)

    async def send_message(self, message: ChatMessage) -> str:
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[message],
            max_tokens=16384,
        )
        return completion.choices[0].message.content
