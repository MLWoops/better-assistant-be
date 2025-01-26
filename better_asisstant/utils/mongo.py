import os

from pymongo import MongoClient

from better_asisstant.exceptions import (
    CollectionNotDefinedException,
    DataNotCreatedException,
    DataNotDeletedException,
    DataNotReadException,
    DataNotUpdatedException,
    NoDataException,
)


class mongo_client:
    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST")
        mongo_port = os.getenv("MONGO_PORT")
        mongo_db = os.getenv("MONGO_DB")

        self.client = MongoClient(host=mongo_host, port=int(mongo_port))
        self.db = self.client.get_database(mongo_db)

    def create(self, data, collection=None):

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not data:
            raise NoDataException("Data is required")
        collection = self.db.get_collection(collection)
        result = collection.insert_one(data)

        if result.acknowledged:
            return result.inserted_id
        else:
            raise DataNotCreatedException("Data not created")


    def read(self, data, collection=None):

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not data:
            raise NoDataException("Data is required")
        collection = self.db.get_collection(collection)
        result = collection.find_one(data)

        if result:
            return result
        else:
            raise DataNotReadException("Data not found")

    def update(self, data, new_data, collection=None):

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not data:
            raise NoDataException("Data is required")
        if not new_data:
            raise NoDataException("New data is required")
        collection = self.db.get_collection(collection)
        result = collection.update_one(data, new_data)

        if result.acknowledged:
            if result.modified_count > 0:
                return DataNotUpdatedException("No data to update")
            return True
        else:
            raise DataNotUpdatedException("Update failed")

    def delete(self, data, collection=None):

        if not collection:
            raise CollectionNotDefinedException("Collection is required")
        if not data:
            raise NoDataException("Data is required")

        collection = self.db.get_collection(collection)
        result = collection.delete_one(data)

        if result.acknowledged:
            if result.deleted_count > 0:
                return True
            raise DataNotDeletedException("No data to delete")
        else:
            raise DataNotDeletedException("Data not deleted")
