from huggingface_hub import InferenceClient

from chat.domain.entities import ChatMessage
from services.chat.base import ChatService
from common.mixins import SettingsMixin


class HuggingFaceChatService(ChatService, SettingsMixin):
    huggingface_api_key: str = "huggingface_api_key"

    def __init__(self):
        super().__init__()

        self.supported_formats = {
            ".pdf",
            ".doc",
            ".docx",
            ".txt",
        }
        self.API_URL = (
            "https://api-inference.huggingface.co/models/meta-llama/"
            "Llama-3.3-70B-Instruct/v1/chat/completions"
        )
        self.headers = {
            "Authorization": f"Bearer {self.huggingface_api_key}"
        }

    async def send_message(self, message: ChatMessage) -> str:
        client = InferenceClient(
            model="meta-llama/Llama-3.3-70B-Instruct",
            token=self.huggingface_api_key,
        )

        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=list(message),
            max_tokens=50000,
        )
        return completion.choices[0].message.content
