import os

from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()

origins = [os.getenv("ALLOW_ORIGIN")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """
    서버 상태 확인을 위한 헬스체크 API

    Returns:
        Response: 서버 상태 확인 결과
    """
    return Response(status_code=200)


@app.get("/projects")
async def fetch_projects():
    """
    프로젝트 목록 호출을 위한 API
    Returns:
        Response: 프로젝트 목록
    """
    pass

@app.get("/project")
async def fetch_project(project_id: str):
    """
    프로젝트 detail 호출을 위한 API

    Args:
        project_id (str): 프로젝트 ID

    Returns:
        Response: {project_id}에 해당하는 프로젝트 정보
    """
    # TODO: Implement project creation logic
    return JSONResponse(content={"project_id": project_id})

@app.post("/project")
async def create_project():
    """
    프로젝트 생성 API

    Returns:
        Response: 생성된 프로젝트 정보
    """
    # TODO: Implement project creation logic
    return JSONResponse(content={"project_id": "new_project_id"})

@app.put("/project")
async def update_project(project_id: str):
    """
    프로젝트 수정 API

    Returns:
        Response: 수정된 프로젝트 정보
    """
    # TODO: Implement project update logic
    return JSONResponse(content={"project_id": "updated_project_id"})

@app.delete("/project")
async def delete_project(project_id: str):
    """
    프로젝트 삭제 API

    Returns:
        Response: 삭제된 프로젝트 정보
    """
    # TODO: Implement project deletion logic
    return JSONResponse(content={"project_id": "deleted_project_id"})

@app.post("/prompt")
async def create_prompt(project_id: str):
    """
    프롬프트 생성 API

    Returns:
        Response: 생성된 프롬프트 정보
    """
    # TODO: Implement prompt creation logic
    return JSONResponse(content={"prompt_id": "new_prompt_id"})

@app.put("/prompt")
async def update_prompt(project_id: str, prompt_id: str):
    """
    프롬프트 수정 API

    Returns:
        Response: 수정된 프롬프트 정보
    """
    # TODO: Implement prompt update logic
    return JSONResponse(content={"prompt_id": "updated_prompt_id"})

@app.get("/dialog/{project_id}")
async def fetch_dialog(project_id: str, dialogId: str = Query(..., description="The ID of the dialog")):
    """
    대화 생성 API

    Returns:
        Response: 생성된 대화 정보
    """
    # TODO: Implement dialog creation logic
    if not project_id or not dialogId:
        raise HTTPException(status_code=400, detail="Invalid project_id or dialogId")
    return JSONResponse(content={"dialog_id": "new_dialog_id"})

@app.post("/dialog/{project_id}")
async def create_dialog(project_id: str):
    """
    대화 생성 API

    Returns:
        Response: 생성된 대화 정보
    """
    # TODO: Implement dialog creation logic
    if not project_id:
        raise HTTPException(status_code=400, detail="Invalid project_id")
    return JSONResponse(content={"dialog_id": "new_dialog_id"})

@app.put("/dialog/{project_id}")
async def update_dialog(project_id: str, dialogId: str = Query(..., description="The ID of the dialog")):
    """
    대화 수정 API

    Returns:
        Response: 수정된 대화 정보
    """
    # TODO: Implement dialog update logic
    if not project_id or not dialogId:
        raise HTTPException(status_code=400, detail="Invalid project_id or dialogId")
    return JSONResponse(content={"dialog_id": "updated_dialog_id"})

@app.delete("/dialog/{project_id}")
async def delete_dialog(project_id: str, dialogId: str = Query(..., description="The ID of the dialog")):
    """
    대화 삭제 API

    Returns:
        Response: 삭제된 대화 정보
    """
    # TODO: Implement dialog deletion logic
    if not project_id or not dialogId:
        raise HTTPException(status_code=400, detail="Invalid project_id or dialogId")
    return JSONResponse(content={"dialog_id": "deleted_dialog_id"})

@app.post("/generate/{dialog_id}")
async def generate_dialog(dialog_id: str, promptId: str = Query(..., description="The ID of the prompt")):
    """
    대화 생성 API

    Returns:
        Response: 생성된 대화 정보
    """
    # TODO: Implement dialog generation logic
    if not dialog_id or not promptId:
        raise HTTPException(status_code=400, detail="Invalid dialog_id or promptId")
    return StreamingResponse(content={"dialog_id": "new_dialog_id"})
