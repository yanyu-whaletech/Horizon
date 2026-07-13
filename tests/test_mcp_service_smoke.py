from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.models import ContentItem, SourceType
from src.mcp.server import hz_get_metrics
from src.mcp.service import HorizonPipelineService


def make_item(item_id: str, score: float | None = None) -> ContentItem:
    item = ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url=f"https://example.com/{item_id}",
        content="content",
        author="tester",
        published_at=datetime.now(timezone.utc),
    )
    item.ai_score = score
    return item
def test_validate_config_smoke(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = tmp_path / "config.json"
    config_path.write_text(
        (repo_root / "data" / "config.example.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    result = asyncio.run(
        service.validate_config(
            horizon_path=str(repo_root),
            config_path=str(config_path),
            check_env=False,
        )
    )

    assert result["config_path"] == str(config_path.resolve())
    assert result["enabled_sources"]
    assert result["missing_env"] == []


def test_get_effective_config_can_filter_sources(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    config_path = tmp_path / "config.json"
    config_path.write_text(
        (repo_root / "data" / "config.example.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    result = service.get_effective_config(
        horizon_path=str(repo_root),
        config_path=str(config_path),
        sources=["rss"],
    )

    assert result["selected_sources"] == ["rss"]
    assert result["config"]["sources"]["github"] == []
    assert result["config"]["sources"]["rss"]


def test_metrics_tool_smoke() -> None:
    result = hz_get_metrics()

    assert result["ok"] is True
    assert result["tool"] == "hz_get_metrics"


def test_fetch_items_uses_public_orchestrator_api(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    config_path = tmp_path / "config.json"

    monkeypatch.setattr(
        service,
        "_build_context",
        lambda **kwargs: (
            SimpleNamespace(
                horizon_path=tmp_path,
                config_path=config_path,
                runtime=SimpleNamespace(),
                config=SimpleNamespace(),
            ),
            ["rss"],
            [],
        ),
    )
    monkeypatch.setattr("src.mcp.service.make_storage", lambda runtime, config_path: object())

    class FakeOrchestrator:
        last_fetch_report = {
            "rss": {"status": "succeeded", "item_count": 2, "duration_ms": 5}
        }

        async def fetch_all_sources(self, since):  # type: ignore[no-untyped-def]
            return [make_item("item-1"), make_item("item-2")]

        def merge_cross_source_duplicates(self, items):  # type: ignore[no-untyped-def]
            return items[:1]

    monkeypatch.setattr(
        "src.mcp.service.make_orchestrator",
        lambda runtime, config, storage: FakeOrchestrator(),
    )

    result = asyncio.run(service.fetch_items(hours=6))

    assert result["fetched"] == 1
    assert result["raw_before_merge"] == 2
    assert result["source_health"]["rss"]["status"] == "succeeded"
    assert result["meta"]["source_health"] == result["source_health"]
    assert service.run_store.load_items(result["run_id"], "raw")[0]["id"] == "item-1"


def test_filter_items_uses_public_topic_dedup_api(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    service.run_store.create_run("run-topic-dedup")

    monkeypatch.setattr(
        service,
        "_load_stage_items",
        lambda **kwargs: (
            [make_item("item-1", score=9.0), make_item("item-2", score=8.0)],
            SimpleNamespace(
                runtime=SimpleNamespace(),
                config_path=tmp_path / "config.json",
                config=SimpleNamespace(filtering=SimpleNamespace(ai_score_threshold=7.0)),
            ),
        ),
    )
    monkeypatch.setattr("src.mcp.service.make_storage", lambda runtime, config_path: object())

    class FakeOrchestrator:
        async def merge_topic_duplicates(self, items):  # type: ignore[no-untyped-def]
            return items[:1]

    monkeypatch.setattr(
        "src.mcp.service.make_orchestrator",
        lambda runtime, config, storage: FakeOrchestrator(),
    )

    result = asyncio.run(service.filter_items(run_id="run-topic-dedup", topic_dedup=True))

    assert result["kept"] == 1
    assert result["removed_by_topic_dedup"] == 1
    assert service.run_store.load_items("run-topic-dedup", "filtered")[0]["id"] == "item-1"


def test_filter_items_applies_balanced_digest(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")
    service.run_store.create_run("run-balanced")
    filtering = SimpleNamespace(
        ai_score_threshold=7.0,
        max_items=1,
        category_groups={},
    )

    monkeypatch.setattr(
        service,
        "_load_stage_items",
        lambda **kwargs: (
            [make_item("item-1", score=9.0), make_item("item-2", score=8.0)],
            SimpleNamespace(
                runtime=SimpleNamespace(),
                config_path=tmp_path / "config.json",
                config=SimpleNamespace(filtering=filtering),
            ),
        ),
    )
    monkeypatch.setattr("src.mcp.service.make_storage", lambda runtime, config_path: object())

    class FakeOrchestrator:
        def apply_balanced_digest(self, items, log=True):  # type: ignore[no-untyped-def]
            assert log is False
            return SimpleNamespace(items=items[:1], group_counts={"other": 1})

    monkeypatch.setattr(
        "src.mcp.service.make_orchestrator",
        lambda runtime, config, storage: FakeOrchestrator(),
    )

    result = asyncio.run(
        service.filter_items(run_id="run-balanced", topic_dedup=False)
    )

    assert result["kept"] == 1
    assert result["removed_by_balanced_digest"] == 1
    assert result["balanced_digest_enabled"] is True
    assert result["group_counts"] == {"other": 1}


def test_run_pipeline_records_successful_stage_lifecycle(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")

    async def fake_fetch(**kwargs):  # type: ignore[no-untyped-def]
        return {"run_id": kwargs["run_id"]}

    async def fake_stage(**kwargs):  # type: ignore[no-untyped-def]
        return {"run_id": kwargs["run_id"]}

    monkeypatch.setattr(service, "fetch_items", fake_fetch)
    monkeypatch.setattr(service, "score_items", fake_stage)
    monkeypatch.setattr(service, "filter_items", fake_stage)
    monkeypatch.setattr(service, "generate_summary", fake_stage)
    monkeypatch.setattr(
        service,
        "_build_context",
        lambda **kwargs: (
            SimpleNamespace(config=SimpleNamespace(ai=SimpleNamespace(languages=["en"]))),
            [],
            [],
        ),
    )

    result = asyncio.run(service.run_pipeline(enrich=False))

    assert result["meta"]["status"] == "succeeded"
    assert set(result["meta"]["stages"]) == {
        "raw",
        "scored",
        "filtered",
        "summary:en",
    }
    assert all(
        stage["status"] == "succeeded"
        for stage in result["meta"]["stages"].values()
    )


def test_run_pipeline_records_failed_stage(tmp_path: Path, monkeypatch) -> None:
    service = HorizonPipelineService(runs_root=tmp_path / "mcp-runs")

    async def fake_fetch(**kwargs):  # type: ignore[no-untyped-def]
        return {"run_id": kwargs["run_id"]}

    async def fail_score(**kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("model unavailable")

    monkeypatch.setattr(service, "fetch_items", fake_fetch)
    monkeypatch.setattr(service, "score_items", fail_score)

    with pytest.raises(RuntimeError, match="model unavailable"):
        asyncio.run(service.run_pipeline(enrich=False))

    meta = service.run_store.list_runs(limit=1)[0]["meta"]
    assert meta["status"] == "failed"
    assert meta["failed_stage"] == "scored"
    assert meta["stages"]["raw"]["status"] == "succeeded"
    assert meta["stages"]["scored"]["status"] == "failed"
