import os
from contextlib import asynccontextmanager

from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from loguru import logger

from better_assistant.exceptions import (
    CollectionNotDefinedException,
    DataNotCreatedException,
    DataNotFoundException,
    NoDataException,
    NoFilterException,
)
from better_assistant.models import Project, Prompt
from better_assistant.services import ProjectService, PromptService
from better_assistant.utils import MongoClientWrapper

mongo_client: MongoClientWrapper = None
project_service: ProjectService = None
prompt_service: PromptService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    서버 시작 시 초기화 작업을 위한 함수
    """
    global project_service, prompt_service, mongo_client
    mongo_client = MongoClientWrapper()
    await mongo_client.__create_index__()

    project_service = ProjectService(mongo_client)
    prompt_service = PromptService(mongo_client)

    logger.add("app.log", rotation="500 MB", format="{time} {level} {message}", level="DEBUG", enqueue=True)

    yield

app = FastAPI(lifespan=lifespan)

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
    try:
        result = await project_service.get_projects()
        return JSONResponse({"projects": result})
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except DataNotFoundException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=404, content="No data found.")

@app.get("/project")
async def fetch_project(projectId: str):
    """
    프로젝트 detail 호출을 위한 API

    Args:
        project_id (str): 프로젝트 ID

    Returns:
        Response: {project_id}에 해당하는 프로젝트 정보
    """
    try:
        project_result: dict = await project_service.get_project(projectId)
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except DataNotFoundException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=404, content=f"No data found in requested project id: {projectId}.")

    try:
        prompt_result: list = await prompt_service.get_prompts(project_id=projectId)
        project_result["prompts"] = prompt_result
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except DataNotFoundException:
        project_result["prompts"] = []
    return JSONResponse({"project_detail": project_result})


@app.post("/project")
async def create_project(new_project: Project):
    """
    프로젝트 생성 API

    Returns:
        Response: 생성된 프로젝트 정보
    """
    try:
        result: ObjectId = await project_service.create_project(new_project)
        return JSONResponse({"project_id": str(result)})
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except DataNotCreatedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")

@app.put("/project")
async def update_project(projectId: str, updated_project: Project):
    """
    프로젝트 수정 API

    Returns:
        Response: 수정된 프로젝트 정보
    """
    try:
        await project_service.update_project(projectId, updated_project)
        return Response()
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoDataException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=422, content="No data to update.")
    except DataNotFoundException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=404, content="No data found to update.")

@app.delete("/project")
async def delete_project(projectId: str):
    """
    프로젝트 삭제 API

    Returns:
        Response: 삭제된 프로젝트 정보
    """
    try:
        await project_service.delete_project(projectId)
        return Response()
    except CollectionNotDefinedException:
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException:
        return Response(status_code=500, content="Contect to administator.")
    except DataNotFoundException:
        return Response(status_code=404, content="No data found to delete.")

@app.get("/prompts/{projectId}")
async def create_prompt(projectId: str):
    """
    프롬프트 목록 호출 API

    Returns:
        Response: 프롬프트 목록
    """
    try:
        result = await prompt_service.get_prompts(project_id=projectId)
        return JSONResponse(content={"prompts": result})
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except DataNotFoundException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=404, content="No data found.")

@app.post("/prompt")
async def create_prompt(prompt: Prompt):
    """
    프롬프트 생성 API

    Returns:
        Response: 생성된 프롬프트 정보
    """
    try:
        result: ObjectId = await prompt_service.create_prompt(prompt)
        return JSONResponse(content={"prompt_id": str(result)})
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except DataNotCreatedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")

@app.put("/prompt")
async def update_prompt(promptId: str, prompt: Prompt):
    """
    프롬프트 수정 API

    Returns:
        Response: 수정된 프롬프트 정보
    """
    try:
        await prompt_service.update_prompt(promptId, prompt)
        return Response()
    except CollectionNotDefinedException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=500, content="Contect to administator.")
    except NoDataException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=422, content="No data to update.")
    except DataNotFoundException as e:
        logger.error(f"An error occurred: {str(e)}")
        return Response(status_code=404, content="No data found to update.")

@app.delete("/prompt")
async def delete_prompt(promptId: str):
    """
    프롬프트 삭제 API

    Returns:
        Response: 삭제된 프롬프트 정보
    """
    try:
        await prompt_service.delete_prompt(promptId)
        return Response()
    except CollectionNotDefinedException:
        return Response(status_code=500, content="Contect to administator.")
    except NoFilterException:
        return Response(status_code=500, content="Contect to administator.")
    except DataNotFoundException:
        return Response(status_code=404, content="No data found to delete.")

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
