from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.repositories.tasks import create_task, finish_task_failure, finish_task_success
from app.schemas.polish import PolishResponse


def make_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()


def test_create_and_finish_success_task() -> None:
    session = make_session()
    response = PolishResponse(
        original_text="原文",
        polish_text="润色后",
        optimize_dimension="学术化润色",
        modify_detail="修改说明",
        remaining_problem="后续建议",
        ai_learning_knowledge="知识点",
        practical_operation_points="实操要点",
        project_resume_highlight="简历亮点",
    )

    task = create_task(
        session=session,
        input_text="原文",
        requirement="学术化润色",
        model_name="gpt-5.5",
        prompt_version="paper_polish_v1",
    )
    finished = finish_task_success(session, task, response)

    assert finished.id == task.id
    assert finished.status == "success"
    assert finished.result_json["polish_text"] == "润色后"
    assert finished.completed_at is not None


def test_create_and_finish_failed_task() -> None:
    session = make_session()

    task = create_task(
        session=session,
        input_text="原文",
        requirement="学术化润色",
        model_name="gpt-5.5",
        prompt_version="paper_polish_v1",
    )
    finished = finish_task_failure(session, task, "模型调用失败")

    assert finished.status == "failed"
    assert finished.error_message == "模型调用失败"
    assert finished.completed_at is not None
