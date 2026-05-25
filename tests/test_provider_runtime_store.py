from pathlib import Path
from usa_signal_bot.data_provider_runtime.provider_runtime_store import provider_runtime_store_dir, write_provider_runtime_context_json
from usa_signal_bot.data_provider_runtime.provider_runtime_report import build_provider_runtime_context

def test_provider_runtime_store(tmp_path):
    d = provider_runtime_store_dir(tmp_path)
    assert d.exists()

    ctx = build_provider_runtime_context()
    f = write_provider_runtime_context_json(d / "test.json", ctx)
    assert f.exists()
