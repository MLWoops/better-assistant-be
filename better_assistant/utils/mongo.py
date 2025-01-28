import os
from typing import Dict, List

from bson import ObjectId
from pymongo import AsyncMongoClient
from pymongo.errors import ServerSelectionTimeoutError
from pymongo.server_api import ServerApi

from better_assistant.exceptions import (
    CollectionNotDefinedException,
    DataNotCreatedException,
    DataNotFoundException,
    NoDataException,
    NoFilterException,
)


class MongoClientWrapper:
    def __init__(self):
        mongo_host = os.getenv("MONGO_HOST_NAME")
        mongo_user = os.getenv("MONGO_USER")
        mongo_pass = os.getenv("MONGO_PASS")
        mongo_db = os.getenv("MONGO_DB_NAME")

        uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@{mongo_host}/?retryWrites=true&w=majority&appName=MLWoops"

        print(f"Connecting to MongoDB: {mongo_host}")

        self.client = AsyncMongoClient(
            uri,
            server_api=ServerApi('1'),
            )
        self.db = self.client.get_database(mongo_db)

    async def __create_index__(self):
        print("Creating indexes...")
        try:
            await self.db.get_collection("projects").create_index("project_title", unique=True, background=True)
            await self.db.get_collection("prompts").create_index("prompt_version", unique=True, background=True)
            # await self.db.get_collection("dialogs").create_index("dialog_title", unique=True, background=True)
        except ServerSelectionTimeoutError:
            print("Failed to create indexes. Collection might not exist yet.")

    async def insert(self, document: "MongoDocument", collection_name: str=None) -> ObjectId: # noqa

        if not collection_name:
            raise CollectionNotDefinedException("Collection is required")
        if not document:
            raise NoFilterException("Data is required")
        collection = self.db.get_collection(collection_name)

        document = document.to_dict()

        result = await collection.insert_one(document)

        if result.acknowledged:
            return result.inserted_id

        raise DataNotCreatedException("Data not created")


    async def find(self, filter: Dict[str, Dict[str, any]], collection_name: str=None) -> List:

        if not collection_name:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")
        collection = self.db.get_collection(collection_name)

        cursor = collection.find(filter=filter["filter"], projection=filter["projection"])
        result = await cursor.to_list(length=None)

        if result and len(result) > 0:
            return result
        raise DataNotFoundException(f"No data found for filter: {filter} in collection: {collection_name}")


    async def update(self, filter: Dict[str, any], update: Dict[str, any], collection_name: str=None) -> bool:

        if not collection_name:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")
        if not update:
            raise NoDataException("New data is required")
        collection = self.db.get_collection(collection_name)
        result = await collection.update_one(filter, update)

        if result.acknowledged:
            if result.modified_count > 0:
                return True
        raise DataNotFoundException(f"No data found for filter: {filter} in collection: {collection_name}")


    async def delete(self, filter: Dict[str, any], collection_name: str=None) -> bool:

        if not collection_name:
            raise CollectionNotDefinedException("Collection is required")
        if not filter:
            raise NoFilterException("Data is required")

        collection = self.db.get_collection(collection_name)
        result = await collection.delete_one(filter)

        if result.acknowledged:
            if result.deleted_count > 0:
                return True
        raise DataNotFoundException(f"No data found for filter: {filter} in collection: {collection_name}")
