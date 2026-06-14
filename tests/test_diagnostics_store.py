import json
from pathlib import Path
from dataclasses import dataclass
from usa_signal_bot.diagnostics.diagnostics_store import write_diagnostic_review_json


@dataclass
class DummyDiagnostic:
    score: float
    reason: str


def test_write_diagnostic_review_json_dict(tmp_path: Path):
    item = {"status": "ok", "value": 42}
    file_path = tmp_path / "test1.json"
    result_path = write_diagnostic_review_json(file_path, item)
    assert result_path == file_path
    assert file_path.exists()
    data = json.loads(file_path.read_text())
    assert data == item


def test_write_diagnostic_review_json_dataclass(tmp_path: Path):
    item = DummyDiagnostic(score=0.9, reason="passed")
    file_path = tmp_path / "test2.json"
    result_path = write_diagnostic_review_json(file_path, item)
    assert result_path == file_path
    assert file_path.exists()
    data = json.loads(file_path.read_text())
    assert data == {"score": 0.9, "reason": "passed"}
