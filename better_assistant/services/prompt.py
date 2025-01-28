from datetime import datetime
from typing import Dict, List

from bson import ObjectId

from better_assistant.models import MongoFilter, MongoUpdate, Prompt
from better_assistant.utils import MongoClientWrapper

class PromptService:
    def __init__(self):
        self.mongo_client = MongoClientWrapper()

    async def get_prompts(self, project_id: str) -> List[Dict[str, any]]:
        filter_obj = (
            MongoFilter()
            .equals("project_id", project_id)
            .fields(["prompt_version", "prompt_content", "updated_at", "_id"])
            .build_with_projection()
            )
        result: List[Dict[str, any]] = await self.mongo_client.find(filter_obj, collection_name="prompts")

        for data in result:
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value, ObjectId):
                    data[key] = value.__str__()
        return result
    
    async def create_prompt(self, prompt: Prompt) -> ObjectId:
        return await self.mongo_client.insert(prompt, "prompts")
    
    async def update_prompt(self, prompt_id: str, prompt: Prompt) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(prompt_id))
            .build()
            )
        update_obj = (
            MongoUpdate()
            .set("prompt_content", prompt.prompt_content)
            .set_updated_at()
            .build()
        )
        return await self.mongo_client.update(filter_obj, update_obj, collection_name="prompts")