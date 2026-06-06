from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import PolishTask
from app.schemas.polish import PolishResponse


def create_task(
    *,
    session: Session,
    input_text: str,
    requirement: str,
    model_name: str,
    prompt_version: str,
) -> PolishTask:
    task = PolishTask(
        input_text=input_text,
        requirement=requirement,
        status="running",
        model_name=model_name,
        prompt_version=prompt_version,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def finish_task_success(session: Session, task: PolishTask, response: PolishResponse) -> PolishTask:
    task.status = "success"
    task.result_json = response.model_dump()
    task.error_message = None
    task.completed_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(task)
    return task


def finish_task_failure(session: Session, task: PolishTask, error_message: str) -> PolishTask:
    task.status = "failed"
    task.error_message = error_message
    task.completed_at = datetime.now(timezone.utc)
    session.commit()
    session.refresh(task)
    return task


def list_tasks(session: Session, limit: int = 20) -> list[PolishTask]:
    statement = select(PolishTask).order_by(PolishTask.created_at.desc()).limit(limit)
    return list(session.scalars(statement))


def get_task(session: Session, task_id: int) -> Optional[PolishTask]:
    return session.get(PolishTask, task_id)
