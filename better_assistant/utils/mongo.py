import os

from pymongo import MongoClient

from better_assistant.exceptions import (
    CollectionNotDefinedException,
    DataNotCreatedException,
    DataNotDeletedException,
    DataNotReadException,
    DataNotUpdatedException,
    DataNotFoundException,
    NoFilterException,
)


class mongo_client:
    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        mongo_db = os.getenv("MONGO_DB")

        self.client = MongoClient(host=mongo_host, port=int(mongo_port))
        self.db = self.client.get_database(mongo_db)

    def insert(self, data, collection=None):

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not data:
            raise NoFilterException("Data is required")
        collection = self.db.get_collection(collection)
        result = collection.insert_one(data)

        if result.acknowledged:
            return result.inserted_id
        else:
            raise DataNotCreatedException("Data not created")


    def find(self, filter, collection=None):

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")
        collection = self.db.get_collection(collection)
        result = collection.find_one(filter)

        if result:
            return result
        else:
            raise DataNotReadException("Data not found")
        
    def find_all(self, filter, collection=None):
        
        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        
        if not filter:
            raise NoFilterException("Data is required")
        
        collection = self.db.get_collection(collection)
        result = collection.find(filter)

        if result:
            return result
        else:
            raise DataNotReadException("Data not found")

    def update(self, filter, update, collection=None):

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
            return DataNotFoundException("No data to update")
        else:
            raise DataNotUpdatedException("Update failed")

    def delete(self, filter, collection=None):

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
