from fastapi import APIRouter, Request, status
from fastapi.responses import JSONResponse

from app.models import HealthResponse
from app.services import HealthService

api_router = APIRouter()


@api_router.get(
    "/health",
    response_model=HealthResponse,
    summary="Runtime health check",
)
async def healthcheck(request: Request) -> JSONResponse:
    health_service: HealthService = request.app.state.health_service
    response = await health_service.get_health()
    status_code = status.HTTP_200_OK if response.is_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(mode="json"),
    )
