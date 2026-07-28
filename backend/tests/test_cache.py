import pytest
from pydantic import ValidationError

from app.core.config import Settings
from app.providers import SearchRequest
from app.services import (
    AggregationRequest,
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
