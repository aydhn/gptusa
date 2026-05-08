from pathlib import Path
from usa_signal_bot.release.versioning import build_release_version
from usa_signal_bot.core.enums import ReleaseArtifactType
from usa_signal_bot.release.release_manifest import (
    calculate_file_checksum, build_release_artifact, build_release_manifest,
    release_manifest_to_markdown, write_release_manifest_json, read_release_manifest_json
)

def test_manifest_workflow(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello", encoding="utf-8")

    chk = calculate_file_checksum(f)
    assert len(chk) == 64

    art = build_release_artifact(f, "test.txt", ReleaseArtifactType.CUSTOM)
    assert art.checksum == chk

    v = build_release_version("1.0.0")
    man = build_release_manifest("test_release", v, [art])

    assert man.artifact_count == 1

    md = release_manifest_to_markdown(man)
    assert "test_release" in md

    json_path = tmp_path / "manifest.json"
    write_release_manifest_json(json_path, man)
    d = read_release_manifest_json(json_path)
    assert d["release_name"] == "test_release"
