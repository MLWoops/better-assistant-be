from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field


class Project(BaseModel):
    project_id: str = Field(..., description="프로젝트 ID", default=str(ObjectId()))
    project_title: str = Field(..., description="프로젝트 제목")
    created_at: datetime = Field(..., description="프로젝트 생성 시각", default=datetime.now())
    updated_at: datetime = Field(..., description="프로젝트 수정 시각", default=datetime.now())

class Prompt(BaseModel):
    prompt_id: str = Field(..., description="프롬프트 ID", default=str(ObjectId()))
    project_id: str = Field(..., description="프로젝트 ID")
    prompt_version: str = Field(..., description="프롬프트 버전")
    prompt_content: str = Field(..., description="프롬프트 내용")
    created_at: datetime = Field(..., description="프롬프트 생성 시각", default=datetime.now())
    updated_at: datetime = Field(..., description="프롬프트 수정 시각", default=datetime.now())

class Msg(BaseModel):
    msg: str = Field(..., description="메시지")
    role: str = Field(..., description="역할")

class Dialog(BaseModel):
    project_id: str = Field(..., description="프로젝트 ID")
    dialog_id: str = Field(..., description="대화 ID", default=str(ObjectId()))
    dialog_content: list[Msg] = Field(..., description="대화 내용")
    created_at: datetime = Field(..., description="대화 생성 시각", default=datetime.now())
    updated_at: datetime = Field(..., description="대화 수정 시각", default=datetime.now())
