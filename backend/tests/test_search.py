from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.main import create_app
from app.providers import SearchRequest, SearchResult
from app.services import (
    AggregationMetrics,
    AggregationProviderFailure,
    AggregationProviderSelectionError,
    AggregationRequest,
    AggregationResponse,
    SearchSortOption,
)


def test_search_endpoint_returns_200_with_aggregated_results(
    monkeypatch,
) -> None:
    app = create_app()
    expected_response = AggregationResponse(
        results=(
            SearchResult(
                id="ebay:1",
                external_id="1",
                title="RTX 3090",
                price=899.0,
                currency="EUR",
                platform="ebay",
                url="https://example.com/items/1",
            ),
        ),
        failures=(
            AggregationProviderFailure(
                provider_name="SubitoProvider",
                platform="subito",
                error_type="ProviderUnavailableError",
                message="SubitoProvider is temporarily unavailable",
            ),
        ),
        metrics=AggregationMetrics(
            provider_count=2,
            successful_provider_count=1,
            failed_provider_count=1,
            raw_result_count=1,
            normalized_result_count=1,
            filtered_result_count=1,
            final_result_count=1,
            duration_ms=12.5,
        ),
    )

    with TestClient(app) as client:
        search_mock = AsyncMock(return_value=expected_response)
        monkeypatch.setattr(app.state.aggregation_service, "search", search_mock)

        response = client.get(
            "/search",
            params=[
                ("query", "  RTX   3090  "),
                ("page", "2"),
                ("page_size", "10"),
                ("platforms", " ebay "),
                ("platforms", "subito"),
                ("min_price", "500"),
                ("max_price", "1200"),
                ("sort", "price_asc"),
            ],
        )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "id": "ebay:1",
                "external_id": "1",
                "title": "RTX 3090",
                "description": None,
                "price": 899.0,
                "currency": "EUR",
                "platform": "ebay",
                "location": None,
                "url": "https://example.com/items/1",
                "image_url": None,
                "seller_name": None,
                "seller_rating": None,
                "condition": None,
                "published_at": None,
                "collected_at": response.json()["results"][0]["collected_at"],
                "relevance_score": 0.0,
            }
        ],
        "failures": [
            {
                "provider_name": "SubitoProvider",
                "platform": "subito",
                "error_type": "ProviderUnavailableError",
                "message": "SubitoProvider is temporarily unavailable",
            }
        ],
        "metrics": {
            "provider_count": 2,
            "successful_provider_count": 1,
            "failed_provider_count": 1,
            "raw_result_count": 1,
            "normalized_result_count": 1,
            "filtered_result_count": 1,
            "final_result_count": 1,
            "duration_ms": 12.5,
        },
    }
    search_mock.assert_awaited_once_with(
        AggregationRequest(
            search=SearchRequest(query="RTX 3090", page=2, page_size=10),
            platforms=[" ebay ", "subito"],
            min_price=500.0,
            max_price=1200.0,
            sort=SearchSortOption.PRICE_ASC,
        )
    )


def test_search_endpoint_returns_400_for_unknown_platform(
    monkeypatch,
) -> None:
    app = create_app()

    with TestClient(app) as client:
        monkeypatch.setattr(
            app.state.aggregation_service,
            "search",
            AsyncMock(side_effect=AggregationProviderSelectionError(("wallapop",))),
        )
        response = client.get("/search", params={"query": "RTX 3090", "platforms": "wallapop"})

    assert response.status_code == 400
    assert response.json() == {
        "error_code": "unknown_platform",
        "detail": "Unknown provider platforms requested: wallapop",
        "unknown_platforms": ["wallapop"],
    }


def test_search_endpoint_returns_422_for_invalid_price_range() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get(
            "/search",
            params={
                "query": "RTX 3090",
                "min_price": "900",
                "max_price": "800",
            },
        )

    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, min_price cannot be greater than max_price"
    )


def test_search_endpoint_returns_422_for_blank_query() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/search", params={"query": "   "})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, query cannot be blank"


def test_search_endpoint_returns_422_for_unknown_sort() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/search", params={"query": "RTX 3090", "sort": "price_desc"})

    assert response.status_code == 422
    assert "relevance" in response.json()["detail"][0]["msg"]
    assert "price_asc" in response.json()["detail"][0]["msg"]


def test_search_endpoint_is_exposed_in_openapi_schema() -> None:
    app = create_app()

    with TestClient(app) as client:
        response = client.get("/openapi.json")

    assert response.status_code == 200
    search_operation = response.json()["paths"]["/search"]["get"]
    assert search_operation["summary"] == "Aggregated marketplace search"
    sort_parameter = next(
        parameter for parameter in search_operation["parameters"] if parameter["name"] == "sort"
    )
    assert sort_parameter["schema"]["default"] == SearchSortOption.RELEVANCE.value
    assert search_operation["responses"]["200"]["description"] == "Successful Response"
    assert search_operation["responses"]["400"]["description"] == "Bad Request"
