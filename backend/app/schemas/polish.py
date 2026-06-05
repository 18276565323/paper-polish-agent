from pydantic import BaseModel, Field


class PolishRequest(BaseModel):
    text: str = Field(min_length=1, description="论文原文或段落")
    requirement: str = Field(default="综合润色", description="润色需求")


class PolishResponse(BaseModel):
    original_text: str
    polish_text: str
    optimize_dimension: str
    modify_detail: str
    remaining_problem: str
    ai_learning_knowledge: str
    practical_operation_points: str
    project_resume_highlight: str
