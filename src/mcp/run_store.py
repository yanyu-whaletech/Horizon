"""Run artifact persistence for Horizon MCP."""

from __future__ import annotations

import json
import re
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator
from uuid import uuid4

from ..error_utils import safe_error_message


STAGES = {
    "raw": "raw_items.json",
    "scored": "scored_items.json",
    "filtered": "filtered_items.json",
    "enriched": "enriched_items.json",
}
RUN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
LANGUAGE_RE = re.compile(r"^[A-Za-z0-9_-]+$")
STAGE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]*$")


@dataclass
class RunStore:
    """Store intermediate artifacts per pipeline run."""

    root: Path

    def __post_init__(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True)

    def create_run(self, run_id: str | None = None) -> str:
        run_id = run_id or self._make_run_id()
        run_dir = self._run_path(run_id)
        run_dir.mkdir(parents=True, exist_ok=True)
        meta_path = run_dir / "meta.json"
        if not meta_path.exists():
            self.write_json(
                run_id,
                "meta.json",
                {
                    "run_id": run_id,
                    "status": "created",
                    "created_at": self._utc_now(),
                    "stages": {},
                },
            )
        return run_id

    def start_run(self, run_id: str, operation: str = "pipeline") -> dict[str, Any]:
        """Mark a run active while preserving its original start time."""

        meta = self.load_meta(run_id)
        now = self._utc_now()
        meta["status"] = "running"
        meta["operation"] = operation
        meta.setdefault("started_at", now)
        meta.pop("completed_at", None)
        meta.pop("duration_ms", None)
        meta.pop("error", None)
        meta.pop("failed_stage", None)
        return self._save_meta(run_id, meta)

    def complete_run(self, run_id: str) -> dict[str, Any]:
        """Mark a run successful and record its wall-clock duration."""

        meta = self.load_meta(run_id)
        completed_at = self._utc_now()
        meta.update(
            {
                "status": "succeeded",
                "completed_at": completed_at,
                "duration_ms": self._duration_ms(meta.get("started_at"), completed_at),
            }
        )
        meta.pop("current_stage", None)
        meta.pop("error", None)
        meta.pop("failed_stage", None)
        return self._save_meta(run_id, meta)

    def fail_run(
        self,
        run_id: str,
        error: BaseException,
        stage: str | None = None,
    ) -> dict[str, Any]:
        """Mark a run failed with a compact, serializable error snapshot."""

        meta = self.load_meta(run_id)
        completed_at = self._utc_now()
        meta.update(
            {
                "status": "failed",
                "completed_at": completed_at,
                "duration_ms": self._duration_ms(meta.get("started_at"), completed_at),
                "error": self._error_payload(error),
            }
        )
        if stage:
            meta["failed_stage"] = stage
        meta.pop("current_stage", None)
        return self._save_meta(run_id, meta)

    @contextmanager
    def track_stage(self, run_id: str, stage: str) -> Iterator[None]:
        """Track one pipeline stage, including failures across awaited work."""

        self._validate_stage_name(stage)
        self.start_run(run_id)
        started_at = self._utc_now()
        self._update_stage(
            run_id,
            stage,
            {
                "status": "running",
                "started_at": started_at,
            },
            current_stage=stage,
        )
        try:
            yield
        except BaseException as exc:
            completed_at = self._utc_now()
            self._update_stage(
                run_id,
                stage,
                {
                    "status": "failed",
                    "completed_at": completed_at,
                    "duration_ms": self._duration_ms(started_at, completed_at),
                    "error": self._error_payload(exc),
                },
            )
            self.fail_run(run_id, exc, stage=stage)
            raise
        else:
            completed_at = self._utc_now()
            self._update_stage(
                run_id,
                stage,
                {
                    "status": "succeeded",
                    "completed_at": completed_at,
                    "duration_ms": self._duration_ms(started_at, completed_at),
                },
            )

    def run_dir(self, run_id: str) -> Path:
        path = self._run_path(run_id)
        if not path.exists():
            raise FileNotFoundError(f"Run not found: {run_id}")
        return path

    def has_stage(self, run_id: str, stage: str) -> bool:
        return (self.run_dir(run_id) / self._stage_file(stage)).exists()

    def save_items(self, run_id: str, stage: str, items: list[dict[str, Any]]) -> Path:
        return self.write_json(run_id, self._stage_file(stage), items)

    def load_items(self, run_id: str, stage: str) -> list[dict[str, Any]]:
        return self.read_json(run_id, self._stage_file(stage))

    def save_summary(self, run_id: str, language: str, markdown: str) -> Path:
        filename = self._summary_file(language)
        path = self.run_dir(run_id) / filename
        temp_path = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
        temp_path.write_text(markdown, encoding="utf-8")
        temp_path.replace(path)
        return path

    def load_summary(self, run_id: str, language: str) -> str:
        path = self.run_dir(run_id) / self._summary_file(language)
        if not path.exists():
            raise FileNotFoundError(f"Summary not found: run={run_id} lang={language}")
        return path.read_text(encoding="utf-8")

    def update_meta(self, run_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        meta = self.read_json(run_id, "meta.json")
        meta.update(updates)
        return self._save_meta(run_id, meta)

    def load_meta(self, run_id: str) -> dict[str, Any]:
        return self.read_json(run_id, "meta.json")

    def list_runs(self, limit: int = 20) -> list[dict[str, Any]]:
        """List runs sorted by create/update time descending."""

        entries: list[dict[str, Any]] = []
        for run_dir in self.root.iterdir():
            if not run_dir.is_dir():
                continue
            meta_path = run_dir / "meta.json"
            if not meta_path.exists():
                continue
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue

            created = meta.get("created_at") or ""
            updated = meta.get("updated_at") or created
            entries.append(
                {
                    "run_id": meta.get("run_id", run_dir.name),
                    "created_at": created,
                    "updated_at": updated,
                    "meta": meta,
                }
            )

        entries.sort(key=lambda x: x["updated_at"] or x["created_at"], reverse=True)
        return entries[: max(0, limit)]

    def write_json(self, run_id: str, filename: str, payload: Any) -> Path:
        path = self.run_dir(run_id) / filename
        temp_path = path.with_name(f".{path.name}.{uuid4().hex}.tmp")
        temp_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temp_path.replace(path)
        return path

    def read_json(self, run_id: str, filename: str) -> Any:
        path = self.run_dir(run_id) / filename
        if not path.exists():
            raise FileNotFoundError(f"Artifact not found: run={run_id} file={filename}")
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _stage_file(stage: str) -> str:
        if stage not in STAGES:
            supported = ", ".join(sorted(STAGES))
            raise ValueError(
                f"Unsupported stage '{stage}', expected one of: {supported}"
            )
        return STAGES[stage]

    def _run_path(self, run_id: str) -> Path:
        if not RUN_ID_RE.fullmatch(run_id) or ".." in run_id:
            raise ValueError("Invalid run_id")

        root = self.root.resolve()
        path = (self.root / run_id).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Invalid run_id")
        return path

    def _update_stage(
        self,
        run_id: str,
        stage: str,
        updates: dict[str, Any],
        current_stage: str | None = None,
    ) -> dict[str, Any]:
        meta = self.load_meta(run_id)
        stages = dict(meta.get("stages") or {})
        stage_meta = dict(stages.get(stage) or {})
        stage_meta.update(updates)
        stages[stage] = stage_meta
        meta["stages"] = stages
        if current_stage:
            meta["current_stage"] = current_stage
        elif meta.get("current_stage") == stage:
            meta.pop("current_stage", None)
        return self._save_meta(run_id, meta)

    def _save_meta(self, run_id: str, meta: dict[str, Any]) -> dict[str, Any]:
        meta["updated_at"] = self._utc_now()
        self.write_json(run_id, "meta.json", meta)
        return meta

    @staticmethod
    def _validate_stage_name(stage: str) -> None:
        if not STAGE_NAME_RE.fullmatch(stage) or ".." in stage:
            raise ValueError("Invalid stage name")

    @staticmethod
    def _duration_ms(started_at: str | None, completed_at: str) -> int | None:
        if not started_at:
            return None
        try:
            started = datetime.fromisoformat(started_at)
            completed = datetime.fromisoformat(completed_at)
        except ValueError:
            return None
        return max(0, round((completed - started).total_seconds() * 1000))

    @staticmethod
    def _error_payload(error: BaseException) -> dict[str, str]:
        return {
            "type": error.__class__.__name__,
            "message": safe_error_message(error),
        }

    @staticmethod
    def _summary_file(language: str) -> str:
        if not LANGUAGE_RE.fullmatch(language):
            raise ValueError("Invalid summary language")
        return f"summary-{language}.md"

    @staticmethod
    def _make_run_id() -> str:
        now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return f"run-{now}-{uuid4().hex[:8]}"

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat()
