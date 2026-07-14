import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

import src.ai.analyzer as analyzer_module
from src.ai.analyzer import (
    AnalysisBatchError,
    ContentAnalyzer,
    TransientAnalysisError,
)
from src.models import ContentItem, SourceType


def _make_item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url="https://example.com/item",
        published_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )


def test_analyze_batch_does_not_sleep_by_default(monkeypatch):
    analyzer = ContentAnalyzer(SimpleNamespace())
    items = [_make_item("rss:test:1"), _make_item("rss:test:2")]
    sleep_calls = []

    async def fake_analyze_item(item):
        item.ai_score = 8.0

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)
    monkeypatch.setattr(analyzer_module.asyncio, "sleep", fake_sleep)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert len(result) == 2
    assert sleep_calls == []


def test_analyze_batch_sleeps_between_items_when_throttle_configured(monkeypatch):
    client = SimpleNamespace(config=SimpleNamespace(throttle_sec=1.5))
    analyzer = ContentAnalyzer(client)
    items = [_make_item("rss:test:1"), _make_item("rss:test:2"), _make_item("rss:test:3")]
    sleep_calls = []

    async def fake_analyze_item(item):
        item.ai_score = 8.0

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)
    monkeypatch.setattr(analyzer_module.asyncio, "sleep", fake_sleep)

    asyncio.run(analyzer.analyze_batch(items))

    assert sleep_calls == [1.5, 1.5]


def test_analyze_batch_concurrent_processing(monkeypatch):
    """Verify that higher concurrency allows overlapping item processing."""
    client = SimpleNamespace(config=SimpleNamespace(analysis_concurrency=3))
    analyzer = ContentAnalyzer(client)
    items = [_make_item(f"rss:test:{i}") for i in range(5)]
    active_count = 0
    max_active = 0

    async def fake_analyze_item(item):
        nonlocal active_count, max_active
        active_count += 1
        max_active = max(max_active, active_count)
        await asyncio.sleep(0.05)  # Small delay to allow overlap
        active_count -= 1

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    asyncio.run(analyzer.analyze_batch(items))

    assert max_active == 3
    assert all(item.ai_score is None for item in items)  # None because fake_analyze_item doesn't set it


def test_analyze_batch_concurrent_preserves_order(monkeypatch):
    """Verify that analyze_batch preserves input order in results."""
    client = SimpleNamespace(config=SimpleNamespace(analysis_concurrency=3))
    analyzer = ContentAnalyzer(client)
    items = [_make_item(f"rss:test:{i}") for i in range(5)]

    async def fake_analyze_item(item):
        item.ai_score = float(item.id.split(":")[-1]) * 10

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert [item.id for item in result] == [item.id for item in items]


def test_analyze_batch_raises_temporary_error_when_entire_batch_is_unavailable(monkeypatch):
    class InternalServerError(Exception):
        status_code = 500

    analyzer = ContentAnalyzer(SimpleNamespace())
    items = [_make_item("rss:test:1"), _make_item("rss:test:2")]

    async def fake_analyze_item(item):
        raise InternalServerError("upstream unavailable")

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    with pytest.raises(TransientAnalysisError, match="all 2 items failed"):
        asyncio.run(analyzer.analyze_batch(items))

    assert all(item.ai_score == 0.0 for item in items)


def test_transient_error_detection_unwraps_exhausted_retry():
    class InternalServerError(Exception):
        status_code = 500

    class RetryError(Exception):
        def __init__(self):
            self.last_attempt = SimpleNamespace(
                exception=lambda: InternalServerError("upstream unavailable")
            )

    assert ContentAnalyzer._is_transient_error(RetryError()) is True


def test_analyze_batch_does_not_abort_on_partial_transient_failure(monkeypatch):
    class InternalServerError(Exception):
        status_code = 500

    analyzer = ContentAnalyzer(SimpleNamespace())
    items = [_make_item("rss:test:1"), _make_item("rss:test:2")]

    async def fake_analyze_item(item):
        if item.id.endswith(":1"):
            raise InternalServerError("upstream unavailable")
        item.ai_score = 8.0

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert [item.ai_score for item in result] == [0.0, 8.0]


def test_analyze_batch_raises_non_temporary_error_for_permanent_batch_failure(monkeypatch):
    analyzer = ContentAnalyzer(SimpleNamespace())
    items = [_make_item("rss:test:1")]

    async def fake_analyze_item(item):
        raise ValueError("invalid request")

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    with pytest.raises(AnalysisBatchError, match="failed for all 1 items") as exc_info:
        asyncio.run(analyzer.analyze_batch(items))

    assert not isinstance(exc_info.value, TransientAnalysisError)
