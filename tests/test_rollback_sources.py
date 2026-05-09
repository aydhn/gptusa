from usa_signal_bot.incident.rollback_sources import discover_config_profile_sources
from pathlib import Path

def test_discover_config_profiles(tmp_path):
    c = tmp_path / "config"
    c.mkdir()
    (c / "a.yaml").touch()
    srcs = discover_config_profile_sources(tmp_path)
    assert len(srcs) == 1
