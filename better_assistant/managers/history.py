from better_assistant.models import Dialog, MongoFilter
from better_assistant.utils import MongoClientWrapper


class HistoryManager:
    def __init__(self):
        self.mongo = MongoClientWrapper()

    def get_dialogs(self):
        filter_obj = (
            MongoFilter()
            .exists("dialog_title")
            .exists("update_at")
            .build()
        )

        return list(self.mongo.find(filter_obj, 'dialogs'))

    def get_dialog(self, dialog_id) -> Dialog:
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .build()
        )
        result = (list(self.mongo.find(filter_obj, 'dialogs')))[0]
        return Dialog.from_dictresult(result)

    def post_dialog(self, dialog: Dialog):
        return self.mongo.insert(dialog, 'dialogs')

    def update_dialog(self, dialog_id, dialog):
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .build()
        )
        return self.mongo.update(filter_obj, dialog, 'dialogs')

    def delete_dialog(self, dialog_id):
        filter_obj = (
            MongoFilter()
            .equals("dialog_id", dialog_id)
            .build()
        )
        return self.mongo.delete(filter_obj, 'dialogs')
