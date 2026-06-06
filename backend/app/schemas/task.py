from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TaskSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    requirement: str
    status: str
    model_name: str
    prompt_version: str
    created_at: datetime
    completed_at: Optional[datetime] = None


class TaskDetail(TaskSummary):
    input_text: str
    result_json: Optional[dict] = None
    error_message: Optional[str] = None
