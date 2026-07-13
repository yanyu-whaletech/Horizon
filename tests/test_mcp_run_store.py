from __future__ import annotations

from pathlib import Path

import pytest

from src.mcp.run_store import RunStore


def test_create_run_writes_meta(tmp_path: Path) -> None:
    store = RunStore(tmp_path)

    run_id = store.create_run()
    meta = store.load_meta(run_id)

    assert run_id.startswith("run-")
    assert meta["run_id"] == run_id
    assert meta["status"] == "created"
    assert meta["stages"] == {}
    assert "created_at" in meta


def test_save_and_load_stage_items(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-fixed")
    items = [{"title": "foo"}, {"title": "bar"}]

    path = store.save_items(run_id, "raw", items)
    loaded = store.load_items(run_id, "raw")

    assert path.name == "raw_items.json"
    assert loaded == items
    assert store.has_stage(run_id, "raw") is True


def test_update_meta_sets_updated_at(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-meta")

    meta = store.update_meta(run_id, {"status": "done"})

    assert meta["status"] == "done"
    assert "updated_at" in meta


def test_save_and_load_summary(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-summary")

    saved = store.save_summary(run_id, "zh", "# 摘要")
    content = store.load_summary(run_id, "zh")

    assert saved.name == "summary-zh.md"
    assert content == "# 摘要"


def test_unsupported_stage_raises(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-invalid-stage")

    with pytest.raises(ValueError, match="Unsupported stage"):
        store.save_items(run_id, "unknown", [])


def test_missing_run_raises(tmp_path: Path) -> None:
    store = RunStore(tmp_path)

    with pytest.raises(FileNotFoundError, match="Run not found"):
        store.run_dir("missing-run")


def test_rejects_path_traversal_run_id(tmp_path: Path) -> None:
    store = RunStore(tmp_path / "runs")

    with pytest.raises(ValueError, match="Invalid run_id"):
        store.create_run("../outside")

    assert not (tmp_path / "outside").exists()


def test_rejects_unsafe_summary_language(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-summary-safe")

    with pytest.raises(ValueError, match="Invalid summary language"):
        store.save_summary(run_id, "../zh", "# unsafe")


def test_missing_artifact_raises(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-missing-file")

    with pytest.raises(FileNotFoundError, match="Artifact not found"):
        store.read_json(run_id, "does-not-exist.json")


def test_list_runs_returns_desc_order(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run1 = store.create_run("run-1")
    store.update_meta(run1, {"seq": 1})
    run2 = store.create_run("run-2")
    store.update_meta(run2, {"seq": 2})

    runs = store.list_runs(limit=10)

    assert runs[0]["run_id"] == "run-2"
    assert runs[1]["run_id"] == "run-1"


def test_track_stage_and_complete_run_records_lifecycle(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-lifecycle")

    with store.track_stage(run_id, "raw"):
        pass
    meta = store.complete_run(run_id)

    assert meta["status"] == "succeeded"
    assert meta["operation"] == "pipeline"
    assert meta["stages"]["raw"]["status"] == "succeeded"
    assert meta["stages"]["raw"]["duration_ms"] >= 0
    assert meta["duration_ms"] >= 0
    assert "completed_at" in meta


def test_track_stage_records_failure(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-failed")

    with pytest.raises(RuntimeError, match="scraper unavailable"):
        with store.track_stage(run_id, "raw"):
            raise RuntimeError("scraper unavailable")

    meta = store.load_meta(run_id)
    assert meta["status"] == "failed"
    assert meta["failed_stage"] == "raw"
    assert meta["error"] == {
        "type": "RuntimeError",
        "message": "scraper unavailable",
    }
    assert meta["stages"]["raw"]["status"] == "failed"


def test_track_stage_rejects_unsafe_name(tmp_path: Path) -> None:
    store = RunStore(tmp_path)
    run_id = store.create_run("run-safe-stage")

    with pytest.raises(ValueError, match="Invalid stage name"):
        with store.track_stage(run_id, "../raw"):
            pass
