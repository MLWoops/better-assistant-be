from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from better_assistant.utils import get_kst_timezone

KST_TIMEZONE = get_kst_timezone()

class MongoFilter:
    def __init__(self):
        self.filter: Dict[str, Any] = {}
        self.projection: Dict[str, Any] = {"_id": 0}

    def equals(self, field: str, value: Any) -> "MongoFilter":
        self.filter[field] = value
        return self

    def not_equals(self, field: str, value: Any) -> "MongoFilter":
        self.filter[field] = {"$ne": value}
        return self

    def greater_than(self, field: str, value: Any) -> "MongoFilter":
        self.filter[field] = {"$gt": value}
        return self

    def less_than(self, field: str, value: Any) -> "MongoFilter":
        self.filter[field] = {"$lt": value}
        return self

    def in_list(self, field: str, values: list) -> "MongoFilter":
        self.filter[field] = {"$in": values}
        return self

    def not_in_list(self, field: str, values: list) -> "MongoFilter":
        self.filter[field] = {"$nin": values}
        return self

    def exists(self, field: str, value: bool = True) -> "MongoFilter":
        self.filter[field] = {"$exists": value}
        return self

    def regex(self, field: str, pattern: str) -> "MongoFilter":
        self.filter[field] = {"$regex": pattern}
        return self

    def fields(self, include: list[str] = None, exclude: list[str] = None) -> "MongoFilter":
        """
        Specify which fields to include or exclude in the result.
        - `include`: List of fields to include (set to 1).
        - `exclude`: List of fields to exclude (set to 0).
        """
        if include:
            for field in include:
                self.projection[field] = 1
        if exclude:
            for field in exclude:
                self.projection[field] = 0
        return self

    def build_with_projection(self) -> Dict[str, Dict[str, Any]]:
        return {"filter": self.filter, "projection": self.projection}
    def build(self) -> Dict[str, Any]:
        return self.filter


class MongoUpdate:
    def __init__(self):
        self.update: Dict[str, Any] = {}

    def set(self, field: str, value: Any) -> "MongoUpdate":
        if "$set" not in self.update:
            self.update["$set"] = {}
        self.update["$set"][field] = value
        return self

    def unset(self, field: str) -> "MongoUpdate":
        if "$unset" not in self.update:
            self.update["$unset"] = {}
        self.update["$unset"][field] = ""
        return self

    def increment(self, field: str, value: int) -> "MongoUpdate":
        if "$inc" not in self.update:
            self.update["$inc"] = {}
        self.update["$inc"][field] = value
        return self

    def push(self, field: str, value: Any) -> "MongoUpdate":
        if "$push" not in self.update:
            self.update["$push"] = {}
        self.update["$push"][field] = value
        return self

    def push_all(self, field: str, values: list) -> "MongoUpdate":
        if "$push" not in self.update:
            self.update["$push"] = {}
        self.update["$push"][field]["$each"] = values
        return self

    def add_to_set(self, field: str, value: Any) -> "MongoUpdate":
        if "$addToSet" not in self.update:
            self.update["$addToSet"] = {}
        self.update["$addToSet"][field] = value
        return self

    def remove_from_array(self, field: str, value: Any) -> "MongoUpdate":
        if "$pull" not in self.update:
            self.update["$pull"] = {}
        self.update["$pull"][field] = value
        return self

    def set_updated_at(self) -> "MongoUpdate":
        return self.set("updated_at", datetime.now(KST_TIMEZONE))

    def build(self) -> Dict[str, Any]:
        return self.update

class MongoDocument(BaseModel):
    """MongoDB 문서 기본 구조"""
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(KST_TIMEZONE))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(KST_TIMEZONE))

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MongoDocument":
        """dict를 MongoDocument로 변환"""
        return cls(**data)

    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """MongoDB에 삽입하기 위한 dict로 변환"""
        data = self.model_dump(by_alias=True, exclude_none=exclude_none)
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
        return data

    def update_timestamp(self):
        """updated_at 필드를 현재 시간으로 업데이트"""
        self.updated_at = datetime.now(KST_TIMEZONE)
