import json
from typing import Any

from openai import OpenAI

from app.agent.prompt import AGENT_SYSTEM_PROMPT, build_user_prompt
from app.core.config import get_settings
from app.schemas.polish import PolishRequest, PolishResponse

POLISH_RESPONSE_FIELDS = (
    "original_text",
    "polish_text",
    "optimize_dimension",
    "modify_detail",
    "remaining_problem",
    "ai_learning_knowledge",
    "practical_operation_points",
    "project_resume_highlight",
)


def _normalize_text_field(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)


def _normalize_polish_payload(data: dict[str, Any]) -> dict[str, str]:
    return {field: _normalize_text_field(data.get(field, "")) for field in POLISH_RESPONSE_FIELDS}


def call_modelgate(request: PolishRequest) -> PolishResponse:
    settings = get_settings()
    if not settings.modelgate_api_key:
        raise RuntimeError("MODELGATE_API_KEY is missing. Create backend/.env first.")
    if not settings.modelgate_model:
        raise RuntimeError("MODELGATE_MODEL is missing. Fill in the exact ModelGate model id.")

    client = OpenAI(
        api_key=settings.modelgate_api_key,
        base_url=settings.modelgate_base_url,
    )

    completion = client.chat.completions.create(
        model=settings.modelgate_model,
        temperature=0.2,
        messages=[
            {"role": "system", "content": AGENT_SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(request.text, request.requirement)},
        ],
    )

    content = completion.choices[0].message.content or "{}"
    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        raise RuntimeError("ModelGate returned non-JSON content.") from exc

    normalized_data = _normalize_polish_payload(data)
    return PolishResponse(**normalized_data)
