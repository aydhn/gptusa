from pathlib import Path

def test_is_protected_path():
    from usa_signal_bot.retention.protected_paths import is_protected_path
    assert is_protected_path(Path(".env")) is True
    assert is_protected_path(Path("secret.key")) is True
    assert is_protected_path(Path("config/default.yaml")) is True
    assert is_protected_path(Path("data/runtime/scans/scan_1.json")) is False

def test_filter_unprotected_paths():
    from usa_signal_bot.retention.protected_paths import filter_unprotected_paths
    paths = [Path(".env"), Path("data/runtime/scans/scan_1.json")]
    filtered = filter_unprotected_paths(paths)
    assert len(filtered) == 1
    assert str(filtered[0]) == "data/runtime/scans/scan_1.json"
