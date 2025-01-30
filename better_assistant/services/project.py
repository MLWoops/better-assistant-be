from datetime import datetime
from typing import Dict, List

from bson import ObjectId

from better_assistant.models import MongoFilter, MongoUpdate, Project
from better_assistant.utils import MongoClientWrapper


class ProjectService:
    def __init__(self, mongo_client: MongoClientWrapper):
        self.mongo_client = mongo_client

    async def get_projects(self) -> List[Dict[str, any]]:
        filter_obj = (
            MongoFilter()
            .exists("project_title")
            .fields(["project_title", "updated_at", "_id"])
            .build_with_projection()
            )
        result: List[Dict[str, any]] = await self.mongo_client.find(filter_obj, collection_name="projects")

        for data in result:
            for key, value in data.items():
                if isinstance(value, datetime):
                    data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(value, ObjectId):
                    data[key] = value.__str__()
        return result

    async def get_project(self, project_id: str) -> dict:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(project_id))
            .fields(["project_title", "updated_at"])
            .build_with_projection()
            )
        result = await self.mongo_client.find(filter_obj, collection_name="projects")
        return Project.from_dict(data=result[0]).to_dict()

    async def create_project(self, project: Project) -> ObjectId:
        return await self.mongo_client.insert(project, "projects")

    async def update_project(self, project_id: str, project: Project) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(project_id))
            .build()
            )
        update_obj = (
            MongoUpdate()
            .set("project_title", project.project_title)
            .set_updated_at()
            .build()
        )
        return await self.mongo_client.update(filter_obj, update_obj, collection_name="projects")

    async def delete_project(self, project_id: str) -> bool:
        filter_obj = (
            MongoFilter()
            .equals("_id", ObjectId(project_id))
            .build()
            )
        return await self.mongo_client.delete(filter_obj, collection_name="projects")
