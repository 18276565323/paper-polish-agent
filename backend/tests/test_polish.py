from fastapi.testclient import TestClient

import app.main as main
from app.main import app
from app.schemas.polish import PolishRequest, PolishResponse


def test_polish_endpoint_returns_fixed_json_contract(monkeypatch) -> None:
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
    client = TestClient(app)

    response = client.post(
        "/api/polish",
        json={
            "text": "本文提出了一种方法，该方法可以提高系统性能。",
            "requirement": "学术化润色",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "original_text": "本文提出了一种方法，该方法可以提高系统性能。",
        "polish_text": "润色后文本",
        "optimize_dimension": "学术化润色",
        "modify_detail": "修改说明",
        "remaining_problem": "后续建议",
        "ai_learning_knowledge": "知识点",
        "practical_operation_points": "实操要点",
        "project_resume_highlight": "简历亮点",
    }
