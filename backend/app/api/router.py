from typing import Annotated

from fastapi import APIRouter, Query, Request, status
from fastapi.responses import JSONResponse

from app.models import (
    HealthResponse,
    SearchErrorCode,
    SearchErrorResponse,
    SearchQueryParams,
    SearchRateLimitErrorResponse,
    SearchResponse,
)
from app.services import (
    AggregationProviderSelectionError,
    AggregationService,
    HealthService,
    SlidingWindowRateLimiter,
)

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


@api_router.get(
    "/search",
    response_model=SearchResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": SearchErrorResponse},
        status.HTTP_429_TOO_MANY_REQUESTS: {"model": SearchRateLimitErrorResponse},
    },
    summary="Aggregated marketplace search",
)
async def search(
    request: Request,
    params: Annotated[SearchQueryParams, Query()],
) -> JSONResponse:
    rate_limiter: SlidingWindowRateLimiter = request.app.state.search_rate_limiter
    client_key = request.client.host if request.client is not None else "unknown"
    rate_limit = await rate_limiter.check(client_key)
    if not rate_limit.allowed:
        retry_after = rate_limit.retry_after_seconds or 1
        error_response = SearchRateLimitErrorResponse(
            detail="Search rate limit exceeded",
            retry_after_seconds=retry_after,
        )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content=error_response.model_dump(mode="json"),
            headers={"Retry-After": str(retry_after)},
        )

    aggregation_service: AggregationService = request.app.state.aggregation_service

    try:
        response = await aggregation_service.search(params.to_aggregation_request())
    except AggregationProviderSelectionError as exc:
        error_response = SearchErrorResponse(
            error_code=SearchErrorCode.UNKNOWN_PLATFORM,
            detail=str(exc),
            unknown_platforms=exc.unknown_platforms,
        )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=error_response.model_dump(mode="json"),
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=SearchResponse.from_aggregation_response(response).model_dump(mode="json"),
    )
