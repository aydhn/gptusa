import pytest
from pathlib import Path
from usa_signal_bot.strategies.signal_store import signal_store_dir, write_signals_jsonl, read_signals_jsonl, list_signal_outputs, signal_store_summary
from usa_signal_bot.strategies.signal_contract import create_watch_signal

def test_signal_store_operations(tmp_path):
    d = signal_store_dir(tmp_path)
    assert d.exists()

    sig = create_watch_signal("test", "AAPL", "1d", "2023-01-01T00:00:00Z", "r1")

    fpath = d / "test.jsonl"
    write_signals_jsonl(fpath, [sig])

    assert fpath.exists()

    read_back = read_signals_jsonl(fpath)
    assert len(read_back) == 1
    assert read_back[0]["symbol"] == "AAPL"

    outs = list_signal_outputs(tmp_path)
    assert len(outs) == 1

    summary = signal_store_summary(tmp_path)
    assert summary["file_count"] == 1
    assert summary["total_size_bytes"] > 0
