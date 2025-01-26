from better_asisstant.utils import mongo_client


class HistoryManager:
    def __init__(self):
        self.mongo = mongo_client()
