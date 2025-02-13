from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from better_assistant.models.mongo import MongoDocument
from better_assistant.utils import get_kst_timezone

KST_TIMEZONE = get_kst_timezone()

class Project(MongoDocument):
    project_title: str = Field(..., description="프로젝트 제목")
    created_at: Optional[datetime] = Field(description="프로젝트 생성 시각", default=datetime.now(KST_TIMEZONE))
    updated_at: Optional[datetime] = Field(description="프로젝트 수정 시각", default=datetime.now(KST_TIMEZONE))

class Prompt(MongoDocument):
    project_id: str = Field(..., description="프로젝트 ID")
    prompt_version: str = Field(..., description="프롬프트 버전")
    prompt_content: str = Field(..., description="프롬프트 내용")
    created_at: Optional[datetime] = Field(description="프롬프트 생성 시각", default=datetime.now(KST_TIMEZONE))
    updated_at: Optional[datetime] = Field(description="프롬프트 수정 시각", default=datetime.now(KST_TIMEZONE))

class Msg(BaseModel):
    content: str = Field(..., description="메시지")
    role: str = Field(..., description="역할")

class Dialog(MongoDocument):
    project_id: str = Field(..., description="프로젝트 ID")
    dialog_title: str = Field(..., description="대화 제목")
    dialog_content: list[Msg] = Field(..., description="대화 내용")
    created_at: Optional[datetime] = Field(description="대화 생성 시각", default=datetime.now(KST_TIMEZONE))
    updated_at: Optional[datetime] = Field(description="대화 수정 시각", default=datetime.now(KST_TIMEZONE))

class GenerateRequest(BaseModel):
    dialog_id: str = Field(..., description="대화 ID")
    messages: list[Msg] = Field(..., description="메시지 리스트, 사용자 입력 포함")
    user_input: str = Field(..., description="사용자 입력")
