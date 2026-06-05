from fastapi import FastAPI

from app.agent.service import polish_paper
from app.core.config import get_settings
from app.schemas.polish import PolishRequest, PolishResponse

app = FastAPI(title="Paper Polish Agent API")


@app.get("/health")
def health() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": "paper-polish-agent",
        "env": settings.app_env,
    }


@app.post("/api/polish", response_model=PolishResponse)
def polish(request: PolishRequest) -> PolishResponse:
    return polish_paper(request)
