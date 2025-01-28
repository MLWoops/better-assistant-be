from typing import List

from better_assistant.models import Dialog, MongoFilter, MongoUpdate
from better_assistant.models.models import Msg
from better_assistant.utils import MongoClientWrapper


class HistoryManager:
    def __init__(self):
        self.mongo = MongoClientWrapper()

    async def get_dialogs(self):
        filter_obj = (
            MongoFilter()
            .fields(["dialog_title", "updated_at"])
            .build_with_projection()
        )

        return await self.mongo.find(filter_obj, 'dialogs')

    async def get_dialog(self, dialog_id) -> Dialog:
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .fields(["dialog_title", "dialog_content", "updated_at"])
            .build_with_projection()
        )
        result = self.mongo.find(filter_obj, 'dialogs')[0]
        return await Dialog.from_dict(result)

    async def post_dialog(self, dialog: Dialog):
        return await self.mongo.insert(dialog, 'dialogs')

    async def update_dialog(self, dialog_id, dialog):
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .build()
        )
        update_obj = (
            MongoUpdate()
            .set("dialog_title", dialog.dialog_title)
            .set("dialog_content", dialog.dialog_content)
            .set_updated_at()
            .build()
        )
        return await self.mongo.update(filter_obj, update_obj, 'dialogs')

    async def push_new_messages(self, dialog_id, new_messages: List[Msg]):
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .build()
        )
        update_obj = (
            MongoUpdate()
            .push("dialog_content", new_messages)
            .set_updated_at()
            .build()
        )
        return await self.mongo.update(filter_obj, update_obj, 'dialogs')

    async def delete_dialog(self, dialog_id):
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .build()
        )
        return await self.mongo.delete(filter_obj, 'dialogs')
