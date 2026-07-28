from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from pydantic import ValidationError
from redis.exceptions import ConnectionError as RedisConnectionError

from app.core.config import Settings
from app.providers import SearchRequest, SearchResult
from app.services import (
    AggregationMetrics,
    AggregationRequest,
    AggregationResponse,
    RedisSearchCache,
    SearchCacheKeyBuilder,
    SearchSortOption,
)


def test_search_cache_key_is_stable_for_equivalent_normalized_requests() -> None:
    key_builder = SearchCacheKeyBuilder()
    first = AggregationRequest(
        search=SearchRequest(query="  RTX   3090  ", page=2, page_size=10),
        platforms=[" EBAY ", "subito", "ebay"],
        min_price=500,
        max_price=1200,
        sort=SearchSortOption.PRICE_ASC,
    )
    second = AggregationRequest(
        search=SearchRequest(query="RTX 3090", page=2, page_size=10),
        platforms=("ebay", "subito"),
        min_price=500.0,
        max_price=1200.0,
        sort=SearchSortOption.PRICE_ASC,
    )

    assert key_builder.build(first) == key_builder.build(second)
    assert key_builder.build(first).startswith("search:v1:")
    assert len(key_builder.build(first)) == len("search:v1:") + 64


def test_search_cache_key_includes_query_filters_pagination_and_sort() -> None:
    key_builder = SearchCacheKeyBuilder()
    base = AggregationRequest(search=SearchRequest(query="RTX 3090"))
    variants = (
        AggregationRequest(search=SearchRequest(query="RTX 3080")),
        AggregationRequest(search=SearchRequest(query="RTX 3090", page=2)),
        AggregationRequest(search=SearchRequest(query="RTX 3090", page_size=50)),
        AggregationRequest(
            search=SearchRequest(query="RTX 3090"),
            platforms=("ebay",),
        ),
        AggregationRequest(search=SearchRequest(query="RTX 3090"), min_price=100),
        AggregationRequest(search=SearchRequest(query="RTX 3090"), max_price=1000),
        AggregationRequest(
            search=SearchRequest(query="RTX 3090"),
            sort=SearchSortOption.PRICE_ASC,
        ),
    )

    base_key = key_builder.build(base)

    assert all(key_builder.build(variant) != base_key for variant in variants)
    assert len({key_builder.build(variant) for variant in variants}) == len(variants)


def test_search_cache_ttl_defaults_to_five_minutes_and_must_be_positive() -> None:
    assert Settings().search_cache_ttl_seconds == 300

    with pytest.raises(ValidationError):
        Settings(search_cache_ttl_seconds=0)


@pytest.fixture
def aggregation_request() -> AggregationRequest:
    return AggregationRequest(
        search=SearchRequest(query="RTX 3090"),
        platforms=("ebay",),
    )


@pytest.fixture
def aggregation_response() -> AggregationResponse:
    return AggregationResponse(
        results=(
            SearchResult(
                id="ebay:1",
                external_id="1",
                title="RTX 3090",
                price=899.0,
                currency="EUR",
                platform="ebay",
                url="https://example.com/items/1",
                collected_at=datetime(2026, 7, 28, tzinfo=UTC),
            ),
        ),
        metrics=AggregationMetrics(
            provider_count=1,
            successful_provider_count=1,
            raw_result_count=1,
            normalized_result_count=1,
            filtered_result_count=1,
            final_result_count=1,
            duration_ms=10.5,
        ),
    )


@pytest.mark.asyncio
async def test_redis_search_cache_round_trips_typed_response_with_ttl(
    aggregation_request: AggregationRequest,
    aggregation_response: AggregationResponse,
) -> None:
    redis_client = AsyncMock()
    redis_client.get.return_value = aggregation_response.model_dump_json()
    cache = RedisSearchCache(redis_client)
    expected_key = cache.key_builder.build(aggregation_request)

    cached_response = await cache.get(aggregation_request)
    await cache.set(
        aggregation_request,
        aggregation_response,
        ttl_seconds=300,
    )

    assert cached_response == aggregation_response
    redis_client.get.assert_awaited_once_with(expected_key)
    redis_client.set.assert_awaited_once_with(
        expected_key,
        aggregation_response.model_dump_json(),
        ex=300,
    )


@pytest.mark.asyncio
async def test_redis_search_cache_returns_miss_for_missing_or_invalid_payload(
    aggregation_request: AggregationRequest,
) -> None:
    redis_client = AsyncMock()
    cache = RedisSearchCache(redis_client)

    redis_client.get.return_value = None
    assert await cache.get(aggregation_request) is None

    redis_client.get.return_value = '{"results":"invalid"}'
    assert await cache.get(aggregation_request) is None


@pytest.mark.asyncio
async def test_redis_search_cache_fails_open_when_redis_is_unavailable(
    aggregation_request: AggregationRequest,
    aggregation_response: AggregationResponse,
) -> None:
    redis_client = AsyncMock()
    redis_client.get.side_effect = RedisConnectionError("unavailable")
    redis_client.set.side_effect = RedisConnectionError("unavailable")
    redis_client.aclose.side_effect = RedisConnectionError("unavailable")
    cache = RedisSearchCache(redis_client)

    assert await cache.get(aggregation_request) is None
    await cache.set(
        aggregation_request,
        aggregation_response,
        ttl_seconds=300,
    )
    await cache.aclose()


@pytest.mark.asyncio
async def test_redis_search_cache_rejects_non_positive_ttl(
    aggregation_request: AggregationRequest,
    aggregation_response: AggregationResponse,
) -> None:
    cache = RedisSearchCache(AsyncMock())

    with pytest.raises(ValueError, match="ttl_seconds must be greater than zero"):
        await cache.set(
            aggregation_request,
            aggregation_response,
            ttl_seconds=0,
        )
