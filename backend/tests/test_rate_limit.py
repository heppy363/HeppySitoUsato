import pytest

from app.services import SlidingWindowRateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_blocks_requests_over_limit_and_reports_retry() -> None:
    current_time = 100.0
    limiter = SlidingWindowRateLimiter(
        limit=2,
        window_seconds=10.0,
        clock=lambda: current_time,
    )

    first = await limiter.check("client-a")
    second = await limiter.check("client-a")
    blocked = await limiter.check("client-a")

    assert first.allowed is True
    assert first.remaining == 1
    assert second.allowed is True
    assert second.remaining == 0
    assert blocked.allowed is False
    assert blocked.retry_after_seconds == 10


@pytest.mark.asyncio
async def test_rate_limiter_isolates_clients_and_releases_expired_requests() -> None:
    current_time = 100.0
    limiter = SlidingWindowRateLimiter(
        limit=1,
        window_seconds=10.0,
        clock=lambda: current_time,
    )

    assert (await limiter.check("client-a")).allowed is True
    assert (await limiter.check("client-b")).allowed is True

    current_time = 110.0

    renewed = await limiter.check("client-a")
    assert renewed.allowed is True
    assert renewed.remaining == 0
