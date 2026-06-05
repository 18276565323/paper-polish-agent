from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.schemas.polish import PolishRequest


def test_call_modelgate_parses_model_json_response(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.config import Settings
    import app.providers.modelgate as modelgate

    fake_settings = Settings(
        modelgate_api_key="test-key",
        modelgate_base_url="https://mg.aid.pub/v1",
        modelgate_model="gpt-5.5",
    )
    monkeypatch.setattr(modelgate, "get_settings", lambda: fake_settings)

    completion = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=(
                        '{"original_text":"原文","polish_text":"润色后",'
                        '"optimize_dimension":"学术化润色",'
                        '"modify_detail":"修改说明",'
                        '"remaining_problem":"后续建议",'
                        '"ai_learning_knowledge":"知识点",'
                        '"practical_operation_points":"实操要点",'
                        '"project_resume_highlight":"简历亮点"}'
                    )
                )
            )
        ]
    )
    create_mock = Mock(return_value=completion)
    openai_client = Mock()
    openai_client.chat.completions.create = create_mock
    openai_class = Mock(return_value=openai_client)
    monkeypatch.setattr(modelgate, "OpenAI", openai_class)

    response = modelgate.call_modelgate(
        PolishRequest(text="原文", requirement="学术化润色")
    )

    openai_class.assert_called_once_with(
        api_key="test-key",
        base_url="https://mg.aid.pub/v1",
    )
    create_mock.assert_called_once()
    call_kwargs = create_mock.call_args.kwargs
    assert call_kwargs["model"] == "gpt-5.5"
    assert call_kwargs["temperature"] == 0.2
    assert call_kwargs["messages"][0]["role"] == "system"
    assert call_kwargs["messages"][1]["role"] == "user"
    assert "学术化润色" in call_kwargs["messages"][1]["content"]
    assert "原文" in call_kwargs["messages"][1]["content"]
    assert response.polish_text == "润色后"


def test_call_modelgate_requires_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.config import Settings
    import app.providers.modelgate as modelgate

    fake_settings = Settings(
        modelgate_api_key="",
        modelgate_base_url="https://mg.aid.pub/v1",
        modelgate_model="gpt-5.5",
    )
    monkeypatch.setattr(modelgate, "get_settings", lambda: fake_settings)

    with pytest.raises(RuntimeError, match="MODELGATE_API_KEY is missing"):
        modelgate.call_modelgate(PolishRequest(text="原文", requirement="学术化润色"))
