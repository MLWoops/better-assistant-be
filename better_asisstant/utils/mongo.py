from pymongo import MongoClient
from better_asisstant.exceptions import NoDataException

class mongo_clinet:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['better_assistant']
        self.collection = self.db['user']

    def insert(self, data):
        if not data:
            raise NoDataException("Data is required")
        
        self.collection.insert_one(data)

    def find(self, data):
        if not data:
            raise NoDataException("Data is required")
        
        return self.collection.find_one(data)

    def update(self, data, new_data):
        if not data:
            raise NoDataException("Data is required")
        if not new_data:
            raise NoDataException("New data is required")
        
        self.collection.update_one(data, new_data)

    def delete(self, data):
        if not data:
            raise NoDataException("Data is required")
        
        self.collection.delete_one(data)
