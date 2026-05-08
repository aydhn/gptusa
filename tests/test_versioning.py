from usa_signal_bot.release.versioning import (
    get_project_version, create_build_id, build_release_version, normalize_version_string, version_to_text
)

def test_normalize_version_string():
    assert normalize_version_string(" 1.0.0 ") == "1.0.0"

def test_create_build_id():
    bid = create_build_id("1.0.0")
    assert bid.startswith("build_1_0_0_")

def test_build_release_version():
    v = build_release_version("1.0.0")
    assert v.version == "1.0.0"
    assert v.python_version is not None

def test_version_to_text():
    v = build_release_version("1.0.0")
    t = version_to_text(v)
    assert "Version: 1.0.0" in t
