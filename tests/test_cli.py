import pytest
import subprocess
import sys

def test_universe_info_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-info"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "USA Signal Bot Universe Info" in result.stdout

def test_universe_validate_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-validate"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Passed        : YES" in result.stdout

def test_universe_list_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-list", "--limit", "2"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Symbols" in result.stdout

def test_universe_build_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-build"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Snapshot written" in result.stdout

def test_universe_summary_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-summary"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Summary" in result.stdout

def test_provider_info_command():
    # Since we use sys.exit, we'll just check if it runs without exception
    # directly using a subprocess or mock
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-info"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "USA Signal Bot Provider Info" in result.stdout
    assert "mock" in result.stdout

def test_provider_list_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-list"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Registered Providers" in result.stdout

def test_provider_check_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-check"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "All guard checks passed" in result.stdout

def test_provider_plan_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-plan", "--symbols", "AAPL,MSFT", "--timeframe", "1d"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Provider Fetch Plan" in result.stdout
    assert "Symbols: 2" in result.stdout

def test_provider_mock_fetch_command():
    import subprocess
    result = subprocess.run(["python", "-m", "usa_signal_bot", "provider-mock-fetch", "--symbols", "AAPL", "--timeframe", "1d"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Mock Data Fetch Result" in result.stdout
    assert "fake data" in result.stdout

def test_cli_data_provider_info():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "data-provider-info"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "[MOCK]" in result.stdout

def test_cli_data_cache_info():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "data-cache-info"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Market Data Cache Info" in result.stdout

def test_cli_data_download_mock():
    # Execute a download via the mock provider to avoid real network calls
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "data-download", "--symbols", "AAPL", "--timeframe", "1d", "--provider", "mock"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Success: True" in result.stdout
    assert "Data Quality Report (mock - 1d)" in result.stdout

def test_data_mtf_plan_command_success(monkeypatch, tmp_path):
    import sys
    from unittest.mock import patch
    import usa_signal_bot.app.cli

    with patch("usa_signal_bot.app.cli.handle_data_mtf_plan", return_value=0) as mock:
        testargs = ["usa_signal_bot", "data-mtf-plan", "--symbols", "AAPL", "--timeframes", "1d,1h"]
        monkeypatch.setattr(sys, 'argv', testargs)

        with pytest.raises(SystemExit) as e:
            usa_signal_bot.app.cli.main()

        assert e.value.code == 0
        mock.assert_called_once()

def test_universe_sources_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-sources"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "USA Signal Bot Universe Sources" in result.stdout

def test_universe_presets_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-presets"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Presets" in result.stdout

def test_universe_catalog_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-catalog"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Catalog" in result.stdout

def test_universe_expand_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-expand", "--max-symbols", "20", "--no-snapshot"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Expansion Result" in result.stdout

def test_universe_snapshots_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-snapshots"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Universe Snapshots" in result.stdout

def test_universe_import_command(tmp_path):
    # Create temp csv
    import uuid
    rand_name = f"test_import_{uuid.uuid4().hex[:8]}"
    p = tmp_path / "test.csv"
    with open(p, "w") as f:
        f.write("symbol,asset_type\nAAPL,stock\n")

    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-import", "--file", str(p), "--name", rand_name],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Import successful!" in result.stdout

def test_universe_export_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "universe-export", "--format", "txt", "--active-only"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "Export successful:" in result.stdout


def test_active_universe_info_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "active-universe-info"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_active_universe_symbols_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "active-universe-symbols", "--limit", "5"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_active_universe_plan_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "active-universe-plan", "--timeframes", "1d,1h", "--limit", "5"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_active_universe_runs_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "active-universe-runs"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0

def test_active_universe_latest_run_command():
    result = subprocess.run(
        [sys.executable, "-m", "usa_signal_bot", "active-universe-latest-run"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
