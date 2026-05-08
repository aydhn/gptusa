import pytest
from datetime import datetime, timezone
from usa_signal_bot.core.enums import ReleaseStatus, ReleaseArtifactType, ReleaseValidationStatus
from usa_signal_bot.release.release_models import (
    ReleaseVersion, ReleaseArtifact, ReleaseManifest, ReleaseBuildRequest, ReleaseBuildResult, OperatorRunbook,
    create_release_build_id, create_release_manifest_id, create_release_artifact_id, create_runbook_id,
    validate_release_version, validate_release_artifact, validate_release_manifest, validate_release_build_request,
    validate_release_build_result
)

def test_release_version_valid():
    v = ReleaseVersion(version="1.0.0", build_id="b1", created_at_utc=datetime.now(timezone.utc).isoformat())
    validate_release_version(v)

def test_release_artifact_valid():
    a = ReleaseArtifact(artifact_id="a1", artifact_type=ReleaseArtifactType.SOURCE_CODE, name="test.py", source_path="test.py", target_path="test.py", size_bytes=10, checksum="abc", included=True)
    validate_release_artifact(a)

def test_release_manifest_valid():
    v = ReleaseVersion(version="1.0.0", build_id="b1", created_at_utc=datetime.now(timezone.utc).isoformat())
    m = ReleaseManifest(manifest_id="m1", release_name="r1", version=v, status=ReleaseStatus.CREATED, created_at_utc=v.created_at_utc, artifacts=[], artifact_count=0, total_size_bytes=0, checksum=None)
    validate_release_manifest(m)

def test_release_build_request_include_secrets_false():
    req = ReleaseBuildRequest(request_id="req1", release_name="r1", output_dir="out")
    validate_release_build_request(req)
    assert req.include_secrets is False

def test_release_build_request_include_secrets_true_blocks():
    req = ReleaseBuildRequest(request_id="req1", release_name="r1", output_dir="out", include_secrets=True)
    with pytest.raises(ValueError):
        validate_release_build_request(req)

def test_id_factories_generate_non_empty_strings():
    assert len(create_release_build_id()) > 0
    assert len(create_release_manifest_id()) > 0
    assert len(create_release_artifact_id("x")) > 0
    assert len(create_runbook_id()) > 0
