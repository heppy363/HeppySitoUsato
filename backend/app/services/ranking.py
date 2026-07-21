import re
from abc import ABC, abstractmethod
from collections.abc import Iterable

from app.providers import SearchRequest, SearchResult


class RankingService(ABC):
    @abstractmethod
    def rank(
        self,
        request: SearchRequest,
        results: Iterable[SearchResult],
    ) -> tuple[SearchResult, ...]:
        raise NotImplementedError


class HeuristicRankingService(RankingService):
    def rank(
        self,
        request: SearchRequest,
        results: Iterable[SearchResult],
    ) -> tuple[SearchResult, ...]:
        prepared_results = tuple(results)
        if not prepared_results:
            return ()

        price_bounds = self._price_bounds(prepared_results)
        return tuple(
            self._rank_result(request, result, price_bounds) for result in prepared_results
        )

    def _rank_result(
        self,
        request: SearchRequest,
        result: SearchResult,
        price_bounds: tuple[float, float],
    ) -> SearchResult:
        heuristic_score = (
            self._query_match_score(request.query, result)
            + self._freshness_score(result)
            + self._data_quality_score(result)
            + self._price_score(result.price, price_bounds)
        )
        final_score = min(1.0, max(result.relevance_score, heuristic_score))
        return result.model_copy(update={"relevance_score": round(final_score, 6)})

    @staticmethod
    def _price_bounds(results: tuple[SearchResult, ...]) -> tuple[float, float]:
        prices = tuple(result.price for result in results)
        return (min(prices), max(prices))

    @classmethod
    def _query_match_score(cls, query: str, result: SearchResult) -> float:
        normalized_query = cls._normalize_text(query)
        normalized_title = cls._normalize_text(result.title)
        normalized_description = cls._normalize_text(result.description or "")
        query_tokens = cls._tokenize(query)

        if normalized_title == normalized_query:
            title_score = 0.55
        elif normalized_query and normalized_query in normalized_title:
            title_score = 0.45
        else:
            title_score = cls._token_overlap(query_tokens, cls._tokenize(result.title)) * 0.4

        if normalized_query and normalized_query in normalized_description:
            description_score = 0.1
        else:
            description_score = (
                cls._token_overlap(query_tokens, cls._tokenize(result.description or "")) * 0.1
            )

        return min(0.65, title_score + description_score)

    @staticmethod
    def _freshness_score(result: SearchResult) -> float:
        if result.published_at is None:
            return 0.0

        age_days = max(
            0.0,
            (result.collected_at - result.published_at).total_seconds() / 86400.0,
        )
        freshness_ratio = max(0.0, (30.0 - age_days) / 30.0)
        return freshness_ratio * 0.15

    @staticmethod
    def _data_quality_score(result: SearchResult) -> float:
        score = 0.0
        if result.description is not None:
            score += 0.02
        if result.image_url is not None:
            score += 0.02
        if result.location is not None:
            score += 0.02
        if result.seller_name is not None:
            score += 0.02
        if result.seller_rating is not None or result.condition is not None:
            score += 0.02
        return score

    @staticmethod
    def _price_score(price: float, price_bounds: tuple[float, float]) -> float:
        minimum_price, maximum_price = price_bounds
        if minimum_price == maximum_price:
            return 0.05
        return ((maximum_price - price) / (maximum_price - minimum_price)) * 0.1

    @staticmethod
    def _token_overlap(query_tokens: tuple[str, ...], text_tokens: tuple[str, ...]) -> float:
        if not query_tokens or not text_tokens:
            return 0.0

        matched_tokens = set(query_tokens).intersection(text_tokens)
        return len(matched_tokens) / len(set(query_tokens))

    @classmethod
    def _tokenize(cls, value: str) -> tuple[str, ...]:
        normalized = cls._normalize_text(value)
        if not normalized:
            return ()
        return tuple(normalized.split())

    @staticmethod
    def _normalize_text(value: str) -> str:
        sanitized = re.sub(r"[\W_]+", " ", value.casefold(), flags=re.UNICODE)
        return " ".join(sanitized.split())
