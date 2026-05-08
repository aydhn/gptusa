from pathlib import Path
from usa_signal_bot.release.artifact_collector import (
    is_secret_like_path, should_exclude_path, collect_source_artifacts,
    collect_config_artifacts, artifact_collection_to_text
)

def test_secret_paths():
    assert is_secret_like_path(Path(".env")) is True
    assert is_secret_like_path(Path("secret.json")) is True
    assert is_secret_like_path(Path("token.key")) is True
    assert is_secret_like_path(Path("default.yaml")) is False

def test_should_exclude_path():
    assert should_exclude_path(Path("src/__pycache__/x.pyc")) is True
    assert should_exclude_path(Path(".git/config")) is True

def test_collect_config_artifacts(tmp_path):
    conf_dir = tmp_path / "config"
    conf_dir.mkdir()
    (conf_dir / "default.yaml").write_text("a: 1")
    (conf_dir / ".env").write_text("secret=1")

    arts = collect_config_artifacts(tmp_path, include_secrets=False)
    assert len(arts) == 1
    assert "default.yaml" in arts[0].name
