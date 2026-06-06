from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.agent.service import polish_paper
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine, get_db
from app.models.task import PolishTask
from app.repositories.tasks import (
    create_task,
    finish_task_failure,
    finish_task_success,
    get_task,
    list_tasks,
)
from app.schemas.polish import PolishRequest, PolishResponse
from app.schemas.task import TaskDetail, TaskSummary

PROMPT_VERSION = "paper_polish_v1"

app = FastAPI(title="Paper Polish Agent API")


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "paper-polish-agent",
        "env": settings.app_env,
    }


@app.post("/api/polish", response_model=PolishResponse)
def polish(request: PolishRequest, db: Session = Depends(get_db)) -> PolishResponse:
    settings = get_settings()
    task = create_task(
        session=db,
        input_text=request.text,
        requirement=request.requirement,
        model_name=settings.modelgate_model or "unknown",
        prompt_version=PROMPT_VERSION,
    )

    try:
        response = polish_paper(request)
    except Exception as exc:
        finish_task_failure(db, task, str(exc))
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    finish_task_success(db, task, response)
    return response


@app.get("/api/tasks", response_model=list[TaskSummary])
def tasks(limit: int = 20, db: Session = Depends(get_db)) -> list[PolishTask]:
    safe_limit = min(max(limit, 1), 100)
    return list_tasks(db, safe_limit)


@app.get("/api/tasks/{task_id}", response_model=TaskDetail)
def task_detail(task_id: int, db: Session = Depends(get_db)) -> PolishTask:
    task = get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
