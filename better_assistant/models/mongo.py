from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from better_assistant.utils import get_kst_timezone

KST_TIMEZONE = get_kst_timezone()

class MongoFilter:
    def __init__(self):
        self.filter: Dict[str, Any] = {}

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

    def build(self) -> Dict[str, Any]:
        return self.filter

class MongoDocument(BaseModel):
    """MongoDB 문서 기본 구조"""
    id: Optional[str] = Field(None, alias="_id")
    created_at: datetime = Field(default_factory=datetime.now(KST_TIMEZONE))
    updated_at: datetime = Field(default_factory=datetime.now(KST_TIMEZONE))


    def _model_load(self, data: Dict[str, Any]):
        """dict를 MongoDocument로 변환"""
        return self.__class__(**data)

    def from_dict(self, data: Dict[str, Any]):
        """dict를 MongoDocument로 변환"""
        return self._model_load(data)

    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """MongoDB에 삽입하기 위한 dict로 변환"""
        return self.model_dump(by_alias=True, exclude_none=exclude_none)

    def update_timestamp(self):
        """updated_at 필드를 현재 시간으로 업데이트"""
        self.updated_at = datetime.now(KST_TIMEZONE)
