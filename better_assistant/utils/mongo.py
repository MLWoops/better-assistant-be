import os

from bson import objectid
from pymongo import MongoClient

from better_assistant.exceptions import (
    CollectionNotDefinedException,
    DataNotCreatedException,
    DataNotDeletedException,
    DataNotFoundException,
    DataNotUpdatedException,
    NoFilterException,
)
from better_assistant.models import MongoDocument, MongoFilter


class MongoClientWrapper:
    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        mongo_db = os.getenv("MONGO_DB")

        self.client = MongoClient(host=mongo_host, port=int(mongo_port))
        self.db = self.client.get_database(mongo_db)

    def __create_index__(self):
        self.db.get_collection("projects").create_index("project_title", unique=True)
        self.db.get_collection("prompts").create_index("prompt_version", unique=True)
        self.db.get_collection("dialogs").create_index("dialog_title", unique=True)

    def insert(self, document: MongoDocument, collection: str=None) -> objectid:

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not document:
            raise NoFilterException("Data is required")
        collection = self.db.get_collection(collection)

        document = document.to_dict()
        result = collection.insert_one(document)

        if result.acknowledged:
            return result.inserted_id
        else:
            raise DataNotCreatedException("Data not created")


    def find(self, filter: MongoFilter, collection: str=None) -> MongoDocument:

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")
        collection = self.db.get_collection(collection)
        result = collection.find(filter)

        if result:
            return result
        else:
            raise DataNotFoundException("Data not found")

    def update(self, filter: MongoFilter, update, collection: str=None) -> bool:

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")
        if not update:
            raise NoFilterException("New data is required")
        collection = self.db.get_collection(collection)
        result = collection.update_one(filter, update)

        if result.acknowledged:
            if result.modified_count > 0:
                return True
            raise DataNotFoundException("No data to update")
        else:
            raise DataNotUpdatedException("Update failed")

    def delete(self, filter: MongoFilter, collection: str=None) -> bool:

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")

        collection = self.db.get_collection(collection)
        result = collection.delete_one(filter)

        if result.acknowledged:
            if result.deleted_count > 0:
                return True
            raise DataNotFoundException("No data to delete")
        else:
            raise DataNotDeletedException("Deleted failed")
