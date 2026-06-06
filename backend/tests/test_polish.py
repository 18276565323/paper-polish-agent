import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.main as main
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.schemas.polish import PolishRequest, PolishResponse


@pytest.fixture()
def client_with_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


def test_polish_endpoint_returns_fixed_json_contract(monkeypatch, client_with_db) -> None:
    def fake_polish_paper(request: PolishRequest) -> PolishResponse:
        return PolishResponse(
            original_text=request.text,
            polish_text="润色后文本",
            optimize_dimension=request.requirement,
            modify_detail="修改说明",
            remaining_problem="后续建议",
            ai_learning_knowledge="知识点",
            practical_operation_points="实操要点",
            project_resume_highlight="简历亮点",
        )

    monkeypatch.setattr(main, "polish_paper", fake_polish_paper)

    response = client_with_db.post(
        "/api/polish",
        json={
            "text": "本文提出了一种方法，该方法可以提高系统性能。",
            "requirement": "学术化润色",
        },
    )

    assert response.status_code == 200
    assert response.json()["polish_text"] == "润色后文本"

    tasks_response = client_with_db.get("/api/tasks")
    assert tasks_response.status_code == 200
    tasks = tasks_response.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "success"
    assert tasks[0]["requirement"] == "学术化润色"
    assert tasks[0]["model_name"] != ""


def test_polish_endpoint_records_failed_task(monkeypatch, client_with_db) -> None:
    def fake_polish_paper(request: PolishRequest) -> PolishResponse:
        raise RuntimeError("模型调用失败")

    monkeypatch.setattr(main, "polish_paper", fake_polish_paper)

    response = client_with_db.post(
        "/api/polish",
        json={
            "text": "本文提出了一种方法，该方法可以提高系统性能。",
            "requirement": "学术化润色",
        },
    )

    assert response.status_code == 500
    assert response.json()["detail"] == "模型调用失败"

    tasks_response = client_with_db.get("/api/tasks")
    tasks = tasks_response.json()
    assert len(tasks) == 1
    assert tasks[0]["status"] == "failed"


def test_get_task_detail_returns_saved_task(monkeypatch, client_with_db) -> None:
    def fake_polish_paper(request: PolishRequest) -> PolishResponse:
        return PolishResponse(
            original_text=request.text,
            polish_text="润色后文本",
            optimize_dimension=request.requirement,
            modify_detail="修改说明",
            remaining_problem="后续建议",
            ai_learning_knowledge="知识点",
            practical_operation_points="实操要点",
            project_resume_highlight="简历亮点",
        )

    monkeypatch.setattr(main, "polish_paper", fake_polish_paper)
    client_with_db.post(
        "/api/polish",
        json={"text": "原文", "requirement": "综合润色"},
    )
    task_id = client_with_db.get("/api/tasks").json()[0]["id"]

    response = client_with_db.get(f"/api/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["result_json"]["polish_text"] == "润色后文本"
