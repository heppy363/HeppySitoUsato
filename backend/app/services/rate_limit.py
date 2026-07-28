import asyncio
import math
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from time import monotonic


@dataclass(frozen=True, slots=True)
class RateLimitDecision:
    allowed: bool
    limit: int
    remaining: int
    retry_after_seconds: int | None = None


class SlidingWindowRateLimiter:
    def __init__(
        self,
        *,
        limit: int,
        window_seconds: float,
        clock: Callable[[], float] = monotonic,
    ) -> None:
        if limit < 1:
            raise ValueError("limit must be greater than zero")
        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than zero")

        self._limit = limit
        self._window_seconds = window_seconds
        self._clock = clock
        self._requests: dict[str, deque[float]] = {}
        self._lock = asyncio.Lock()

    async def check(self, key: str) -> RateLimitDecision:
        normalized_key = key.strip() or "unknown"

        async with self._lock:
            now = self._clock()
            threshold = now - self._window_seconds
            self._discard_expired_keys(threshold)
            timestamps = self._requests.setdefault(normalized_key, deque())

            if len(timestamps) >= self._limit:
                retry_after = max(1, math.ceil(timestamps[0] + self._window_seconds - now))
                return RateLimitDecision(
                    allowed=False,
                    limit=self._limit,
                    remaining=0,
                    retry_after_seconds=retry_after,
                )

            timestamps.append(now)
            return RateLimitDecision(
                allowed=True,
                limit=self._limit,
                remaining=self._limit - len(timestamps),
            )

    def _discard_expired_keys(self, threshold: float) -> None:
        for key, timestamps in tuple(self._requests.items()):
            while timestamps and timestamps[0] <= threshold:
                timestamps.popleft()
            if not timestamps:
                del self._requests[key]
