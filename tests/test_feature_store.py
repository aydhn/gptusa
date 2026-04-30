import pytest
from pathlib import Path
import json

from usa_signal_bot.features.feature_store import (
    feature_store_dir, build_feature_output_path,
    write_feature_rows_jsonl, read_feature_rows_jsonl,
    write_feature_rows_csv, write_feature_metadata_json,
    list_feature_outputs, feature_store_summary
)
from usa_signal_bot.features.output_contract import FeatureRow, FeatureOutputMetadata
from usa_signal_bot.core.enums import FeatureStorageFormat

@pytest.fixture
def fake_rows():
    return [
        FeatureRow("2023-01-01", "AAPL", "1d", {"f1": 1.0, "f2": 2.0}),
        FeatureRow("2023-01-02", "AAPL", "1d", {"f1": 1.5, "f2": 2.5})
    ]

def test_feature_store_paths(tmp_path):
    d = feature_store_dir(tmp_path)
    assert d.exists()

    path = build_feature_output_path(tmp_path, "yfinance", None, "1d", "close_return", FeatureStorageFormat.JSONL)
    assert path.name == "yfinance_adhoc_1d_close_return.jsonl"

    path_csv = build_feature_output_path(tmp_path, "yfinance", "core", "1h", "all", FeatureStorageFormat.CSV)
    assert path_csv.name == "yfinance_core_1h_all.csv"

def test_feature_store_rw_jsonl(tmp_path, fake_rows):
    path = tmp_path / "test.jsonl"
    write_feature_rows_jsonl(path, fake_rows)
    assert path.exists()

    data = read_feature_rows_jsonl(path)
    assert len(data) == 2
    assert data[0]["symbol"] == "AAPL"
    assert data[0]["features"]["f1"] == 1.0

def test_feature_store_w_csv(tmp_path, fake_rows):
    path = tmp_path / "test.csv"
    write_feature_rows_csv(path, fake_rows)
    assert path.exists()

    content = path.read_text()
    assert "timestamp_utc,symbol,timeframe,f1,f2" in content
    assert "2023-01-01,AAPL,1d,1.0,2.0" in content

def test_feature_metadata_write(tmp_path):
    meta = FeatureOutputMetadata("id", "yfinance", None, ["AAPL"], ["1d"], ["ind"], ["feat"], 10, "2023", ["/path"])
    path = tmp_path / "test_meta.json"
    write_feature_metadata_json(path, meta)
    assert path.exists()
    assert '"output_id": "id"' in path.read_text()

def test_feature_store_list_and_summary(tmp_path, fake_rows):
    d = feature_store_dir(tmp_path)
    write_feature_rows_jsonl(d / "test1.jsonl", fake_rows)
    write_feature_rows_csv(d / "test2.csv", fake_rows)

    meta = FeatureOutputMetadata("id", "yfinance", None, ["AAPL"], ["1d"], ["ind"], ["feat"], 10, "2023", ["/path"])
    write_feature_metadata_json(d / "test_meta.json", meta)

    outputs = list_feature_outputs(tmp_path)
    assert len(outputs) == 2

    summary = feature_store_summary(tmp_path)
    assert summary["total_files"] == 3
    assert summary["jsonl_files"] == 1
    assert summary["csv_files"] == 1
    assert summary["metadata_files"] == 1
