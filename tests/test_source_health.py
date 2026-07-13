from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from src.orchestrator import HorizonOrchestrator


def make_orchestrator() -> HorizonOrchestrator:
    config = SimpleNamespace(email=None, webhook=None)
    return HorizonOrchestrator(config=config, storage=object())


def test_fetch_progress_records_success() -> None:
    orchestrator = make_orchestrator()

    class Scraper:
        async def fetch(self, since):  # type: ignore[no-untyped-def]
            return [SimpleNamespace(metadata={}, author="author")]

    items = asyncio.run(
        orchestrator._fetch_with_progress(
            "RSS Feeds",
            Scraper(),
            datetime.now(timezone.utc),
        )
    )

    assert len(items) == 1
    report = orchestrator.last_fetch_report["rss"]
    assert report["status"] == "succeeded"
    assert report["item_count"] == 1
    assert report["duration_ms"] >= 0


def test_fetch_progress_records_failure() -> None:
    orchestrator = make_orchestrator()

    class Scraper:
        async def fetch(self, since):  # type: ignore[no-untyped-def]
            raise TimeoutError("feed timed out")

    with pytest.raises(TimeoutError, match="feed timed out"):
        asyncio.run(
            orchestrator._fetch_with_progress(
                "RSS Feeds",
                Scraper(),
                datetime.now(timezone.utc),
            )
        )

    report = orchestrator.last_fetch_report["rss"]
    assert report["status"] == "failed"
    assert report["item_count"] == 0
    assert report["error"] == {
        "type": "TimeoutError",
        "message": "feed timed out",
    }
