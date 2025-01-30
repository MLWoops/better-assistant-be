from datetime import datetime
from typing import Dict, List

from bson import ObjectId

from better_assistant.models import Dialog, MongoFilter, MongoUpdate
from better_assistant.utils import MongoClientWrapper


class ChatService:
    def __init__(self, mongo_client: MongoClientWrapper):
        self.mongo_client = mongo_client

    async def get_dialogs(self, project_id: str) -> List[Dict[str, any]]:
        filter_obj = (
            MongoFilter()
            .equals("project_id", project_id)
            .fields(["dialog_title", "updated_at", "_id"])
            .build_with_projection()
            )
        result: List[Dict[str, any]] = await self.mongo_client.find(filter_obj, collection_name="dialogs")

        for data in result:
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value, ObjectId):
                    data[key] = value.__str__()
        return result

    async def get_dialog(self, project_id: str, dialog_id: str) -> dict:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(dialog_id))
            .equals("project_id", project_id)
            .fields(["dialog_title", "dialog_content", "updated_at", "project_id"])
            .build_with_projection()
            )
        result = await self.mongo_client.find(filter_obj, collection_name="dialogs")
        return Dialog.from_dict(data=result[0]).to_dict()

    async def create_dialog(self, dialog: Dialog) -> ObjectId:
        return await self.mongo_client.insert(dialog, "dialogs")

    async def update_dialog(self, dialog_id: str, dialog: Dialog) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(dialog_id))
            .build()
            )
        update_obj = (
            MongoUpdate()
            .set("dialog_title", dialog.dialog_title)
            .set_updated_at()
            .build()
        )
        return await self.mongo_client.update(filter_obj, update_obj, collection_name="dialogs")

    async def add_msg_to_dialog(self, dialog_id: str, msg: Dict[str, any]) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(dialog_id))
            .build()
            )
        update_obj = (
            MongoUpdate()
            .push("dialog_content", msg)
            .set_updated_at()
            .build()
        )
        return await self.mongo_client.update(filter_obj, update_obj, collection_name="dialogs")

    async def add_msgs_to_dialog(self, dialog_id: str, msgs: List[Dict[str, any]]) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(dialog_id))
            .build()
            )
        update_obj = (
            MongoUpdate()
            .push_all("dialog_content", msgs)
            .set_updated_at()
            .build()
        )
        return await self.mongo_client.update(filter_obj, update_obj, collection_name="dialogs")

    async def delete_dialog(self, dialog_id: str) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(dialog_id))
            .build()
            )
        return await self.mongo_client.delete(filter_obj, collection_name="dialogs")
