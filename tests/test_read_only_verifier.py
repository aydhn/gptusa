import pytest
from pathlib import Path
from usa_signal_bot.core.enums import SandboxValidationStatus, SandboxMountMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxMountPlan
from usa_signal_bot.release_sandbox.read_only_verifier import (
    verify_path_readable, verify_bundle_source_not_output_path, verify_read_only_mount_plan, read_only_verifier_to_text
)

def test_verify_path_readable(tmp_path):
    assert verify_path_readable(tmp_path) is True
    assert verify_path_readable(Path("/invalid/path/that/does/not/exist")) is False

def test_verify_source_not_output(tmp_path):
    source = tmp_path / "source"
    out = tmp_path / "out"
    assert verify_bundle_source_not_output_path(source, out) is True
    assert verify_bundle_source_not_output_path(source, source) is False

def test_verify_read_only_mount_plan(tmp_path):
    source = tmp_path / "source"
    out = tmp_path / "out"

    plan = SandboxMountPlan(
        mount_id="m1", created_at_utc="now", bundle_id="b1", bundle_version="v1", mount_mode=SandboxMountMode.READ_ONLY,
        source_bundle_path=str(source), sandbox_output_path=str(out), read_only_verified=True, copy_on_write_enabled=True,
        allowed_operations=[], denied_operations=[], safety_flags=[], warnings=[], errors=[]
    )

    assert verify_read_only_mount_plan(plan) == SandboxValidationStatus.PASS

    plan.sandbox_output_path = str(source)
    assert verify_read_only_mount_plan(plan) == SandboxValidationStatus.FAIL

def test_read_only_verifier_to_text(tmp_path):
    plan = SandboxMountPlan(
        mount_id="m1", created_at_utc="now", bundle_id="b1", bundle_version="v1", mount_mode=SandboxMountMode.READ_ONLY,
        source_bundle_path="src", sandbox_output_path="out", read_only_verified=True, copy_on_write_enabled=True,
        allowed_operations=[], denied_operations=[], safety_flags=[], warnings=[], errors=[]
    )
    txt = read_only_verifier_to_text({"read_only_status": "PASS", "source_path": "src", "output_path": "out"})
    assert "PASS" in txt
    assert "src" in txt
