from types import SimpleNamespace

import pytest

import src.main as main_module
from src.ai.analyzer import TransientAnalysisError


def test_main_uses_temporary_failure_exit_code_for_ai_outage(monkeypatch):
    class FakeStorageManager:
        def __init__(self, data_dir):
            self.data_dir = data_dir

        def load_config(self):
            return SimpleNamespace()

    class FakeOrchestrator:
        def __init__(self, config, storage):
            pass

        async def run(self, force_hours=None):
            raise TransientAnalysisError("all items failed")

    monkeypatch.setattr(main_module, "StorageManager", FakeStorageManager)
    monkeypatch.setattr(main_module, "HorizonOrchestrator", FakeOrchestrator)
    monkeypatch.setattr(main_module.sys, "argv", ["horizon", "--hours", "24"])

    with pytest.raises(SystemExit) as exc_info:
        main_module.main()

    assert exc_info.value.code == main_module.TEMPORARY_FAILURE_EXIT_CODE == 75
