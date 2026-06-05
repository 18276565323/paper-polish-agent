from app.providers.modelgate import call_modelgate
from app.schemas.polish import PolishRequest, PolishResponse


def polish_paper(request: PolishRequest) -> PolishResponse:
    return call_modelgate(request)
