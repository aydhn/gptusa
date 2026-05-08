from pathlib import Path
from usa_signal_bot.release.local_packager import LocalReleasePackager
from usa_signal_bot.release.release_models import ReleaseBuildRequest

def test_local_packager_build(tmp_path):
    req = ReleaseBuildRequest(
        request_id="req1",
        release_name="test_release",
        output_dir=str(tmp_path / "out"),
        include_docs=False,
        include_tests=False,
        include_reports=False
    )

    packager = LocalReleasePackager(project_root=tmp_path, data_root=tmp_path / "data")
    res = packager.build(req)

    assert res.status.value == "BUILT"
    assert res.bundle_path is not None
    assert Path(res.bundle_path).exists()
    assert res.validation_status.value == "PASSED"
