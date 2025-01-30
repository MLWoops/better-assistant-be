import asyncio
import os

from openai import AsyncOpenAI

from better_assistant.models import GenerateRequest
from better_assistant.services import ChatService


class GenerateService:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
        api_base_url = os.getenv("API_BASE_URL")
        api_key = os.getenv("API_KEY")
        self.model_name = os.getenv("MODEL_NAME")
        self.client = AsyncOpenAI(api_key=api_key, base_url=api_base_url)

    async def generate(self, generate_request: GenerateRequest):
        stream = await self.client.chat.completions.create(
            model=self.model_name,
            messages=generate_request.messages,
            max_tokens=1024,
            temperature=1.2,
            stream=True
        )

        llm_response = ""

        async for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                llm_response += content
                yield f"data: {content}\n\n"

            await asyncio.sleep(0.001)

        await self.chat_service.add_msgs_to_dialog(
            generate_request.dialog_id,
            [
                {"content": generate_request.user_input, "role": "user"},
                {"content": llm_response, "role": "assistant"}
            ]
        )
